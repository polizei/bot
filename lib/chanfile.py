# encoding: utf-8
# vim: ts=4 noexpandtab

import pickle

class Chanfile(list):
    def __new__(cls, filename):
        try:
            f = open(filename, 'r')
            s = f.read()
            f.close()
        except:
            s = None

        if s is not None:
            return pickle.loads(s)

    def save(self, filename):
        try:
            f = open(filename)
            f.write(pickle.dumps(self))
            f.close()
        except:
            pass
