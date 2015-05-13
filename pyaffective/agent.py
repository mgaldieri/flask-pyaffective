__author__ = 'mgaldieri'
from emotions import OCEAN, OCC, PAD
from time import time
from copy import deepcopy
import numpy as np


class Agent():
    # TODO: make event wear off
    def __init__(self, personality=None):
        self.personality = self.set_personality(personality) if personality else OCEAN()
        self.neurotics = 1+((self.personality.neuroticism+1.0)/2.0)
        self.timer = time()
        self.time_threshold = 60
        self.forward = False
        self.events = []

    def set_personality(self, personality=None):
        self.personality = personality if personality else OCEAN()
        self.mood = deepcopy(self.personality.pad.state)
        self.source = deepcopy(self.personality.pad.state)
        self.target = deepcopy(self.personality.pad.state)

    def put(self, vals=None):
        self.timer = time()
        self.source = deepcopy(self.mood)
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

    def get(self, mode='pad'):
        '''
        >>> a = np.array([3,2])
        >>> b = np.array([8,5])
        >>> k = 0.6
        >>> p = k*b+(1-k)*a
        :param mode:
        :return:
        '''
        if len(self.events) > 0:
            self.target = np.median(self.events, axis=0)
            self.events = []

        # print 'Source: '+str(self.source)
        # print 'Target: '+str(self.target)
        # print 'Mood: '+str(self.mood)

        thres = self.time_threshold/self.neurotics
        delta_t = time() - self.timer
        if delta_t > 60:
            delta_t = 60
        k = (float(thres)-float(delta_t))/float(thres)

        if self.forward:
            self.mood = k * self.source + (1-k) * self.target
        else:
            self.mood = k * self.personality.pad.state + (1-k) * self.source

        # if np.allclose(self.mood, self.personality.pad.state):
        #     delta_t = 60
        # if np.allclose(self.mood, self.target):
        #     delta_t = 60

        return PAD(pleasure=self.mood[0], arousal=self.mood[1], dominance=self.mood[2])

    @staticmethod
    def get_progress(delta):
        # quadratic progress
        if not 0.0 <= delta <= 1.0:
            raise ValueError("Delta deve possuir um valor entre 0.0 e 1.0")
        return -delta * (delta-2)

    @staticmethod
    def get_point_on_line(x0, y0, z0, x1, y1, z1, progress):
        x = ((x1-x0) * progress) + x0
        y = ((y1-y0) * progress) + y0
        z = ((z1-z0) * progress) + z0
        return x, y, z
