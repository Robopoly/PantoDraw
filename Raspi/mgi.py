#!/usr/bin/python

from __future__ import division
from numpy import linalg as LA
import numpy as np
import cv2
import cPickle

def MGI( x, y ):
   
    a = 1
    L1 = 5
    powL1 = np.power(L1, 2)
    L2 = 6
    powL2 = np.power(L2, 2)

    E = np.array([x, y])


    M1 = [-a/2,0]
    M2 = [a/2,0]

    E1p = E-M1
    E2p = E-M2

    #print 'E1p: ', E1p
    #print 'E2p: ', E2p


    normE1p = LA.norm(E1p)
    normE2p = LA.norm(E2p)
    powerL1 = np.power(L1, 2)
    powerL2 = np.power(L2, 2)

    #print 'E1p(1): ', E1p[0]
    #print 'E1p(2): ', E1p[1]

    q1acosPar = ( np.power(normE1p, 2) + powerL1 - powerL2 ) / ( 2 * normE1p * L1 )
    print 'q1acosPar: ', q1acosPar
    q1acos = np.arccos(q1acosPar)
    q1atan2 = np.arctan2(E1p[1], E1p[0])
    q1 = q1acos + q1atan2
    #print 'q1: ', q1

    q2acosPar = ( np.power(normE2p, 2) + powerL1 - powerL2 ) / ( 2 * normE2p * L1 )
    q2acos = np.arccos(q2acosPar)
    q2atan2 = np.arctan2(E2p[1], E2p[0])
    q2 = q2acos + np.pi - q2atan2
    #print 'q2: ', q2

    return q1, q2



