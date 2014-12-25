#!/usr/bin/python
#creates a map of what all the pins attach to 
import RPi.GPIO as GPIO
import time

mapFile = open('pinMap.txt','w')
pins = {} 
GPIO.setmode(GPIO.BOARD)

for i in range(1,27):
    try:
        raw_input("press enter to test pin " + str(i))
        GPIO.setup(i, GPIO.OUT) 
        raw_input("press enter to turn off pin " + str(i))
        GPIO.setup(i, GPIO.IN) 
        used=raw_input("used? y/n:")
        if used == "y" or used =="Y":
            description = raw_input("add description")
            pins[i] = description
    except Exception:
        pass

save=raw_input("write to file? y/n:")
if save == "y" or save =="Y":
    for pin in pins:
        mapFile.write(str(pin) + ":" + str(pins.get(pin)))

mapFile.close()
