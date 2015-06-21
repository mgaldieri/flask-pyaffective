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
from scipy.spatial.distance import cosine
import numpy as np
import operator


class PAD:
    pleasure = 0.0
    arousal = 0.0
    dominance = 0.0

    def __init__(self, pleasure=None, arousal=None, dominance=None, state=np.zeros(3)):
        if not all([pleasure is None, arousal is None, dominance is None]):
            _state = np.array([pleasure, arousal, dominance])
            _norm = np.linalg.norm(_state, np.inf)
            if _norm > 1:
                self.state = _state/_norm
            else:
                self.state = _state
        else:
            _norm = np.linalg.norm(state, np.inf)
            if _norm > 1:
                self.state = state/_norm
            else:
                self.state = state
        self.pleasure = self.state[0]
        self.arousal = self.state[1]
        self.dominance = self.state[2]

        self.states = {
            'exuberante': np.array([1.0, 1.0, 1.0]),
            'dependente': np.array([1.0, 1.0, -1.0]),
            'relaxado': np.array([1.0, -1.0, 1.0]),
            'dócil': np.array([1.0, -1.0, -1.0]),

            'entediado': np.array([-1.0, -1.0, -1.0]),
            'desdenhoso': np.array([-1.0, -1.0, 1.0]),
            'ansioso': np.array([-1.0, 1.0, -1.0]),
            'hostil': np.array([-1.0, 1.0, 1.0])
        }
        self.levels = ['levemente', 'moderadamente', 'altamente']

    def mood(self):
        idx, val = min(enumerate([cosine(self.state, s) for s in self.states.values()]), key=operator.itemgetter(1))
        level = self.levels[int(round((len(self.levels)-1)*np.linalg.norm(self.state)/np.linalg.norm(np.ones(3))))]
        return ' '.join([level, self.states.keys()[idx]])

    def __repr__(self):
        return '<PAD: %s>' % self.mood()


class OCEAN:
    def __init__(self, openness=None, conscientiousness=None, extraversion=None, agreeableness=None, neuroticism=None, personality=np.zeros(5)):
        if not all([openness is None, conscientiousness is None, extraversion is None, agreeableness is None, neuroticism is None]):
            _personality = np.array([openness, conscientiousness, extraversion, agreeableness, neuroticism])
            _norm = np.linalg.norm(_personality, np.inf)
            if _norm > 1:
                self.personality = _personality/_norm
            else:
                self.personality = _personality
        else:
            _norm = np.linalg.norm(personality, np.inf)
            if _norm > 1:
                self.personality = personality/_norm
            else:
                self.personality = personality
        self.openness = self.personality[0]
        self.conscientiousness = self.personality[1]
        self.extraversion = self.personality[2]
        self.agreeableness = self.personality[3]
        self.neuroticism = self.personality[4]

        self.pad = self.set_pad()

    def set_pad(self):
        pleasure = 0.21*self.extraversion + 0.59*self.agreeableness + 0.19*self.neuroticism
        arousal = 0.15*self.openness + 0.30*self.agreeableness - 0.57*self.neuroticism
        dominance = 0.25*self.openness + 0.17*self.conscientiousness + 0.60*self.extraversion - 0.32*self.neuroticism
        return PAD(pleasure, arousal, dominance)


class OCC:
    pad_map = {
        'admiration': {'P': 0.5, 'A': 0.3, 'D': -0.2, 'valence': 1},
        'gloating': {'P': 0.3, 'A': -0.3, 'D': -0.1, 'valence': 1},
        'gratification': {'P': 0.6, 'A': 0.5, 'D': 0.4, 'valence': 1},
        'gratitude': {'P': 0.4, 'A': 0.2, 'D': -0.3, 'valence': 1},
        'hope': {'P': 0.2, 'A': 0.2, 'D': -0.1, 'valence': 1},
        'happy_for': {'P': 0.4, 'A': 0.2, 'D': 0.2, 'valence': 1},
        'joy': {'P': 0.4, 'A': 0.2, 'D': 0.1, 'valence': 1},
        'liking': {'P': 0.4, 'A': 0.16, 'D': -0.24, 'valence': 1},
        'love': {'P': 0.3, 'A': 0.1, 'D': 0.2, 'valence': 1},
        'pride': {'P': 0.4, 'A': 0.3, 'D': 0.3, 'valence': 1},
        'relief': {'P': 0.2, 'A': -0.3, 'D': 0.4, 'valence': 1},
        'satisfaction': {'P': 0.3, 'A': -0.2, 'D': 0.4, 'valence': 1},

        'anger': {'P': -0.51, 'A': 0.59, 'D': 0.25, 'valence': -1},
        'disliking': {'P': -0.4, 'A': 0.2, 'D': 0.1, 'valence': -1},
        'disappointment': {'P': -0.3, 'A': 0.1, 'D': -0.4, 'valence': -1},
        'distress': {'P': -0.4, 'A': -0.2, 'D': -0.5, 'valence': -1},
        'fear': {'P': -0.64, 'A': 0.6, 'D': -0.43, 'valence': -1},
        'fears_confirmed': {'P': -0.5, 'A': -0.3, 'D': -0.7, 'valence': -1},
        'hate': {'P': -0.6, 'A': 0.6, 'D': 0.3, 'valence': -1},
        'pity': {'P': -0.4, 'A': -0.2, 'D': -0.5, 'valence': -1},
        'remorse': {'P': -0.3, 'A': 0.1, 'D': -0.6, 'valence': -1},
        'reproach': {'P': -0.3, 'A': -0.1, 'D': 0.4, 'valence': -1},
        'resentment': {'P': -0.2, 'A': -0.3, 'D': -0.2, 'valence': -1},
        'shame': {'P': -0.3, 'A': 0.1, 'D': -0.6, 'valence': -1},
    }

    def __init__(self,
                 admiration=None,
                 gloating=None,
                 gratification=None,
                 gratitude=None,
                 hope=None,
                 happy_for=None,
                 joy=None,
                 liking=None,
                 love=None,
                 pride=None,
                 relief=None,
                 satisfaction=None,

                 anger=None,
                 disliking=None,
                 disappointment=None,
                 distress=None,
                 fear=None,
                 fears_confirmed=None,
                 hate=None,
                 pity=None,
                 remorse=None,
                 reproach=None,
                 resentment=None,
                 shame=None,

                 pad=None):
        if not all([admiration is None, gloating is None, gratification is None, gratitude is None, hope is None, happy_for is None,
                    joy is None, liking is None, love is None, pride is None, relief is None, satisfaction is None,
                    anger is None, disliking is None, disappointment is None, distress is None, fear is None, fears_confirmed is None,
                    hate is None, pity is None, remorse is None, reproach is None, resentment is None, shame is None]):
            self.admiration = admiration
            self.gloating = gloating
            self.gratification = gratification
            self.gratitude = gratitude
            self.hope = hope
            self.happy_for = happy_for
            self.joy = joy
            self.liking = liking
            self.love = love
            self.pride = pride
            self.relief = relief
            self.satisfaction = satisfaction

            self.anger = anger
            self.disliking = disliking
            self.disappointment = disappointment
            self.distress = distress
            self.fear = fear
            self.fears_confirmed = fears_confirmed
            self.hate = hate
            self.pity = pity
            self.remorse = remorse
            self.reproach = reproach
            self.resentment = resentment
            self.shame = shame

            self.pad = self.set_pad()
        else:
            if isinstance(pad, np.ndarray):
                self.pad = PAD(pleasure=pad[0], arousal=pad[1], dominance=pad[3]) if pad else self.set_pad()
            elif isinstance(pad, PAD):
                self.pad = pad
            else:
                raise Exception('Invalid event type')

    def set_pad(self):
        emotion = {'P': 0.0, 'A': 0.0, 'D': 0.0}
        for attr in self.pad_map.keys():
            temp = self.__dict__.get(attr)
            emotion = {k: emotion[k]+temp*self.pad_map[attr][k] for k in (set(self.pad_map[attr].keys())-{'valence'})}
        return PAD(pleasure=emotion['P'], arousal=emotion['A'], dominance=emotion['D'])
