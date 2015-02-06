#! /usr/bin/python

import os
import cv2
import RPi.GPIO as GPIO
import time 


pin = 25
frequency = 50

GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.OUT)

p = GPIO.PWM(pin, frequency)
p.start(0)

try:
   while 1:
      for dc in range(10, 20, 1):
         p.ChangeDutyCycle(dc)
         time.sleep(0.1)
      for dc in range(20, 10, -1):
         p.ChangeDutyCycle(dc)
         time.sleep(0.1)

except KeybardInterrupt:
   pass

p.stop()
GPIO.cleanup()


