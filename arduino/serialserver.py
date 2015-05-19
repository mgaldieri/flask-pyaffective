__author__ = 'mgaldieri'

import time

from serial import SerialException
import serial
import os

BAUD_RATE = 9600
PORT_STRINGS = ['USB', 'ACM']

BYTES_TO_READ = 2

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

# run loop
while True:
    try:
        data = server.read(BYTES_TO_READ)
        if data:
            value = ord(data[0]) << 8
            value |= ord(data[1])
            print value
    except SerialException:
        pass