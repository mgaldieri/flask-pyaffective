__author__ = 'mgaldieri'

import time

from serial import SerialException
from utils.sensors import Sensor, Influence, InfluenceValue
from utils.actuators import RGBled
import serial
import os

# *****
# CALIBRATION CONSTANTS
# *****
AUDIO_MIN_VAL = 0
AUDIO_MAX_VAL = 255

CAP_MIN_VAL = 0
CAP_MAX_VAL = 255

ACCEL_MIN_VAL = 0
ACCEL_MAX_VAL = 200

# *****
# globals
# *****
BAUD_RATE = 9600
PORT_STRINGS = ['USB', 'ACM']

BYTES_TO_READ = 2

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
                               conscientiousness=Influence(2.0, InfluenceValue.DIRECT),
                               extraversion=Influence(2.0, InfluenceValue.INVERSE),
                               agreeableness=Influence(1.2, InfluenceValue.INVERSE),
                               neuroticism=Influence(2.0, InfluenceValue.DIRECT))
audio_sensor.fear = Influence(openness=InfluenceValue(1.5, InfluenceValue.DIRECT),
                              conscientiousness=Influence(2.0, InfluenceValue.DIRECT),
                              extraversion=Influence(1.2, InfluenceValue.DIRECT),
                              agreeableness=Influence(1.5, InfluenceValue.DIRECT),
                              neuroticism=Influence(2.0, InfluenceValue.DIRECT))
audio_sensor.joy = Influence(openness=InfluenceValue(2.0, InfluenceValue.DIRECT),
                             conscientiousness=Influence(1.5, InfluenceValue.INVERSE),
                             extraversion=Influence(1.5, InfluenceValue.DIRECT),
                             agreeableness=Influence(1.0, InfluenceValue.DIRECT),
                             neuroticism=Influence(1.5, InfluenceValue.INVERSE))
audio_sensor.love = Influence(openness=InfluenceValue(1.2, InfluenceValue.INVERSE),
                              conscientiousness=Influence(2.0, InfluenceValue.INVERSE),
                              extraversion=Influence(1.0, InfluenceValue.DIRECT),
                              agreeableness=Influence(1.2, InfluenceValue.INVERSE),
                              neuroticism=Influence(2.0, InfluenceValue.INVERSE))
audio_sensor.distress = Influence(openness=InfluenceValue(1.2, InfluenceValue.DIRECT),
                                  conscientiousness=Influence(2.0, InfluenceValue.DIRECT),
                                  extraversion=Influence(1.2, InfluenceValue.DIRECT),
                                  agreeableness=Influence(1.2, InfluenceValue.DIRECT),
                                  neuroticism=Influence(1.5, InfluenceValue.DIRECT))

# capacitance sensor
cap_sensor = Sensor(2, 'Proximity sensor', CAP_MIN_VAL, CAP_MAX_VAL)
# set inflences of this sensor in perceiving emotional events for each personality trait that matters
cap_sensor.anger = Influence(openness=InfluenceValue(1.5, InfluenceValue.INVERSE),
                             conscientiousness=Influence(2.0, InfluenceValue.DIRECT),
                             extraversion=Influence(2.0, InfluenceValue.INVERSE),
                             agreeableness=Influence(1.2, InfluenceValue.INVERSE),
                             neuroticism=Influence(1.5, InfluenceValue.DIRECT))
cap_sensor.fear = Influence(openness=InfluenceValue(1.5, InfluenceValue.INVERSE),
                            conscientiousness=Influence(2.0, InfluenceValue.DIRECT),
                            extraversion=Influence(1.5, InfluenceValue.INVERSE),
                            agreeableness=Influence(1.2, InfluenceValue.DIRECT),
                            neuroticism=Influence(2.0, InfluenceValue.DIRECT))
cap_sensor.joy = Influence(openness=InfluenceValue(1.5, InfluenceValue.DIRECT),
                           conscientiousness=Influence(1.5, InfluenceValue.INVERSE),
                           extraversion=Influence(2.0, InfluenceValue.DIRECT),
                           agreeableness=Influence(1.2, InfluenceValue.DIRECT),
                           neuroticism=Influence(1.5, InfluenceValue.INVERSE))
cap_sensor.love = Influence(openness=InfluenceValue(1.2, InfluenceValue.DIRECT),
                            conscientiousness=Influence(1.2, InfluenceValue.DIRECT),
                            extraversion=Influence(1.7, InfluenceValue.DIRECT),
                            agreeableness=Influence(1.2, InfluenceValue.DIRECT),
                            neuroticism=Influence(1.7, InfluenceValue.INVERSE))
cap_sensor.distress = Influence(openness=InfluenceValue(1.0, InfluenceValue.DIRECT),
                                conscientiousness=Influence(2.0, InfluenceValue.DIRECT),
                                extraversion=Influence(2.0, InfluenceValue.INVERSE),
                                agreeableness=Influence(1.0, InfluenceValue.DIRECT),
                                neuroticism=Influence(1.2, InfluenceValue.DIRECT))

# accelerometer sensor
accel_sensor = Sensor(3, 'Accelerometer sensor', ACCEL_MIN_VAL, ACCEL_MAX_VAL)
# set inflences of this sensor in perceiving emotional events for each personality trait that matters
accel_sensor.anger = Influence(openness=InfluenceValue(1.2, InfluenceValue.DIRECT),
                               conscientiousness=Influence(2.0, InfluenceValue.DIRECT),
                               extraversion=Influence(2.0, InfluenceValue.INVERSE),
                               agreeableness=Influence(1.2, InfluenceValue.DIRECT),
                               neuroticism=Influence(1.5, InfluenceValue.DIRECT))
accel_sensor.fear = Influence(openness=InfluenceValue(1.0, InfluenceValue.DIRECT),
                              conscientiousness=Influence(2.0, InfluenceValue.DIRECT),
                              extraversion=Influence(1.5, InfluenceValue.INVERSE),
                              agreeableness=Influence(1.2, InfluenceValue.DIRECT),
                              neuroticism=Influence(2.0, InfluenceValue.DIRECT))
accel_sensor.joy = Influence(openness=InfluenceValue(1.2, InfluenceValue.DIRECT),
                             conscientiousness=Influence(1.5, InfluenceValue.INVERSE),
                             extraversion=Influence(2.0, InfluenceValue.DIRECT),
                             agreeableness=Influence(1.2, InfluenceValue.DIRECT),
                             neuroticism=Influence(1.5, InfluenceValue.INVERSE))
accel_sensor.love = Influence(openness=InfluenceValue(1.2, InfluenceValue.INVERSE),
                              conscientiousness=Influence(1.7, InfluenceValue.INVERSE),
                              extraversion=Influence(1.7, InfluenceValue.DIRECT),
                              agreeableness=Influence(1.0, InfluenceValue.DIRECT),
                              neuroticism=Influence(1.7, InfluenceValue.INVERSE))
accel_sensor.distress = Influence(openness=InfluenceValue(1.2, InfluenceValue.DIRECT),
                                  conscientiousness=Influence(2.0, InfluenceValue.DIRECT),
                                  extraversion=Influence(2.0, InfluenceValue.INVERSE),
                                  agreeableness=Influence(1.2, InfluenceValue.DIRECT),
                                  neuroticism=Influence(1.5, InfluenceValue.DIRECT))

# *****
# run loop
# *****
while True:
    try:
        data = server.read(BYTES_TO_READ)
        if data:
            value = ord(data[0]) << 8
            value |= ord(data[1])
            print value
    except SerialException:
        pass