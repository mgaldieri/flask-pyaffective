__author__ = 'mgaldieri'

from time import time


class Event:
    def __init__(self, values=None, duration=1.0):
        if values is None:
            values = []
        self.values = values
        self.duration = duration
        self.start_time = time()

    def get_influence(self):
        n = (time() - self.start_time)/self.duration
        if n < 0:
            n = 0
        if n > 1:
            n = 1
        return n*(n-2)+1
