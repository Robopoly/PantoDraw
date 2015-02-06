#!/usr/bin/python

from __future__ import division
from numpy import linalg as LA

import numpy as np
import cv2
import cPickle

x = np.array([1, 2, 3, 4, 5])
y = np.array([10, 11, 12, 13, 14])

print 'x = ', x
print 'y = ', y

print 'res = ', x+y

a = 1

E = [10, 10]

M1 = [-a/2,0]
M2 = [a/2,0]

E1p = [E[0] - M1[0], E[1] - M1[1]]
E2p = [E[0] - M2[0], E[1] - M2[1]]

print E1p
print E2p

A = np.array([3, 5])

print A
print "norm: ", LA.norm(A)
print "power: ", np.power(LA.norm(A),2)
print "acos: ", np.arccos([-1])
print "atan2: ", np.arctan2([-1], [0])
print "Pi: ", np.pi


#print 'p1:',  p1, 'p2:', p2

print '-------------------------'





