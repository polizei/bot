#!/usr/bin/env python
# encoding: utf-8
# vim: ts=4 noexpandtab

from lib.bot import Bot

def main():
    bot = Bot()

    try:
        bot.dispatch()
    except KeyboardInterrupt:
        bot.thread.stop()

if __name__ == '__main__':
    main()
