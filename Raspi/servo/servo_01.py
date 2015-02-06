#! /usr/bin/python

import os
import cv2
import RPi.GPIO as GPIO
import time 


pin = 25
frequency = 50

GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin, GPIO.OUT)

p = GPIO.PWM(pin, frequency)
p.start(0)

try:
   while 1:
      for dc in range(0, 101, 5):
         p.ChangeDutyCycle(dc)
         time.sleep(0.1)
      for dc in range(100, -1, -5):
         p.ChangeDutyCycle(dc)
         time.sleep(0.1)

except KeybardInterrupt:
   pass

p.stop()
GPIO.cleanup()


