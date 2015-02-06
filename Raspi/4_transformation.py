#!/usr/bin/python

from __future__ import division
from numpy import linalg as LA
import numpy as np
import cv2
import cPickle
import mgi


contour = np.array([ [[109, 62]], [[109, 186]], [[261, 186]], [[261, 62]] ])
#print contour

#np.savetxt('contour.txt', contour_example)
#contour = np.load('contour.txt')

for p in contour:
    [[ x, y ]] = p
    (q1, q2) = mgi.MGI(x, y)
    print 'x: ', x, 'y:', y, '	--> q1: ', q1, 'q2:', q2

