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
# File:        image_processing.py
# Date:        2016-05-31
# Authors:     Jean-Luc Liardon, Marco Pagnamenta,
#              Pablo Garcia del Valle, Paul-Edouard Sarlin
# Website:     https://github.com/Robopoly/PantoDraw
#
# Description: Module performing all the image processing tasks: image acquisition,
#              Canny edge detection, path computation and optimization,
#              pen position control.
#
#######################################################################################

from __future__ import division
from time import sleep
import os
import cv2
import sys
import numpy as np
import cPickle
import mgi
import config
from threading import Thread

if config.PLATFORM == 'BEAGLE': 
    import pantolib_stepper as pantolib
else:
    import pantolib_dummy as pantolib

COLORS = [[0,0,255],[0,255,0],[255,0,0],[200,200,50],[0,255,255],[0,128,255]]
MAP_COLOR = 150 # color for discarded pixels

contours = []
cont_counter = 0
x_trans_factor = 0
y_trans_factor = 0
r = 0 # resize factor
cam = None

# Mat objects
img = None
resized = None
canny_out = None
map = None

# for info exchange between main and processing threads
procThreadProgress = 0
procThreadFinished = True
procThreadPause = False
drawingActive = False

def nothing(*arg):
    pass

def drawPoint(x, y, r):
    x_resize = int(x*r)
    y_resize =  int(y*r)
    print 'x: ', x, 'y:', y, '	--> int(x*r): ', x_resize, ' int(y*r):', y_resize
    x_trans = x_resize + x_trans_factor + config.X_OFFSET
    y_trans = -y_resize + y_trans_factor + config.Y_OFFSET
    (q1, q2) = mgi.MGI(x_trans, y_trans)
    print 'x: ', x_resize, 'y:', y_resize, '	--> x-trans: ', x_trans, 'y_trans:', y_trans, '	--> q1: ', q1, 'q2:', q2
    pantolib.GoTo(q1, q2)


def draw_run():
	global contours, cont_counter,  r, procThreadFinished, procThreadProgress, procThreadPause, drawingActive
	drawingActive = True
	
	if cont_counter == 0: # Means a new drawing is started (not resuming a paused one)
		procThreadProgress = 0
		procThreadPause = False
		procThreadFinished = False

	while cont_counter < len(contours):
        	c = contours[cont_counter]

            	print '----------------  contour -------------------'
            	if len(c) < 2:
                	print "Void contour (contained only one point)"
        	elif len(c) < 4:
			print "Filtered point"
		else:
        		# Lift pen, go to first point of the countour, and start drawing
		        pantolib.Down()
        		[ x, y ] = c[0]
	        	drawPoint(x, y, r)
		        sleep(config.TIME_BETWEEN_CONTOURS)
		        pantolib.Up()
		        sleep(config.TIME_BETWEEN_POINTS)
			
			c = c[1:]
			# Iterate through the contour
		        for p in c:
        		        [ x, y ] = p
				drawPoint(x, y, r)
				sleep(config.TIME_BETWEEN_POINTS)

	        	pantolib.Down()
			sleep(config.TIME_BETWEEN_CONTOURS)

		cont_counter += 1
		procThreadProgress = cont_counter * 100 / len(contours)
		
		if procThreadPause: # Pausing command from the GUI
			drawingActive = False
			return

	pantolib.SetHome()
	pantolib.Wait()
	procThreadFinished = True
	drawingActive = False
	return

# Recursive function
def followContour(x, y, map, img):
	map[y, x] = MAP_COLOR
	new_contour = [[x, y]]
	#print "-----> New contour at ", [x, y]

	while(True):
		s = np.array([[x-1,y-1],[x,y-1],[x+1,y-1],[x-1,y],[x+1,y],[x-1,y+1],[x,y+1],[x+1,y+1]])
		# Create masks for surrounding points
		img_mask = []
		map_mask = []
		for k in s:
			img_mask.append(img[k[1], k[0]])
			map_mask.append(map[k[1], k[0]])
		result = np.logical_and(img_mask, np.logical_not(map_mask))
		next = np.nonzero(result)[0] # usually returns a tuple of arrays
	
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
				followContour(u, v, map, img)
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
		contours.insert(0,new_contour)

# Running function for the path computing thread
def computePath_run():
	global canny_out, map, procThreadFinished, procThreadProgress, contours
	contours[:] = []
	procThreadFinished = False
	procThreadProgress = 0

	img = canny_out
	# Convert Canny image from 3 to 1 channels
	img = cv2.copyMakeBorder(img,1,1,1,1,cv2.BORDER_CONSTANT,value=(0,0,0))
	#img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	retval, img = cv2.threshold(img,100,255,cv2.THRESH_BINARY)

	width, height = img.shape
	map = img.copy()
	map[:,:] = 0

	for j in range(1, width-1):
		for i in range(1, height-1):
			procThreadProgress = int((j*height+i)*100/(width*height)) # Update processing progress
			# When accessing img as numpy arrays, x and y are inverted
			if not img[j,i] or map[j,i]: # not a contour or already taken into account
				continue
		
			[x, y] = [i, j]
			followContour(x, y, map, img)

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

	map = cv2.cvtColor(map, cv2.COLOR_GRAY2BGR)
	colors = 0
	# Create a map of the path with a different color for each contour
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

	# Map has to be resized since we added an extra one pixel-width black border
	map = cv2.resize(map, (canny_out.shape[1],canny_out.shape[0]))
	procThreadFinished = True
	return

def exportContours(contours): # Useful when debugging
	file = open("saved_contours.txt", "w")
	np.savetxt(file, contours, delimiter=" ", fmt="%s")
	file.close()

# ---- Below: functions accessed by main.py module ----

def init():
	global procThreadFinished, procThreadPause, drawingActive
	procThreadFinished = True
	procThreadPause = False
	drawingActive = False
	pantolib.Init()

# Capture a new image or import it (capture arg.) or send the previous one (new ar.)
def getImage(new=False, capture=True, path=""):
	global cam, img, r, x_trans_factor, y_trans_factor
	
	if new:
		if capture:
			if cam is None:
				cam = cv2.VideoCapture(-1)
				if cam is None: # Camera is not plugged-in
					return
				cam.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, config.CAM_WIDTH)
				cam.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, config.CAM_HEIGHT)

				print "Camera Properties:"
				print "\t Width: ",cam.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)
				print "\t Height: ",cam.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)
			for i in range(0,10):
				ret, img = cam.read()
	
		else: # import an image
			img = cv2.imread(path)

	        # we need to keep in mind aspect ratio so the image does
        	# not look skewed or distorted -- therefore, we calculate
	        # the ratio of the new image to the old image
        	r = float(config.MAX_WIDTH) / img.shape[1]
	        dim = (config.MAX_WIDTH, int(img.shape[0] * r))
        	if dim[0] > config.MAX_HEIGHT:
	            r = float(config.MAX_HEIGHT) / img.shape[0]
        	    dim = (int(img.shape[1] * r), config.MAX_HEIGHT)
	        # perform the actual resizing of the image and show it
	        resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
	        x_trans_factor = -dim[0]/2.
	        y_trans_factor = dim[1]/2. + 130

	return img

def computeCanny(thrs1, thrs2):
	global canny_out

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        canny_out = cv2.Canny(gray, thrs1, thrs2, apertureSize=5, L2gradient=False)
        vis = img.copy()
        vis /= 2
        vis[canny_out != 0] = (0, 255, 0)

	return vis

# launch a new thread for path computing
def computePath_launch(new=False):
	Thread(target=computePath_run, args=()).start()
	return
def computePath_hasFinished():
	return procThreadFinished
def computePath_progress():
	return procThreadProgress
def computePath_result():
	global map, contours
	return map, len(contours)

# launch a new thread for picture drawing
def draw_launch():
	global cont_counter
	cont_counter = 0
	pantolib.LaunchCalib()
	Thread(target=draw_run, args=()).start()
	return
def draw_hasFinished():
	return procThreadFinished
def draw_progress():
	return procThreadProgress
def draw_pause(pause):
	global procThreadPause
	print "pause triggered: ", pause
	procThreadPause = pause
	if not pause and not drawingActive: # because drawing doesn't pause immediately
		Thread(target=draw_run, args=()).start()
	return


def end():
	global procThreadPause
	if drawingActive: # if Exit while still drawing
		procThreadPause = True
		while drawingActive:
			pass
	pantolib.End()
	if cam is not None:
		cam.release()
