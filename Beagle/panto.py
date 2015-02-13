#! /usr/bin/python

from __future__ import division
from numpy import linalg as LA
from time import sleep
import os
import cv2
import sys
import numpy as np
import cPickle
import mgi
import pantolib

TIME_BETWEEN_POINTS = 0.05      # in seconds
TIME_BETWEEN_CONTOURS = 0.5    # in seconds

max_width = 140
max_height = 90
x_trans_factor = 0
y_trans_factor = 0

APP_STATE_INIT = 0
APP_STATE_TAKE_PICTURE = 1
APP_STATE_RESIZE = 2
APP_STATE_FILTER = 3
APP_STATE_CONTOUR = 4
APP_STATE_PRINTING = 5
APP_STATE_DONE = 6
APP_STATE = 0

def nothing(*arg):
    pass

def printContours (contours):

    if len(contours) == 0:
        print "ERROR: NO CONTOUR FOUND !!!"
        print "Please, press n to restart the procedure..."
    else:

        print "Printing ", len(contours), " contours."
        # TODO: We could filter the small contours (with less that 3 points, for instance)
        for c in contours:
            #print c
            print '----------------  contour -------------------'
            if len(c) < 2:
                print "Void contour (contained only one point)"
                continue
            # Lift pen, go to first point of the countour, and start drawing
            pantolib.Down()
            [[ x, y ]] = c[0]
            x_trans = x + x_trans_factor
            y_trans = -y + y_trans_factor
            (q1, q2) = mgi.MGI(x_trans, y_trans)
            print 'x: ', x, 'y:', y, '	--> x-trans: ', x_trans, 'y_trans:', y_trans, '	--> q1: ', q1, 'q2:', q2
            pantolib.GoTo(q1, q2)
            sleep(TIME_BETWEEN_CONTOURS) # Time in seconds.
            pantolib.Up()

            # For the rest of the points of the countour
            c = c[1:]
            for p in c:
                [[ x, y ]] = p
                x_trans = x + x_trans_factor
                y_trans = -y + y_trans_factor
                (q1, q2) = mgi.MGI(x_trans, y_trans)
                print 'x: ', x, 'y:', y, '	--> x-trans: ', x_trans, 'y_trans:', y_trans, '	--> q1: ', q1, 'q2:', q2
                pantolib.GoTo(q1, q2)
                sleep(TIME_BETWEEN_POINTS) # Time in seconds.

        pantolib.Down()
        sleep(TIME_BETWEEN_CONTOURS)

        print "Image successfully printed !!!"


pantolib.Init()
while True:

    if APP_STATE == APP_STATE_INIT:
        img = cv2.imread('welcome.jpg')
        cv2.imshow('welcome', img)
	
        print "WELCOME TO THE PANTOGRAPHE !!!!"
        print "Press n to advance to the next step..."

    elif APP_STATE == APP_STATE_TAKE_PICTURE:
        
        img = cv2.imread('1.jpg')
        cv2.imshow('Picture', img)

        print "Press any key to repeat the picture, n when done."

    elif APP_STATE == APP_STATE_RESIZE:

        print "Loading Original Image..."
        image = cv2.imread('./1.jpg')
        cv2.imshow('original',image)

        print "Resizing image..."
        # we need to keep in mind aspect ratio so the image does
        # not look skewed or distorted -- therefore, we calculate
        # the ratio of the new image to the old image
        r = float(max_width) / image.shape[1]
        dim = (max_width, int(image.shape[0] * r))
        if dim[0] > max_height:
            r = float(max_height) / image.shape[0]
            dim = (int(image.shape[1] * r), max_height)
        # perform the actual resizing of the image and show it
        resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
        cv2.imshow("resized", resized)
        x_trans_factor = -dim[0]/2.
        y_trans_factor = dim[1]/2. + 130

        print "Press n when done."

    elif APP_STATE == APP_STATE_FILTER:

        print "Saving Resized image..."
        cv2.imwrite('resized.jpg',resized)

        print "Loading Image..."
        cv2.namedWindow('edge')
        cv2.createTrackbar('1', 'edge', 2000, 5000, nothing)
        cv2.createTrackbar('2', 'edge', 4000, 5000, nothing)

        img = cv2.imread('resized.jpg')
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        print "Adjust the thresholds..."
        print "Press n when done."

        while True:
            thrs1 = cv2.getTrackbarPos('1', 'edge')
            thrs2 = cv2.getTrackbarPos('2', 'edge')
            edge = cv2.Canny(gray, thrs1, thrs2, apertureSize=5)
            vis = img.copy()
            vis /= 2
            vis[edge != 0] = (0, 255, 0)
            cv2.imshow('edge', vis)
            ch = cv2.waitKey(5)
            if ch == ord('n'):
                break

     

    elif APP_STATE == APP_STATE_CONTOUR:

        print "Saving filtered image..."
        cv2.imwrite('filtered.jpg',vis)

        print "Loading Image..."
        img = cv2.imread('filtered.jpg')
        cv2.imshow('Image', img)

        imgray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        ret,thresh = cv2.threshold(imgray,127,255,0)
        contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

        cv2.drawContours(img, contours, -1, (0,255,0), 3)
        cv2.imshow('Imag+Cont',img)

        width, height, depth = img.shape

        image=np.zeros((width, height, 3),np.uint8) 
        #image = im.copy()
        cv2.drawContours(image, contours, -1, (0,255,0), 3)

        cv2.imshow('Contours',image)

        print "Final IMAGE !"
        print "Press n when done."

    elif APP_STATE == APP_STATE_PRINTING:

        print "Saving contours image..."
        cv2.imwrite('contours.jpg',image)

        print "Loading Contours image..."
        img = cv2.imread('contours.jpg')
        cv2.imshow('Contours', img)

        print "Printing the contours..."

        #contour = np.array([ [[-50, 80]], [[-50, 150]], [[50, 150]], [[50, 80]] ])
        #print contour

        #np.savetxt('contour.txt', contour_example)
        #contour = np.load('contour.txt')

        printContours(contours)

        img = cv2.imread('printed.jpg')
        cv2.imshow('Printed', img)
        print "Printing complete."
        print "Collect your painting and press n to continue..."

        #APP_STATE = APP_STATE + 1

    else:
        img = cv2.imread('printed.jpg')
        cv2.imshow('Printed', img)
        print "Printing complete."
        print "Collect your painting and press n to continue..."

    while True:
        ch = cv2.waitKey(0)
        if ch == ord('n'):
            print "Next state !"
            if APP_STATE < APP_STATE_PRINTING:
                APP_STATE = APP_STATE + 1
            else:
                APP_STATE = APP_STATE_INIT
        if ch == -1:
            continue
        else:
            #print ch
            break
        #print "p1"
        # ESC = 27
    #print "p2"

    cv2.destroyAllWindows()

        

