#!/usr/bin/env python
# leds.py

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.cleanup()
GPIO.setup(7, GPIO.OUT)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(12, GPIO.OUT)

while True:
	GPIO.output(7, GPIO.HIGH)
	sleep(1000)
	GPIO.output(11, GPIO.HIGH)
	sleep(1000)
	GPIO.output(12, GPIO.HIGH)
	sleep(1000)

GPIO.cleanup()