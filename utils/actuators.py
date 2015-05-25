__author__ = 'mgaldieri'

from pyaffective.emotions import PAD
from scipy.spatial.distance import sqeuclidean
from operator import itemgetter
import numpy as np


class Feature:
    def __init__(self, name='', pad=PAD(), rgb=None):
        if not rgb:
            rgb = []
        self.name = name
        self.pad = pad
        self.rgb = np.array(rgb)


class RGBled:
    def __init__(self, features=[Feature()]*5):
        self.features = features if all([isinstance(f, Feature) for f in features]) else [Feature()]*5
        self.f_vec = [f.pad.state for f in self.features]
        self.rgb_vec = [f.rgb for f in self.features]

    def rgb(self, value=PAD()):
        """
        RGB values for discrete features
        :param value: mood value wrapped in a PAD object
        :return: numpy array containing r, g and b values between 0 and 1
        """
        similarities = np.array([1-sqeuclidean(f, value.state) for f in self.f_vec])
        strongest = max(enumerate(1-similarities/np.linalg.norm(similarities, 1)), key=itemgetter(1))
        return self.rgb_vec[strongest[0]]

    def rgb_alt(self, value=PAD()):
        """
        Averaged RGB values between all measured features
        :param value: mood value wrapped in a PAD object
        :return: numpy array containing r, g and b values between 0 and 1
        """
        similarities = np.array([1-sqeuclidean(f, value.state) for f in self.f_vec])
        weights = 1-similarities/np.linalg.norm(similarities, 1)
        return np.average(self.rgb_vec, axis=0, weights=weights)
