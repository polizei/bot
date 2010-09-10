# encoding: utf-8
# vim: ts=4 noexpandtab

from lib.util import lower

class Session:
    nickname = None
    username = None

    channels = {}

    def add_channel(self, channel):
        channel_lower = lower(channel)

        if self.channels.get(channel_lower) is None:
            self.channels[channel_lower] = {'nicks': {},
                                            'mode': '',
                                            'topic': '',}

    def remove_channel(self, channel):
        del self.channels[lower(channel)]

    def update_channel(self, channel, mode=None, topic=None):
        channel_lower = lower(channel)

        if mode is not None:
            self.channels[channel_lower]['mode'] = mode

        if topic is not None:
            self.channels[channel_lower]['topic'] = topic

    def add_nick(self, nick, channel):
        self.add_channel(channel)

        self.channels[lower(channel)]['nicks'][lower(nick)] = [nick, None,
                                                               None, None]

    def remove_nick(self, nick, channel=None):
        nick_lower = lower(nick)

        if channel is None:
            for channel in self.channels:
                del self.channels[channel]['nicks'][nick_lower]
        else:
            del self.channels[lower(channel)]['nicks'][nick_lower]

    def update_nick(self, nick, channel, user=None, host=None, mode=None):
        nick_lower = lower(nick)
        channel_lower = lower(channel)

        if user is not None:
            self.channels[channel_lower]['nicks'][nick_lower][1] = user

        if host is not None:
            self.channels[channel_lower]['nicks'][nick_lower][2] = host

        if mode is not None:
            self.channels[channel_lower]['nicks'][nick_lower][3] = mode

    def get_nick_user(self, nick, channel=None):
        return self.channels.get(lower(channel), {'nicks': {}}). \
                             get(lower(nick), [None, None])[1]

    def get_nick_host(self, nick, channel=None):
        return self.channels.get(lower(channel), {'nicks': {}}). \
                             get(lower(nick), [None, None, None])[2]

    def get_nick_mode(self, nick, channel):
        return self.channels.get(lower(channel), {'nicks': {}}). \
                             get(lower(nick), [None, None, None, None])[3]

    def is_op(self, nick, channel):
        return '@' in (self.get_nick_mode(nick, channel) or '')

    def is_voice(self, nick, channel):
        return '+' in (self.get_nick_mode(nick, channel) or '')
