# encoding: utf-8
# vim: ts=4 noexpandtab

from lib.hooks import HOOK_MOTD_MESSAGE
from lib.hooks import HOOK_MOTD_END
from lib.hooks import HOOK_MOTD_START
from lib.hooks import HOOK_CONNECT
from lib.util import tokenize
from lib.util import underscore
from lib.hooks import *

class IRC:
    bot = None
    plugins = None

    def __init__(self, bot):
        self.bot = bot
        self.reload_plugins()

    def reload_plugins(self):
        if self.plugins is not None:
            del self.plugins

        self.plugins = []

        for plugin in self.bot.config.plugins:
            underscored = underscore(plugin)

            try:
                exec 'del %s' % (plugin)
            except:
                pass

            try:
                exec 'from plugins.%s import %s' % (underscored, plugin)
                exec 'self.plugins.append(%s(self))' % (plugin)
            except:
                pass

    def process(self, line):
        bot = self.bot
        session = bot.session
        words, words_eol = tokenize(line)
        cnt = len(words)

        if words[0] == 'PING':
            if cnt > 1:
                self.bot.send('PONG %s' % (words_eol[1]))
            else:
                self.bot.send('PONG')
        elif words[0][0] == ':':
            if words[1].isdigit():
                num = int(words[1], 10)

                if num == 1:
                    bot.fire(HOOK_CONNECT)
                elif num == 375:
                    bot.fire(HOOK_MOTD_START)
                elif num == 372:
                    bot.fire(HOOK_MOTD_MESSAGE, words_eol[2][1:])
                elif num == 376:
                    bot.fire(HOOK_MOTD_END)

        else:
            print line
