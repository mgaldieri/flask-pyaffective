__author__ = 'mgaldieri'
from emotions import OCEAN, OCC, PAD
from time import time
from copy import deepcopy
from events import Event
import numpy as np

from collections import namedtuple
from Queue import Queue
import threading

Invocation = namedtuple('Invocation', ('fn', 'args', 'kwargs'))


class Agent:
    # TODO: make event wear off
    def __init__(self, personality=None):
        self.mood = None
        self.source = None
        self.target = None
        self.personality = self.set_personality(personality) if personality else OCEAN()

        self.neurotics = 1+((self.personality.neuroticism+1.0)/2.0)
        self.timer = time()
        self.time_threshold = 60
        self.forward = False

        # newer implementation
        self._in_q = Queue()
        self._out_q = Queue(1)
        self.FRAMES_PER_SECOND = 60.0
        self.MS_PER_UPDATE = 1.0/self.FRAMES_PER_SECOND
        self.TIME_TO_TRAVEL = 1.0  # seconds
        self.BASE_VELOCITY = self.TIME_TO_TRAVEL/self.MS_PER_UPDATE
        self.DISTANCE_TOLERANCE = 1.0/100.0

    def start(self):
        data = threading.local()
        thread = threading.Thread(name='Agent Runloop', target=self._run, args=(data,))
        thread.daemon = True
        thread.start()

    def stop(self):
        self._in_q.put(Invocation(self._stop, (), {}))

    def put(self, values=None):
        if values:
            if isinstance(values, np.ndarray):
                v = values
            elif isinstance(values, PAD):
                v = values.state
            elif isinstance(values, OCC):
                v = values.pad.state
            else:
                v = None
            if v:
                self._in_q.put(Invocation(self._put, (v,), {}))

    def get(self):
        mood = self._out_q.get()
        if mood and len(mood) == 3:
            return PAD(pleasure=mood[0], arousal=mood[1], dominance=mood[2])

    def _run(self, data):
        data.running = True
        data.events = []
        data.state = []
        previous = time()
        lag = 0.0
        print 'running...'
        while data.running:
            current = time()
            elapsed = current - previous
            previous = current
            lag += elapsed

            self._process_input(data)

            while lag >= self.MS_PER_UPDATE:
                self._update(data)
                lag -= self.MS_PER_UPDATE

            self._process_output(data)
        print 'stopped!'

    def _process_input(self, data):
        while not self._in_q.empty():
            job = self._in_q.get()
            job.fn(data, *job.args, **job.kwargs)

    def _process_output(self, data):
        if self._out_q.full():
            self._out_q.get()
        self._out_q.put(data.state)

    def _update(self, data):
        # TODO: process internal state
        if len(data.events) > 0:
            # calculate events weighted average
            vectors = [e.values for e in data.events]
            weights = [e.influence for e in data.events]
            avg_event = np.average(vectors, axis=0, weights=weights)
            # move mood towards average event
            if np.allclose(data.state, avg_event):
                data.state = avg_event
            else:
                pass
        else:
            # move mood towards personality
            pass

        pass

    def _stop(self, data):
        print 'stopping...'
        data.running = False

    def _put(self, data, value):
        print 'putting data...'
        data.events.append(Event(value))

    def set_personality(self, personality=None):
        self.personality = personality if personality else OCEAN()
        self.mood = deepcopy(self.personality.pad.state)
        self.source = deepcopy(self.personality.pad.state)
        self.target = deepcopy(self.personality.pad.state)

    # def put(self, vals=None):
    #     self.timer = time()
    #     self.source = deepcopy(self.mood)
    #     if vals:
    #         if isinstance(vals, np.ndarray):
    #             self.events.append(vals)
    #             #self.return_source = vals
    #         elif isinstance(vals, PAD):
    #             self.events.append(vals.state)
    #         elif isinstance(vals, OCC):
    #             self.events.append(vals.pad.state)
    #         else:
    #             raise Exception('Invalid event type')
    #         self.forward = True
    #     else:
    #         self.forward = False

    # def get(self, mode='pad'):
    #     """
    #     >>> a = np.array([3,2])
    #     >>> b = np.array([8,5])
    #     >>> k = 0.6
    #     >>> p = k*b+(1-k)*a
    #     :param mode:
    #     :return:
    #     """
    #     if len(self.events) > 0:
    #         self.target = np.median(self.events, axis=0)
    #         self.events = []
    #
    #     # print 'Source: '+str(self.source)
    #     # print 'Target: '+str(self.target)
    #     # print 'Mood: '+str(self.mood)
    #
    #     thres = self.time_threshold/self.neurotics
    #     delta_t = time() - self.timer
    #     if delta_t > 60:
    #         delta_t = 60
    #     k = (float(thres)-float(delta_t))/float(thres)
    #
    #     if self.forward:
    #         self.mood = k * self.source + (1-k) * self.target
    #     else:
    #         self.mood = k * self.personality.pad.state + (1-k) * self.source
    #
    #     # if np.allclose(self.mood, self.personality.pad.state):
    #     #     delta_t = 60
    #     # if np.allclose(self.mood, self.target):
    #     #     delta_t = 60
    #
    #     return PAD(pleasure=self.mood[0], arousal=self.mood[1], dominance=self.mood[2])

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
