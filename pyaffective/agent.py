__author__ = 'mgaldieri'
from emotions import OCEAN, OCC, PAD
from time import time
import numpy as np


class Agent():
    # TODO: make event wear off
    def __init__(self, personality=None):
        self.personality = self.set_personality(personality) if personality else OCEAN()
        self.mood = self.personality.pad.state
        self.neurotics = 1+((self.personality.neuroticism+1.0)/2.0)
        self.timer = time()
        self.time_threshold = 60
        self.return_source = None
        self.forward = False
        self.events = []

    def set_personality(self, personality=None):
        self.personality = personality if personality else OCEAN()

    def put(self, vals=None):
        self.timer = time()
        if vals:
            if isinstance(vals, np.ndarray):
                self.events.append(vals)
                #self.return_source = vals
            elif isinstance(vals, PAD):
                self.events.append(vals.state)
            elif isinstance(vals, OCC):
                self.events.append(vals.pad.state)
            else:
                raise Exception('Invalid event type')
            self.forward = True
        else:
            self.forward = False
            self.return_source = self.mood

    def get(self, mode='pad'):
        '''
        >>> a = np.array([3,2])
        >>> b = np.array([8,5])
        >>> k = 0.6
        >>> p = k*b+(1-k)*a
        :param mode:
        :return:
        '''
        if np.allclose(self.mood, self.return_source):
            return self.return_source
        if np.allclose(self.mood, self.personality.pad.state):
            return self.personality.pad.state
        thres = self.time_threshold/self.neurotics
        delta_t = time() - self.timer
        if delta_t > 60:
            delta_t = 60
        k = (float(thres)-float(delta_t))/float(thres)
        if self.forward:
            self.return_source = np.median(self.events)
            self.mood = k * self.return_source + (1-k) * self.personality.pad.state
        else:
            self.mood = k * self.personality.pad.state + (1-k) * self.return_source
        return PAD(pleasure=self.mood[0], arousal=self.mood[1], dominance=self.mood[2])