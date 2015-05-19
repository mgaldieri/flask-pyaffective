# -*- coding:utf-8 -*-
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
    def __init__(self, personality=None):
        self.personality = None
        self._in_q = Queue()
        self._out_q = Queue(1)
        self.FRAMES_PER_SECOND = 60.0
        self.MS_PER_UPDATE = 1.0/self.FRAMES_PER_SECOND
        self.TIME_TO_TRAVEL = 1.0  # seconds
        self.BASE_VELOCITY = self.TIME_TO_TRAVEL/self.MS_PER_UPDATE
        self.DISTANCE_TOLERANCE = 1.0/100.0

        self.set_personality(personality)
        self.neurotics = 1+((self.personality.neuroticism+1.0)/2.0)

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
            elif isinstance(values, OCC):
                v = values.pad.state
            else:
                raise ValueError('Valores de evento inválidos')
            if v:
                self._in_q.put(Invocation(self._put, (v,), {}))

    def get(self):
        mood = self._out_q.get()
        if mood is not None and len(mood) == 3:
            return PAD(pleasure=mood[0], arousal=mood[1], dominance=mood[2])

    def set_personality(self, values):
        if values:
            if isinstance(values, np.ndarray):
                ocean = OCEAN(personality=values)
            elif isinstance(values, OCEAN):
                ocean = values
            else:
                raise ValueError('Valores de personalidade inválidos')
        else:
            ocean = OCEAN()
        self._in_q.put(Invocation(self._set_personality, (ocean,), {}))
        self.personality = ocean

    def _run(self, data):
        data.running = True
        data.events = []
        data.state = np.zeros(3)
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
        if len(data.events) > 0:
            # calculate events weighted average
            vectors = []
            weights = []
            for i in range(len(data.events)):
                if data.events[i].get_influence() > 0:
                    vectors.append(data.events[i].value)
                    weights.append(data.events[i].get_influence())
                else:
                    data.events.pop(i)
            avg_event = np.average(vectors, axis=0, weights=weights)
            # move mood towards average event
            self._move_to(data.state, avg_event)
        else:
            # move mood towards personalit
            self._move_to(data.state, data.personality)

    def _move_to(self, _from, _to):
        if np.allclose(_from, _to, self.DISTANCE_TOLERANCE):
            _from = _to
        else:
            direction = _to - _from
            direction = direction/np.linalg.norm(direction)
            _from = direction + self.BASE_VELOCITY * self.neurotics

    def _stop(self, data):
        print 'stopping...'
        data.running = False

    def _put(self, data, value):
        print 'putting data...'
        data.events.append(Event(value))

    def _set_personality(self, data, value):
        print 'setting personality...'
        data.personality = value.pad.state
        data.state = value.pad.state
