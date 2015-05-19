# -*- coding:utf-8 -*-
__author__ = 'mgaldieri'

import uuid

import numpy as np

from pyaffective.emotions import OCC, OCEAN


class InfluenceValue:
    DIRECT = 1
    INVERSE = -1

    def __init__(self, weight=1.0, relation=None):
        self.weight = weight
        self.relation = relation if relation else InfluenceValue.DIRECT


class Influence:
    def __init__(self, influence=None,
                 openness=InfluenceValue(),
                 conscientiousness=InfluenceValue(),
                 extraversion=InfluenceValue(),
                 agreeableness=InfluenceValue(),
                 neuroticism=InfluenceValue()):
        if not influence:
            influence = []
        if len(influence) == 5 and hasattr(influence, '__iter__'):
            if all(isinstance(x, list) for x in influence) or all(isinstance(x, tuple) for x in influence):
                # self.influence = influence
                self.openness = InfluenceValue(influence[0][0], influence[0][1])
                self.conscientiousness = InfluenceValue(influence[1][0], influence[1][1])
                self.extraversion = InfluenceValue(influence[2][0], influence[2][1])
                self.agreeableness = InfluenceValue(influence[3][0], influence[3][1])
                self.neuroticism = InfluenceValue(influence[4][0], influence[4][1])
            elif all(isinstance(x, dict) for x in influence):
                # self.influence = influence
                self.openness = InfluenceValue(influence[0].get('weight', 0.0), influence[0].get('relation', 0.0))
                self.conscientiousness = InfluenceValue(influence[1].get('weight', 0.0), influence[1].get('relation', 0.0))
                self.extraversion = InfluenceValue(influence[2].get('weight', 0.0), influence[2].get('relation', 0.0))
                self.agreeableness = InfluenceValue(influence[3].get('weight', 0.0), influence[3].get('relation', 0.0))
                self.neuroticism = InfluenceValue(influence[4].get('weight', 0.0), influence[4].get('relation', 0.0))
            else:
                raise ValueError('Valores de influência incompatíveis.')
        elif all(isinstance(x, InfluenceValue) for x in [openness,
                                                         conscientiousness,
                                                         extraversion,
                                                         agreeableness,
                                                         neuroticism]):
            self.openness = openness
            self.conscientiousness = conscientiousness
            self.extraversion = extraversion
            self.agreeableness = agreeableness
            self.neuroticism = neuroticism
            # self.influence = np.array([openness,
            #                            conscientiousness,
            #                            extraversion,
            #                            agreeableness,
            #                            neuroticism], dtype=np.float64)
        else:
            raise ValueError('Valores de influência incompatíveis.')


class Sensor:
    def __init__(self, _id=None, name='No name', minval=0, maxval=1023, influences=None, **kwargs):
        self.id = _id if _id else uuid.uuid4()
        self.name = name
        self.minval = minval
        self.maxval = maxval
        if not influences:
            influences = []
        if isinstance(influences, list) and len(influences) == 24:
            if all(isinstance(x, Influence) for x in influences):
                self.admiration = influences[0]
                self.gloating = influences[1]
                self.gratification = influences[2]
                self.gratitude = influences[3]
                self.hope = influences[4]
                self.happy_for = influences[5]
                self.joy = influences[6]
                self.liking = influences[7]
                self.love = influences[8]
                self.pride = influences[9]
                self.relief = influences[10]
                self.satisfaction = influences[11]

                self.anger = influences[12]
                self.disliking = influences[13]
                self.disappointment = influences[14]
                self.distress = influences[15]
                self.fear = influences[16]
                self.fears_confirmed = influences[17]
                self.hate = influences[18]
                self.pity = influences[19]
                self.remorse = influences[20]
                self.reproach = influences[21]
                self.resentment = influences[22]
                self.shame = influences[23]
            else:
                raise Exception('Tipo de influência incompatível. Por favor utilize o tipo Influence.')
        else:
            self.admiration = kwargs.get('admiration', Influence())
            self.gloating = kwargs.get('gloating', Influence())
            self.gratification = kwargs.get('gratification', Influence())
            self.gratitude = kwargs.get('gratitude', Influence())
            self.hope = kwargs.get('hope', Influence())
            self.happy_for = kwargs.get('happy_for', Influence())
            self.joy = kwargs.get('joy', Influence())
            self.liking = kwargs.get('liking', Influence())
            self.love = kwargs.get('love', Influence())
            self.pride = kwargs.get('pride', Influence())
            self.relief = kwargs.get('relief', Influence())
            self.satisfaction = kwargs.get('satisfaction', Influence())

            self.anger = kwargs.get('anger', Influence())
            self.disliking = kwargs.get('disliking', Influence())
            self.disappointment = kwargs.get('disappointment', Influence())
            self.distress = kwargs.get('distress', Influence())
            self.fear = kwargs.get('fear', Influence())
            self.fears_confirmed = kwargs.get('fears_confirmed', Influence())
            self.hate = kwargs.get('hate', Influence())
            self.pity = kwargs.get('pity', Influence())
            self.remorse = kwargs.get('remorse', Influence())
            self.reproach = kwargs.get('reproach', Influence())
            self.resentment = kwargs.get('resentment', Influence())
            self.shame = kwargs.get('shame', Influence())

    def occ(self, personality=OCEAN(), value=0):
        _val = self.map_value(value, self.minval, self.maxval)
        admiration = _val * self._get_att_factor(personality, self.admiration)
        gloating = _val * self._get_att_factor(personality, self.gloating)
        gratification = _val * self._get_att_factor(personality, self.gratification)
        gratitude = _val * self._get_att_factor(personality, self.gratitude)
        hope = _val * self._get_att_factor(personality, self.hope)
        happy_for = _val * self._get_att_factor(personality, self.happy_for)
        joy = _val * self._get_att_factor(personality, self.joy)
        liking = _val * self._get_att_factor(personality, self.liking)
        love = _val * self._get_att_factor(personality, self.love)
        pride = _val * self._get_att_factor(personality, self.pride)
        relief = _val * self._get_att_factor(personality, self.relief)
        satisfaction = _val * self._get_att_factor(personality, self.satisfaction)

        anger = _val * self._get_att_factor(personality, self.anger)
        disliking = _val * self._get_att_factor(personality, self.disliking)
        disappointment = _val * self._get_att_factor(personality, self.disappointment)
        distress = _val * self._get_att_factor(personality, self.distress)
        fear = _val * self._get_att_factor(personality, self.fear)
        fears_confirmed = _val * self._get_att_factor(personality, self.fears_confirmed)
        hate = _val * self._get_att_factor(personality, self.hate)
        pity = _val * self._get_att_factor(personality, self.pity)
        remorse = _val * self._get_att_factor(personality, self.remorse)
        reproach = _val * self._get_att_factor(personality, self.reproach)
        resentment = _val * self._get_att_factor(personality, self.resentment)
        shame = _val * self._get_att_factor(personality, self.shame)

        return OCC(admiration, gloating, gratification, gratitude, hope, happy_for, joy, liking, love, pride, relief, satisfaction,
                   anger, disliking, disappointment, distress, fear, fears_confirmed, hate, pity, remorse, reproach, resentment, shame)

    def pad(self, personality=OCEAN(), value=0):
        return self.occ(personality, value).pad

    @staticmethod
    def _get_att_factor(personality=OCEAN(), influence=Influence()):
        openness = Sensor.map_value(personality.openness, 0, influence.openness.relation)
        conscientiousness = Sensor.map_value(personality.conscientiousness, 0, influence.conscientiousness.relation)
        extraversion = Sensor.map_value(personality.extraversion, 0, influence.extraversion.relation)
        agreeableness = Sensor.map_value(personality.agreeableness, 0, influence.agreeableness.relation)
        neuroticism = Sensor.map_value(personality.neuroticism, 0, influence.neuroticism.relation)

        values = [openness, conscientiousness, extraversion, agreeableness, neuroticism]
        weights = [influence.openness.weight,
                   influence.conscientiousness.weight,
                   influence.extraversion.weight,
                   influence.agreeableness.weight,
                   influence.neuroticism.weight]
        return np.average(values, axis=0, weights=weights)

    @staticmethod
    def map_value(value=0.0, in_min=0.0, in_max=1.0, out_min=0.0, out_max=1.0):
        return (float(value) - float(in_min)) * (float(out_max) - float(out_min)) / (
            float(in_max) - float(in_min)) + float(out_min)

    def __repr__(self):
        return '<Sensor #%s: %s>' % (self.id, self.name)
