# -*- coding:utf-8 -*-
"""
The MIT License (MIT)
Copyright (c) 2015 Mauricio Galdieri

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
OR OTHER DEALINGS IN THE SOFTWARE.
"""

__author__ = 'mgaldieri'
from emotions import OCEAN, OCC, PAD
from time import time
from events import Event
import numpy as np

from collections import namedtuple
from Queue import Queue
import threading

Invocation = namedtuple('Invocation', ('fn', 'args', 'kwargs'))


class Agent:
    def __init__(self, personality=None):
        self.personality = None
        self.neurotics = 0.0
        self.MAX_NEUROTICS = 3.0
        self._in_q = Queue()
        self._out_q = Queue(1)
        self.FRAMES_PER_SECOND = 60.0
        self.SECS_PER_UPDATE = 1.0/self.FRAMES_PER_SECOND
        self.EVENT_DURATION = 1.0  # seconds
        self.BASE_VELOCITY = 1.0/250  # self.TIME_TO_TRAVEL*self.SECS_PER_UPDATE
        self.DISTANCE_TOLERANCE = 1.0/10000.0

        self.set_personality(personality)

    def start(self):
        data = threading.local()
        thread = threading.Thread(name='Agent Runloop', target=self._run, args=(data,))
        thread.daemon = True
        thread.start()

    def stop(self):
        self._in_q.put_nowait(Invocation(self._stop, (), {}))

    def put(self, values=None):
        if values:
            if isinstance(values, np.ndarray):
                v = values
            elif isinstance(values, OCC):
                v = values.pad.state
            else:
                raise ValueError('Valores de evento inválidos')
            self._in_q.put_nowait(Invocation(self._put, (v,), {}))

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
        self._in_q.put_nowait(Invocation(self._set_personality, (ocean,), {}))

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
            while lag >= self.SECS_PER_UPDATE:
                self._update(data)
                lag -= self.SECS_PER_UPDATE

            self._process_output(data)
        print 'stopped!'

    def _process_input(self, data):
        while not self._in_q.empty():
            job = self._in_q.get()
            job.fn(data, *job.args, **job.kwargs)

    def _process_output(self, data):
        if self._out_q.full():
            with self._out_q.mutex:
                self._out_q.queue.clear()
        self._out_q.put_nowait(data.state)

    def _update(self, data):
        if len(data.events) > 0:
            # calculate events weighted average
            vectors = []
            weights = []
            replacement = []
            for i in range(len(data.events)):
                if data.events[i].get_influence() > 0:
                    vectors.append(data.events[i].values)
                    weights.append(data.events[i].get_influence())
                    replacement.append(data.events[i])
            data.events = list(replacement)
            if len(vectors) > 0 and len(weights) > 0:
                avg_event = np.average(vectors, axis=0, weights=weights)
                # move mood towards average event
                data.state = self._move_to(data.state, avg_event)
        else:
            # move mood towards personality
            data.state = self._move_to(data.state, data.personality)

    def _move_to(self, _from, _to):
        if np.allclose(_from, _to, self.DISTANCE_TOLERANCE):
            return np.array(_to)
        direction = _to - _from
        direction /= np.linalg.norm(direction)
        _from += direction * self.BASE_VELOCITY * self.neurotics
        return _from

    def _stop(self, data):
        print 'stopping...'
        data.running = False

    def _put(self, data, value):
        print 'putting data...'
        data.events.append(Event(value, self.EVENT_DURATION))

    def _set_personality(self, data, value):
        print 'setting personality...'
        data.personality = np.array(value.pad.state)
        data.state = np.array(value.pad.state)
        self.personality = value
        self.neurotics = Agent.map_value(value.neuroticism, -1, 1, 1, self.MAX_NEUROTICS)

    @staticmethod
    def map_value(value=0.0, in_min=0.0, in_max=1.0, out_min=0.0, out_max=1.0):
        return (float(value) - float(in_min)) * (float(out_max) - float(out_min)) / (
            float(in_max) - float(in_min)) + float(out_min)
