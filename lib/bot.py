# encoding: utf-8
# vim: ts=4 noexpandtab

import time
import socket
from threading import Thread
from collections import deque
from lib.util import singleton
from lib.irc import IRC
from lib.session import Session
from lib.userfile import Userfile
from lib.chanfile import Chanfile

@singleton
class Bot:
    irc = None
    thread = None
    session = None

    userfile = None
    chanfile = None

    socket = None
    config = None
    server = None

    buf = ''

    hooks = None

    def __init__(self):
        self.rehash()

        self.thread = _Thread(self)
        self.thread.start()

        self.userfile = Userfile(self.config.userfile)
        self.chanfile = Chanfile(self.config.chanfile)

    def rehash(self):
        if self.userfile is not None:
            self.userfile.save()

        if self.chanfile is not None:
            self.chanfile.save()

        from config import Config
        self.config = Config()
        del Config

        self.hooks = []

        if self.irc is not None:
            del self.irc

        self.irc = IRC(self)

    def reconnect(self):
        # close connection, if any
        if self.socket is not None:
            self.socket.close()
            self.socket = None
            self.buf = ''

        # pick first server in list
        entry = self.config.servers[0]
        self.server = dict(addr=(entry[0], entry[1] or 6667,),
                           password=entry[2])

        # rotate server list
        self.config.servers.rotate()

        # determine address family
        try:
            addrinfo = socket.getaddrinfo(self.server['addr'][0],
                                          self.server['addr'][1])
            self.server['proto'] = addrinfo[0][0]
            self.server['resolved'] = addrinfo[0][4]
        except:
            return

        # create socket
        self.socket = socket.socket(self.server['proto'], socket.SOCK_STREAM)

        # bind address, if any
        if self.config.bindaddr is not None:
            self.socket.bind(self.config.bindaddr)

        # operate in non-blocking mode
        self.socket.setblocking(0)

        # connect!
        try:
            self.socket.connect(self.server['resolved'])
        except socket.error as err:
            # operation in progress
            if err[0] != 115:
                self.socket = None

        # sleep for a little while
        time.sleep(0.1)

        # destroy previous session and start a new one
        if self.session is not None:
            del self.session

        self.session = Session()

        # send password, if any
        if self.server['password'] is not None:
            self.send('PASS %s' % (self.server['password']))

        # register within server
        self.send('USER %s "" %s :%s' % (self.config.username,
                                         self.server['addr'][0],
                                         self.config.realname))
        self.send('NICK %s' % (self.config.nickname))

    def dispatch(self):
        while True:
            if not self.socket:
                self.reconnect()
                continue

            if self.socket is not None:
                line = self.readline()
                if line is not None:
                    self.irc.process(line)

    def send(self, line, queue=0):
        if self.socket is not None:
            if queue == -1:
                try:
                    self.socket.send(line + '\r\n')
                except socket.error as err:
                    print err
            else:
                self.thread.queues[queue].append(line)

    def readline(self):
        # check stale bytes first
        if '\n' in self.buf:
            line, self.buf = self.buf.split('\n', 1)
            return line

        # sleep for a little while
        time.sleep(0.25)

        # read from socket
        try:
            tmp = self.socket.recv(4096)
        except socket.error as err:
            tmp = None

            #  skip "would block" error
            if err[0] != 11:
                self.socket = None

        # if nothing read, nothing read
        if tmp is None:
            return None

        # append to stale
        self.buf = ''.join([self.buf, tmp]) \
                        .replace('\r', '\n') \
                            .replace('\n\n', '\n')

        # if something read, something read
        if '\n' in self.buf:
            line, self.buf = self.buf.split('\n', 1)
            return line

        # nothing read then
        return None

    def hook(self, event, callback):
        hooks = self.hooks.get(event, [])
        hooks.append(callback)
        self.hooks[event] = hooks

    def unnook(self, event, callback=None):
        if callback is None:
            del self.hooks[event]
        else:
            try:
                self.hooks.get(event, []).remove(callback)
            except:
                pass

    def fire(self, event, *kargs):
        [callback(*kargs) for callback in self.hooks.get(event, [])]

class _Thread(Thread):
    x = -1
    bot = None
    queues = [deque(), deque()]
    running = True

    def __init__(self, bot):
        super(_Thread, self).__init__()

        self.bot = bot

    def run(self):
        while self.running:
            self.x += 1

            if self.x % 2:
                if (len(self.queues[1])):
                    self.bot.send(self.queues[1].popleft(), -1)

            if (len(self.queues[0])):
                self.bot.send(self.queues[0].popleft(), -1)

            time.sleep(0.4)

    def stop(self):
        self.running = False
