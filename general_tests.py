__author__ = 'mgaldieri'

from pyaffective.agent import Agent
from time import sleep

agent = Agent()
agent.start()

sleep(5)

agent.stop()

sleep(2)

# def test(*args):
#     # args = args.append(3)
#     print args
#
# test(1, 2)
