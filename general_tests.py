__author__ = 'mgaldieri'

from scipy.spatial.distance import cosine
from scipy.spatial import distance
import numpy as np

# agent = Agent()
# agent.start()
#
# for i in range(5):
#     sleep(1)
#     print i+1
#
# agent.stop()
#
# for i in range(2):
#     sleep(1)
#     print i+1

# def test(*args):
#     # args = args.append(3)
#     print args
#
# test(1, 2)

features = [np.array([0.1, 0.3, 0.2]),
            np.array([0.3, 0.7, 0.6]),
            np.array([0.2, 0.4, 0.7]),
            np.array([-0.4, -0.7, -0.9]),
            np.array([0.3, 0.6, 0.1])]

b = np.array([0.2, 0.4, 0.7])


# print np.array(c)/np.linalg.norm(c, 1)

# print max(enumerate([1-cosine(x, b) for x in a]))

scores = np.array([distance.sqeuclidean(x, b) for x in features])
print 1-(scores/np.linalg.norm(scores, 1))
#
# print np.array([1, 1, 1, 1]) * np.array([1, 2, 3, 4])

# rgbs = np.array([np.array([0.3, 0.5, 0.7]), np.array([0.1, 0.7, 0.7]), np.array([0.9, 0.3, 0.2]), np.array([0.2, 0.9, 0.1])])
# weights = np.array([0.0, 1.0, 0.0, 0.0])
#
# print np.average(rgbs, axis=0, weights=weights)
