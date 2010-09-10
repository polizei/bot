# encoding: utf-8
# vim: ts=4 noexpandtab

class Plugin:
    bot = None
    hooks = dict()

    def __init__(self, bot):
        self.bot = bot

