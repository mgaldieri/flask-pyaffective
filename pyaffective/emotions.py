# -*- coding:utf-8 -*-
__author__ = 'mgaldieri'
from scipy.spatial.distance import cosine
import numpy as np
import operator


class PAD():
    pleasure = 0.0
    arousal = 0.0
    dominance = 0.0

    def __init__(self, pleasure=None, arousal=None, dominance=None, state=np.zeros(3)):
        if not all([pleasure==None, arousal==None, dominance==None]):
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


class OCEAN():
    def __init__(self, openness=None, conscientiousness=None, extraversion=None, agreeableness=None, neuroticism=None, personality=np.zeros(5)):
        if not all([openness==None, conscientiousness==None, extraversion==None, agreeableness==None, neuroticism==None]):
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


class OCC():
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
        if not all([admiration==None, gloating==None, gratification==None, gratitude==None, hope==None, happy_for==None,
                    joy==None, liking==None, love==None, pride==None, relief==None, satisfaction==None,
                    anger==None, disliking==None, disappointment==None, distress==None, fear==None, fears_confirmed==None,
                    hate==None, pity==None, remorse==None, reproach==None, resentment==None, shame==None]):
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
        self.pad = PAD(pleasure=pad[0], arousal=pad[1], dominance=pad[3]) if pad else self.set_pad()

        self.pad_map = {
            'admiration': {'P': 0.5, 'A': 0.3, 'D': -0.2},
            'gloating': {'P': 0.3, 'A': -0.3, 'D': -0.1},
            'gratification': {'P': 0.6, 'A': 0.5, 'D': 0.4},
            'gratitude': {'P': 0.4, 'A': 0.2, 'D': -0.3},
            'hope': {'P': 0.2, 'A': 0.2, 'D': -0.1},
            'happy_for': {'P': 0.4, 'A': 0.2, 'D': 0.2},
            'joy': {'P': 0.4, 'A': 0.2, 'D': 0.1},
            'liking': {'P': 0.4, 'A': 0.16, 'D': -0.24},
            'love': {'P': 0.3, 'A': 0.1, 'D': 0.2},
            'pride': {'P': 0.4, 'A': 0.3, 'D': 0.3},
            'relief': {'P': 0.2, 'A': -0.3, 'D': 0.4},
            'satisfaction': {'P': 0.3, 'A': -0.2, 'D': 0.4},

            'anger': {'P': -0.51, 'A': 0.59, 'D': 0.25},
            'disliking': {'P': -0.4, 'A': 0.2, 'D': 0.1},
            'disappointment': {'P': -0.3, 'A': 0.1, 'D': -0.4},
            'distress': {'P': -0.4, 'A': -0.2, 'D': -0.5},
            'fear': {'P': -0.64, 'A': 0.6, 'D': -0.43},
            'fears_confirmed': {'P': -0.5, 'A': -0.3, 'D': -0.7},
            'hate': {'P': -0.6, 'A': 0.6, 'D': 0.3},
            'pity': {'P': -0.4, 'A': -0.2, 'D': -0.5},
            'remorse': {'P': -0.3, 'A': 0.1, 'D': -0.6},
            'reproach': {'P': -0.3, 'A': -0.1, 'D': 0.4},
            'resentment': {'P': -0.2, 'A': -0.3, 'D': -0.2},
            'shame': {'P': -0.3, 'A': 0.1, 'D': -0.6},
        }

    def set_pad(self):
        emotion = {'P': 0.0, 'A': 0.0, 'D': 0.0}
        for attr in self.__dict__:
            temp = self.__dict__[attr]
            emotion = {k: emotion[k]+temp*self.pad_map[attr][k] for k in temp}
        emotion = {k: emotion[k]/24 for k in emotion}
        return PAD(pleasure=emotion[0], arousal=emotion[1], dominance=emotion[2])