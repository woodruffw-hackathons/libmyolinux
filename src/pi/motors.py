#!/usr/bin/env python
# leds.py

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.cleanup()
GPIO.setup(7, GPIO.OUT)

p = GPIO.PWM(7, 50)
p.start(7.5)
while True:
	p.ChangeDutyCycle(4.5)
	time.sleep(0.5)
	p.ChangeDutyCycle(10.5)
	time.sleep(0.5)
	p.ChangeDutyCycle(7.5)
	time.sleep(0.5)
p.stop()
GPIO.cleanup()
