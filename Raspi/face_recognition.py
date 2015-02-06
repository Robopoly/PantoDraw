#! /usr/bin/python

# This example shows the simplest way of getting an image from the raspi's camera. The # #Face detection, using CascadeClassifiers
# image: is an OpenCV image so we also show how to perform edge detection on the image

import numpy as np

import time
import argparse
import cv2
import py_websockets_bot

#---------------------------------------------------------------------------------------------------        
if __name__ == "__main__":

    print 'Pablo begin!'

    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
    eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

    img = cv2.imread('images/abba.png')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags = cv2.cv.CV_HAAR_SCALE_IMAGE
    )

    print "Found {0} faces!".format(len(faces))

    for (x,y,w,h) in faces:
        print 'face!'
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex,ey,ew,eh) in eyes:
            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
            print 'eye!'

    # Display the image
    cv2.imshow('img',img)

    print 'Pablo end!'

    # Wait for the user to press a key
    cv2.waitKey( 0 )

