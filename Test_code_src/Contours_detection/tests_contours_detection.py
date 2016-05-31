#! /usr/bin/python

from __future__ import division
from numpy import linalg as LA
from time import sleep
import os
import cv2
import sys
import numpy as np
import cPickle

STATE_ACQUIRE = 0
STATE_PROCESS = 1
STATE_DISPLAY = 2
STATE = STATE_ACQUIRE

def nothing(*arg):
    pass

cam = cv2.VideoCapture(0)
cam.set(cv2.cv.CV_CAP_PROP_FOURCC, cv2.cv.CV_FOURCC('Y', 'U', 'Y', 'V') );
cam.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 320)
cam.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 240)

cv2.namedWindow('Edges')
cv2.createTrackbar('1', 'Edges', 2000, 5000, nothing)
cv2.createTrackbar('2', 'Edges', 4000, 5000, nothing)

#face_cascade = cv2.CascadeClassifier('/usr/share/opencv/haarcascades/haarcascade_frontalface_default.xml')

'''
input_file = raw_input('Specify file to proceed: ')
input_file = './' + input_file
img = cv2.imread(input_file)
'''

while True:
	if STATE == STATE_ACQUIRE:
		ret, img = cam.read()

	elif STATE == STATE_PROCESS:
		'''
		gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)	
		faces = face_cascade.detectMultiScale(gray,1.05,2)
		print len(faces), ' faces detected...'
		for (x,y,w,h) in faces:
			cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
		'''

		STATE = STATE_DISPLAY

	thrs1 = cv2.getTrackbarPos('1', 'Edges')
        thrs2 = cv2.getTrackbarPos('2', 'Edges')

	gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	equalized = cv2.equalizeHist(gray)

	canny_out = cv2.Canny(equalized, thrs1, thrs2, apertureSize=5, L2gradient=False)
	displayed = img.copy()
	displayed /= 2
        displayed[canny_out != 0] = (0, 255, 0)

	cv2.imshow('Edges', displayed)
	cv2.imshow('5', canny_out)

	canny_out = cv2.Canny(equalized, thrs1, thrs2, apertureSize=3, L2gradient=False)
	cv2.imshow('3', canny_out)

	ch = cv2.waitKey(10)
	if ch == ord('n'):
		if STATE == STATE_ACQUIRE:
			STATE = STATE_PROCESS
		elif STATE == STATE_DISPLAY:
			STATE = STATE_ACQUIRE
	if ch == ord('q'):
		break
