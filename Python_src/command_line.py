###############################################################################
# Copyright (c) 2016, Robopoly Development Team
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
# may be used to endorse or promote products derived from this software without
# specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
##############################################################################

#######################################################################################
#
# Title:       PantoDraw Project
# File:        command_line.py
# Date:        2016-05-31
# Authors:     Jean-Luc Liardon, Marco Pagnamenta,
#              Pablo Garcia del Valle, Paul-Edouard Sarlin
# Website:     https://github.com/Robopoly/PantoDraw
#
# Description: *DEPRECATED* Command line script to use in replacement of main.py and the GUI
#              interface.
#
#######################################################################################

from __future__ import division
from numpy import linalg as LA
from time import sleep
import os
import cv2
import sys
import numpy as np
import cPickle
import mgi
import config
if config.PLATFORM == 'BEAGLE': 
    import pantolib_stepper as pantolib
else:
    import pantolib_dummy as pantolib

TIME_BETWEEN_POINTS = 0.005      # in seconds
TIME_BETWEEN_CONTOURS = 0.3    # in seconds
COLORS = [[0,0,255],[0,255,0],[255,0,0],[200,200,50],[0,255,255],[0,128,255]]
MAP_COLOR = 150
X_OFFSET = 0
Y_OFFSET = 10

contours = []
max_width = 150
max_height = 70
x_trans_factor = 0
y_trans_factor = 0

APP_STATE_INIT = 0
APP_STATE_TAKE_PICTURE = 1
APP_STATE_RESIZE = 2
APP_STATE_FILTER = 3
APP_STATE_CONTOUR = 4
APP_STATE_PRINTING = 5
APP_STATE_DONE = 6
APP_STATE_QUIT = 7
APP_STATE = 0

def nothing(*arg):
    pass

def drawPoint(x, y, r):

    x_resize = int(x*r)
    y_resize =  int(y*r)
    print 'x: ', x, 'y:', y, '	--> int(x*r): ', x_resize, ' int(y*r):', y_resize
    x_trans = x_resize + x_trans_factor + X_OFFSET
    y_trans = -y_resize + y_trans_factor + Y_OFFSET
    (q1, q2) = mgi.MGI(x_trans, y_trans)
    print 'x: ', x_resize, 'y:', y_resize, '	--> x-trans: ', x_trans, 'y_trans:', y_trans, '	--> q1: ', q1, 'q2:', q2
    pantolib.GoTo(q1, q2)


def printContours (contours, r):

    if len(contours) == 0:
        print "ERROR: NO CONTOUR FOUND !!!"
        print "Please, press n to restart the procedure..."
    else:

        print "Printing ", len(contours), " contours."

        for c in contours:

            print '----------------  contour -------------------'
            if len(c) < 2:
                print "Void contour (contained only one point)"
                continue
            elif len(c) < 4:
		print "Filtered point"
		continue

            # Lift pen, go to first point of the countour, and start drawing
            pantolib.Down()
            [ x, y ] = c[0]
            drawPoint(x, y, r)
            sleep(TIME_BETWEEN_CONTOURS)
            pantolib.Up()
            sleep(TIME_BETWEEN_POINTS)

            c = c[1:]

            for p in c:
                [ x, y ] = p
		drawPoint(x, y, r)
		sleep(TIME_BETWEEN_POINTS)

            pantolib.Down()
            sleep(TIME_BETWEEN_CONTOURS)

        print "Image successfully printed !!!"


def follow_contour(x, y, map, img):

	map[y, x] = MAP_COLOR
	new_contour = [[x, y]]
	#print "-----> New contour at ", [x, y]

	while(True):
		s = np.array([[x-1,y-1],[x,y-1],[x+1,y-1],[x-1,y],[x+1,y],[x-1,y+1],[x,y+1],[x+1,y+1]])
		# Create maks for surrounding points
		img_mask = []
		map_mask = []
		for k in s:
			img_mask.append(img[k[1], k[0]])
			map_mask.append(map[k[1], k[0]])
		result = np.logical_and(img_mask, np.logical_not(map_mask))
		next = np.nonzero(result)[0] #usually returns a tuple of arrays
	
		if len(next) == 0:
			#print "End of contour"
			break

		 # First report every surrounding point on the map
		for k in next:
			[u, v] = s[k]
			map[v, u] = MAP_COLOR

		if len(next) > 1:
			change = -len(contours)
			for k in next:
				[u, v] = s[k]
				follow_contour(u, v, map, img)
			change += len(contours)
			if change > 0: # if the last new_contours were long enough to be used
				new_contour.extend(contours[0])
				del contours[0]
			break
		else:
			# Continue the actual contour
			next = next[0]
			[x, y] = s[next]
			new_contour.append([x, y])

	if len(new_contour) > 1: # Filter one-point contours
		#contours.append(new_contour)
		contours.insert(0,new_contour)


def compute_path(img):
	# Convert Canny image from 3 to 1 channels
	img = cv2.copyMakeBorder(img,1,1,1,1,cv2.BORDER_CONSTANT,value=(0,0,0))
	img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	retval, img = cv2.threshold(img,100,255,cv2.THRESH_BINARY)

	width, height = img.shape
	map = img.copy()
	map[:,:] = 0

	for j in range(1, width-1):
		for i in range(1, height-1):
		
			# When accessing img as numpy arrays, x and y are inverted
			if not img[j,i] or map[j,i]:
				continue
		
			[x, y] = [i, j]
			follow_contour(x, y, map, img)

	# Merge coinciding contours
	for index_i, i in enumerate(contours):
		[x, y] = i[0]
		for index_j, j in enumerate(contours):
			if index_i != index_j:
				[u, v] = j[0]
				if np.absolute(u-x)<2 and np.absolute(v-y)<2:
					contours[index_i][:0] = list(reversed(contours[index_j]))
					del contours[index_j]
					break

	print len(contours), ' contours found'
	return map

def export_contours(contours):
	
	file = open("saved_contours.txt", "w")
	np.savetxt(file, contours, delimiter=" ", fmt="%s")
	file.close()

pantolib.Init()
#pantolib.LaunchCalib()

cam = cv2.VideoCapture(-1)

# Set camera resolution. The max resolution is webcam dependent
# so change it to a resolution that is both supported by your camera
# and compatible with your monitor
cam.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 320)
cam.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 240)

print "Camera Properties:"
print "\t Width: ",cam.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)
print "\t Height: ",cam.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)

while True:

    if APP_STATE == APP_STATE_INIT:
        img = cv2.imread('graphical_ressources/welcome.jpg')
        cv2.imshow('welcome', img)
	
        print "WELCOME TO THE PANTOGRAPHE !!!!"
        print "Press n to advance to the next step..."

    elif APP_STATE == APP_STATE_TAKE_PICTURE:

        cv2.destroyAllWindows()

        if config.PLATFORM == 'BEAGLE':
	    '''
            for i in range (1,10):
                ret, img = cam.read()
            ret, img = cam.read()
            cv2.imshow('Photo', img)
	    '''
#                if cv2.waitKey(1) == 27:
#                    break
            img = cv2.imread('test6.jpg')
            cv2.imshow('Test', img)
            print "Press any key to repeat the picture, n when done."

    elif APP_STATE == APP_STATE_RESIZE:

        cv2.imwrite('1.jpg', img)
                        
        cv2.destroyAllWindows()

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

	print "x_trans= ", x_trans_factor
	print "y_trans= ", y_trans_factor
	print r

        print "Press n when done."

    elif APP_STATE == APP_STATE_FILTER:

        print "Saving Resized image..."
        cv2.imwrite('resized.jpg',resized)

        print "Loading Image..."
        cv2.namedWindow('Edges')
        cv2.createTrackbar('1', 'Edges', 2000, 5000, nothing)
        cv2.createTrackbar('2', 'Edges', 4000, 5000, nothing)

        img = cv2.imread('1.jpg')
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        print "Adjust the thresholds..."
        print "Press n when done."

        while True:
            thrs1 = cv2.getTrackbarPos('1', 'Edges')
            thrs2 = cv2.getTrackbarPos('2', 'Edges')
            canny_out = cv2.Canny(gray, thrs1, thrs2, apertureSize=5, L2gradient=False)
            vis = img.copy()
            vis /= 2
            vis[canny_out != 0] = (0, 255, 0)
            cv2.imshow('Edges', vis)
            ch = cv2.waitKey(50)
            if ch == ord('n'):
                break



    elif APP_STATE == APP_STATE_CONTOUR:
	
        print "Saving filtered image..."
        cv2.imwrite('filtered.jpg',canny_out)
	
        print "Loading Image..."
	original = cv2.imread('1.jpg')
	cv2.imshow('Original', original)
	
        canny_out = cv2.imread('filtered.jpg')
        cv2.imshow('Filtered', canny_out)

	print "Computing path... this may take some time"
	contours = []
	map = compute_path(canny_out)
	#export_contours(contours)

	map = cv2.cvtColor(map, cv2.COLOR_GRAY2BGR)
	colors = 0
	for i in contours:
		for j in i:
			[x, y] = j
			if len(i) < 3:
				map[y, x] = (255,255,255)
			else:
				map[y, x] = COLORS[colors]
		colors += 1
		if colors >= len(COLORS):
			colors = 0

	cv2.namedWindow('Path', 0)
	cv2.imshow('Path', map)

        print "Final IMAGE !"
        print "Press n when done."

    elif APP_STATE == APP_STATE_PRINTING:

        print "Saving contours image..."
        cv2.imwrite('computed_contours.jpg',map)

        print "Loading Contours image..."
        cv2.imshow('Contours', map)

        print "Printing the contours..."

	pantolib.LaunchCalib()
        printContours(contours, r)
	pantolib.SetHome()
	pantolib.Wait()

        img = cv2.imread('graphical_ressources/printed.jpg')
        cv2.imshow('Printed', img)
        print "Printing complete."
        print "Collect your painting and press n to continue..."
	
    elif APP_STATE == APP_STATE_QUIT:
	    break

    else:
        img = cv2.imread('printed.jpg')
        cv2.imshow('Printed', img)
        print "Printing complete."
        print "Collect your painting and press n to continue or q to quit..."

    while True:
        ch = cv2.waitKey(0)
        if ch == ord('n'):
            print "Next state !"
            if APP_STATE < APP_STATE_PRINTING:
                APP_STATE = APP_STATE + 1
            else:
                APP_STATE = APP_STATE_INIT
	if ch == ord('q'):
		print "Quit application..."
		APP_STATE = APP_STATE_QUIT
        if ch == -1:
            continue
        else:
            break

    cv2.destroyAllWindows()
    pantolib.End()

        

