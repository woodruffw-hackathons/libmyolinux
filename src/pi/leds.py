#!/usr/bin/env python
# leds.py

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.cleanup()
GPIO.setup(7, GPIO.OUT)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(12, GPIO.OUT)
GPIO.output(7, GPIO.HIGH)
GPIO.output(11, GPIO.HIGH)
GPIO.output(12, GPIO.HIGH)

GPIO.cleanup()