# encoding: utf-8
# vim: ts=4 noexpandtab

from collections import deque

class Config:
    nickname = 'Python1'
    username = 'Python'
    realname = 'Python'

    servers = deque([('127.0.0.1', 1234, 'letmein',),
                     ('127.0.0.1', 9000, None,)])

    bindaddr = None

    userfile = 'users.db'
    chanfile = 'chans.db'

    plugins = ['DCC', 'Commands']
