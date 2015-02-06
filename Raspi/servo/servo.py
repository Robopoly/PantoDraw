#! /usr/bin/python

import os
import cv2
import RPi.GPIO as GPIO
import time 


pin = 25
frequency = 100

GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.OUT)

p = GPIO.PWM(pin, frequency)
p.start(0)

try:
   while 1:
      for dc in range(7, 23, 1):
         p.ChangeDutyCycle(dc)
         time.sleep(5)
      for dc in range(23, 7, -1):
         p.ChangeDutyCycle(dc)
         time.sleep(5)

except KeyboardInterrupt:
   pass

p.stop()
GPIO.cleanup()


