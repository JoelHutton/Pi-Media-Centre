#!/usr/bin/python

pins = [3,5,7,8,10,11,12,13,15,16,18,19,21,22,23,24,26]

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

for p in pins:
        raw_input("press ENTER to turn on " + str(p))
	GPIO.setup(p, GPIO.OUT)
	time.sleep(0.25)
for p in pins:
        raw_input("press ENTER to turn off " + str(p))
	GPIO.setup(p, GPIO.IN)
	time.sleep(0.25)
