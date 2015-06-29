__author__ = 'mgaldieri'

import time

from serial import SerialException
from pyaffective.emotions import OCEAN, PAD
from utils.sensors import Sensor, Influence, InfluenceValue
from utils.actuators import Feature, RGBled
from socketIO_client import SocketIO, BaseNamespace
import Queue
import logging
import serial
import os

# logging.basicConfig(level=logging.DEBUG)

# *****
# CALIBRATION CONSTANTS
# *****
AUDIO_MIN_VAL = 0
AUDIO_MAX_VAL = 255

CAP_MIN_VAL = 0
CAP_MAX_VAL = 255

ACCEL_MIN_VAL = 0
ACCEL_MAX_VAL = 255

# *****
# globals
# *****
BAUD_RATE = 9600
PORT_STRINGS = ['USB', 'ACM']

BYTES_TO_READ = 3

# *****
# arduino connection
# *****
port = '/dev/'

# try to find a connected arduino port
for fn in os.listdir('/dev'):
    for s in PORT_STRINGS:
        if s in fn:
            port += fn

# connect to arduino
print('Trying to connect to arduino at port %s...' % port)
server = serial.Serial(port, BAUD_RATE)

# wait for arduino auto reset on connect
time.sleep(2)

# *****
# init sensors
# *****

# audio
audio_sensor = Sensor(1, 'Audio sensor', AUDIO_MIN_VAL, AUDIO_MAX_VAL)
# set inflences of this sensor in perceiving emotional events for each personality trait that matters
audio_sensor.anger = Influence(openness=InfluenceValue(1.2, InfluenceValue.INVERSE),
                               conscientiousness=InfluenceValue(2.0, InfluenceValue.DIRECT),
                               extraversion=InfluenceValue(2.0, InfluenceValue.INVERSE),
                               agreeableness=InfluenceValue(1.2, InfluenceValue.INVERSE),
                               neuroticism=InfluenceValue(2.0, InfluenceValue.DIRECT))
audio_sensor.fear = Influence(openness=InfluenceValue(1.5, InfluenceValue.DIRECT),
                              conscientiousness=InfluenceValue(2.0, InfluenceValue.DIRECT),
                              extraversion=InfluenceValue(1.2, InfluenceValue.DIRECT),
                              agreeableness=InfluenceValue(1.5, InfluenceValue.DIRECT),
                              neuroticism=InfluenceValue(2.0, InfluenceValue.DIRECT))
audio_sensor.joy = Influence(openness=InfluenceValue(2.0, InfluenceValue.DIRECT),
                             conscientiousness=InfluenceValue(1.5, InfluenceValue.INVERSE),
                             extraversion=InfluenceValue(1.5, InfluenceValue.DIRECT),
                             agreeableness=InfluenceValue(1.0, InfluenceValue.DIRECT),
                             neuroticism=InfluenceValue(1.5, InfluenceValue.INVERSE))
audio_sensor.love = Influence(openness=InfluenceValue(1.2, InfluenceValue.INVERSE),
                              conscientiousness=InfluenceValue(2.0, InfluenceValue.INVERSE),
                              extraversion=InfluenceValue(1.0, InfluenceValue.DIRECT),
                              agreeableness=InfluenceValue(1.2, InfluenceValue.INVERSE),
                              neuroticism=InfluenceValue(2.0, InfluenceValue.INVERSE))
audio_sensor.distress = Influence(openness=InfluenceValue(1.2, InfluenceValue.DIRECT),
                                  conscientiousness=InfluenceValue(2.0, InfluenceValue.DIRECT),
                                  extraversion=InfluenceValue(1.2, InfluenceValue.DIRECT),
                                  agreeableness=InfluenceValue(1.2, InfluenceValue.DIRECT),
                                  neuroticism=InfluenceValue(1.5, InfluenceValue.DIRECT))

# capacitance sensor
cap_sensor = Sensor(2, 'Proximity sensor', CAP_MIN_VAL, CAP_MAX_VAL)
# set inflences of this sensor in perceiving emotional events for each personality trait that matters
cap_sensor.anger = Influence(openness=InfluenceValue(1.5, InfluenceValue.INVERSE),
                             conscientiousness=InfluenceValue(2.0, InfluenceValue.DIRECT),
                             extraversion=InfluenceValue(2.0, InfluenceValue.INVERSE),
                             agreeableness=InfluenceValue(1.2, InfluenceValue.INVERSE),
                             neuroticism=InfluenceValue(1.5, InfluenceValue.DIRECT))
cap_sensor.fear = Influence(openness=InfluenceValue(1.5, InfluenceValue.INVERSE),
                            conscientiousness=InfluenceValue(2.0, InfluenceValue.DIRECT),
                            extraversion=InfluenceValue(1.5, InfluenceValue.INVERSE),
                            agreeableness=InfluenceValue(1.2, InfluenceValue.DIRECT),
                            neuroticism=InfluenceValue(2.0, InfluenceValue.DIRECT))
cap_sensor.joy = Influence(openness=InfluenceValue(1.5, InfluenceValue.DIRECT),
                           conscientiousness=InfluenceValue(1.5, InfluenceValue.INVERSE),
                           extraversion=InfluenceValue(2.0, InfluenceValue.DIRECT),
                           agreeableness=InfluenceValue(1.2, InfluenceValue.DIRECT),
                           neuroticism=InfluenceValue(1.5, InfluenceValue.INVERSE))
cap_sensor.love = Influence(openness=InfluenceValue(1.2, InfluenceValue.DIRECT),
                            conscientiousness=InfluenceValue(1.2, InfluenceValue.DIRECT),
                            extraversion=InfluenceValue(1.7, InfluenceValue.DIRECT),
                            agreeableness=InfluenceValue(1.2, InfluenceValue.DIRECT),
                            neuroticism=InfluenceValue(1.7, InfluenceValue.INVERSE))
cap_sensor.distress = Influence(openness=InfluenceValue(1.0, InfluenceValue.DIRECT),
                                conscientiousness=InfluenceValue(2.0, InfluenceValue.DIRECT),
                                extraversion=InfluenceValue(2.0, InfluenceValue.INVERSE),
                                agreeableness=InfluenceValue(1.0, InfluenceValue.DIRECT),
                                neuroticism=InfluenceValue(1.2, InfluenceValue.DIRECT))

# accelerometer sensor
accel_sensor = Sensor(3, 'Accelerometer sensor', ACCEL_MIN_VAL, ACCEL_MAX_VAL)
# set inflences of this sensor in perceiving emotional events for each personality trait that matters
accel_sensor.anger = Influence(openness=InfluenceValue(1.2, InfluenceValue.DIRECT),
                               conscientiousness=InfluenceValue(2.0, InfluenceValue.DIRECT),
                               extraversion=InfluenceValue(2.0, InfluenceValue.INVERSE),
                               agreeableness=InfluenceValue(1.2, InfluenceValue.DIRECT),
                               neuroticism=InfluenceValue(1.5, InfluenceValue.DIRECT))
accel_sensor.fear = Influence(openness=InfluenceValue(1.0, InfluenceValue.DIRECT),
                              conscientiousness=InfluenceValue(2.0, InfluenceValue.DIRECT),
                              extraversion=InfluenceValue(1.5, InfluenceValue.INVERSE),
                              agreeableness=InfluenceValue(1.2, InfluenceValue.DIRECT),
                              neuroticism=InfluenceValue(2.0, InfluenceValue.DIRECT))
accel_sensor.joy = Influence(openness=InfluenceValue(1.2, InfluenceValue.DIRECT),
                             conscientiousness=InfluenceValue(1.5, InfluenceValue.INVERSE),
                             extraversion=InfluenceValue(2.0, InfluenceValue.DIRECT),
                             agreeableness=InfluenceValue(1.2, InfluenceValue.DIRECT),
                             neuroticism=InfluenceValue(1.5, InfluenceValue.INVERSE))
accel_sensor.love = Influence(openness=InfluenceValue(1.2, InfluenceValue.INVERSE),
                              conscientiousness=InfluenceValue(1.7, InfluenceValue.INVERSE),
                              extraversion=InfluenceValue(1.7, InfluenceValue.DIRECT),
                              agreeableness=InfluenceValue(1.0, InfluenceValue.DIRECT),
                              neuroticism=InfluenceValue(1.7, InfluenceValue.INVERSE))
accel_sensor.distress = Influence(openness=InfluenceValue(1.2, InfluenceValue.DIRECT),
                                  conscientiousness=InfluenceValue(2.0, InfluenceValue.DIRECT),
                                  extraversion=InfluenceValue(2.0, InfluenceValue.INVERSE),
                                  agreeableness=InfluenceValue(1.2, InfluenceValue.DIRECT),
                                  neuroticism=InfluenceValue(1.5, InfluenceValue.DIRECT))

# *****
# init actuators
# *****

# values obtained empirically
anger_feature = Feature('anger', PAD(pleasure=-0.51, arousal=0.59, dominance=0.25), rgb=[255, 0, 0])
fear_feature = Feature('fear', PAD(pleasure=-0.64, arousal=0.6, dominance=-0.43), rgb=[0, 13, 148])
joy_feature = Feature('joy', PAD(pleasure=0.4, arousal=0.2, dominance=0.1), rgb=[255, 150, 0])
love_feature = Feature('love', PAD(pleasure=0.3, arousal=0.1, dominance=0.2), rgb=[255, 0, 80])
distress_feature = Feature('distress', PAD(pleasure=-0.4, arousal=-0.2, dominance=-0.5), rgb=[51, 58, 59])

rgb = RGBled([anger_feature, fear_feature, joy_feature, love_feature, distress_feature])

# keep track of current personality
personality = OCEAN()

# provide a thread-safe double ended queue for communicating mood between websocket and serial comm
mood_queue = Queue.Queue(maxsize=1)

# *****
# websocket
# *****
class SocketNamespace(BaseNamespace):
    def on_connected_response(self, *args):
        print 'Connected to websocket'

    def on_mood_updated_response(self, *args):
        pad = [args[0].get('p'), args[0].get('a'), args[0].get('d')]
        print 'PUT: ', pad
        try:
            mood_queue.put_nowait(pad)
        except Queue.Full:
            with mood_queue.mutex:
                mood_queue.queue.clear()
            mood_queue.put_nowait(pad)

    def on_ocean_updated(self, *args):
        personality.openness = args[0].get('openness')
        personality.conscientiousness = args[0].get('conscientiousness')
        personality.extraversion = args[0].get('extraversion')
        personality.agreeableness = args[0].get('agreeableness')
        personality.neuroticism = args[0].get('neuroticism')
        print 'Personality updated'

# connect to websocket server
socket = SocketIO('127.0.0.1', 5000)
socket_namespace = socket.define(SocketNamespace, '/socket')

# define event callbacks
socket_namespace.on('connected', socket_namespace.on_connected_response)
socket_namespace.on('mood_updated', socket_namespace.on_mood_updated_response)
socket_namespace.on('ocean_updated', socket_namespace.on_ocean_updated)

# *****
# run loop
# *****
while True:
    try:
        socket.wait(seconds=0.1)
        data = server.read(BYTES_TO_READ)
        if data:
            # put data into sensor class to calculate its occ value
            audio_occ = audio_sensor.occ(personality, ord(data[0]))
            cap_occ = cap_sensor.occ(personality, ord(data[1]))
            accel_occ = accel_sensor.occ(personality, ord(data[2]))

            # send data collected from arduino to affective server via websocket
            socket_namespace.emit('occ', dict(audio_occ))
            socket_namespace.emit('occ', dict(cap_occ))
            socket_namespace.emit('occ', dict(accel_occ))

            # send signal to retrieve current mood
            socket_namespace.emit('mood_get')

            # extract it from mood queue and send it to arduino
            try:
                pad = mood_queue.get_nowait()
                rgb_val = rgb.rgb(PAD(pleasure=pad[0], arousal=pad[1], dominance=pad[2]))
                print 'GET: ', pad
                server.write(rgb_val)
            except Queue.Empty:
                # carry on
                pass

        # take a nap
        time.sleep(0.5)
    except SerialException:
        # fail silently...
        pass
