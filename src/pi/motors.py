#!/usr/bin/env python
# leds.py

import RPi.GPIO as GPIO
import time
import socket
import struct
import sys

POSES = {
0 : "rest",
1 : "fist",
2 : "waveIn",
3 : "waveOut",
4 : "fingersSpread",
5 : "reserved1",
6 : "thumbToPinky",
}

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind('', sys.argv[1])
server.listen(1)
conn, addr = server.accept()

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.cleanup()
GPIO.setup(7, GPIO.OUT)
GPIO.setup(11, GPIO.OUT)

p1 = GPIO.PWM(7, 50)
p2 = GPIO.PWM(11, 50)
p1.start(0)
p2.start(0)
try:
	while True:
	    data = struct.unpack("ffffffBB", conn.recv(30))
		motion = POSES.get(data[7], 'unknown')
   		if not data: break
		if motion == "fingersSpread"
		    p1.ChangeDutyCycle(75)
		    p2.ChangeDutyCycle(75)
		    time.sleep(2)
		p1.ChangeDutyCycle(0)
 		p2.ChangeDutyCycle(0)
		time.sleep(.5)
except KeyboardInterrupt: 
	p1.stop()
	p2.stop()
	conn.close()
	server.close()
	GPIO.cleanup()

conn.close()
server.close()
p1.stop()
p2.stop()
GPIO.cleanup()
