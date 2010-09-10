# encoding: utf-8
# vim: ts=4 noexpandtab

from re import sub as rsub
from hashlib import md5

def singleton(cls):
    instances = {}

    def get_instance(*kargs, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*kargs, **kwargs)

        return instances[cls]

    return get_instance

def underscore(what):
    return rsub('([A-Z]+)', r'_\1', rsub('([A-Z]+)([A-Z][a-z])', r'_\1_\2',
                what)).lstrip('_').lower()

def tokenize(line):
    words = [word for word in line.split(' ') if len(word) > 0]
    words_eol = [' '.join(words[x:]) for x in range(len(words))]
    return words, words_eol

def lower(what):
    result = what.lower()
    for x in _lower:
        result = result.replace(x, _lower[x])
    return result

def crypt(what):
    return md5(what).hexdigest()

_lower = {'[':'{', ']': '}', '\\': '|'}
