#!/usr/bin/env python
# leds.py

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.cleanup()
GPIO.setup(7, GPIO.OUT)
GPIO.setup(11, GPIO.OUT)

p1 = GPIO.PWM(7, 50)
p2 = GPIO.PWM(11, 50)
p1.start(7.5)
p1.start(7.5)
while True:
	p1.ChangeDutyCycle(4.5)
	p2.ChangeDutyCycle(4.5)
	time.sleep(0.5)
	p1.ChangeDutyCycle(10.5)
	p2.ChangeDutyCycle(10.5)
	time.sleep(0.5)
	p1.ChangeDutyCycle(7.5)
	p2.ChangeDutyCycle(7.5)
	time.sleep(0.5)
p1.stop()
p2.stop()
GPIO.cleanup()
