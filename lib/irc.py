    # encoding: utf-8
    # vim: ts=4 noexpandtab

from lib.util import tokenize
from lib.util import underscore

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
        words, words_eol = tokenize(line)

        if words[0] == 'PING':
            if len(words) > 1:
                self.bot.send('PONG %s' % (words_eol[1]))
            else:
                self.bot.send('PONG')
        else:
            print line
