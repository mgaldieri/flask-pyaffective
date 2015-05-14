__author__ = 'mgaldieri'

from pyaffective.agent import Agent
from time import sleep

agent = Agent()
agent.start()

for i in range(5):
    sleep(1)
    print i+1

agent.stop()

for i in range(2):
    sleep(1)
    print i+1

# def test(*args):
#     # args = args.append(3)
#     print args
#
# test(1, 2)
