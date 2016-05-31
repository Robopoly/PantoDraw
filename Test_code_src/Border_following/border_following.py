#! /usr/bin/python

# The following code is a general algorithm whose purpose
# is to find the  different contours in a 1-bit image
# (for example returned by the Canny algorithm) and store
# each of them as a vector of the points which compose it.

# A B C
# D - E
# F G H

from __future__ import division
from numpy import linalg as LA
from time import sleep
import os
import cv2
import sys
import numpy as np
import cPickle

MAP_COLOR = 200
COLORS = [[0,0,255],[0,255,0],[255,0,0],[200,200,50],[0,255,255],[0,128,255]]

def follow_contour(x, y):

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
				follow_contour(u, v)
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

def export_contours(contours):
	
	file = open("saved_contours.txt", "w")
	np.savetxt(file, contours, delimiter=" ", fmt="%s")
	file.close()

input_file = raw_input('Specify file to proceed: ')
input_file = './' + input_file

img = cv2.imread(input_file)
img = cv2.copyMakeBorder(img,1,1,1,1,cv2.BORDER_CONSTANT,value=(0,0,0))
img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
retval, img = cv2.threshold(img,100,255,cv2.THRESH_BINARY)

width, height = img.shape
print 'width=', width, '; height=', height


map = img.copy()
map[:,:] = 0;
contours = []

for j in range(1, width-1):
	for i in range(1, height-1):
		
		# When accessing img as numpy arrays, x and y are inverted
		if not img[j,i] or map[j,i]:
			continue
		
		[x, y] = [i, j]
		follow_contour(x, y)

# Rearrange contours
for index_i, i in enumerate(contours):
	[x, y] = i[0]
	for index_j, j in enumerate(contours):
		if index_i != index_j:
			[u, v] = j[0]
			if np.absolute(u-x)<2 and np.absolute(v-y)<2:
				contours[index_i][:0] = list(reversed(contours[index_j]))
				del contours[index_j]
				break

export_contours(contours)

# Print map
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

cv2.imwrite('result.jpg', map)
print len(contours), ' contours found'

cv2.namedWindow("Original Canny", 0)
cv2.imshow("Original Canny", img)
cv2.namedWindow("Detected valid contours", 0)
cv2.imshow("Detected valid contours", map)

while True:
	ch = cv2.waitKey(0)
	if (ch) == -1:
		continue
	else:
		break


