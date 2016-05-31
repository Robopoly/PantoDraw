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
# File:        mgi.py
# Date:        2016-05-31
# Authors:     Jean-Luc Liardon, Marco Pagnamenta, Pablo Garcia del Valle
# Website:     https://github.com/Robopoly/PantoDraw
#
# Description: Performs the inverse kinematics computation (determines the angle of
#              the arms based on the cartesian coordinates).
#
#######################################################################################

from __future__ import division
from numpy import linalg as LA
import numpy as np
import cv2
import cPickle

def MGI( x, y ):
   
    a = 50
    L1 = 90
    powL1 = np.power(L1, 2)
    L2 = 125
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
    #print 'q1acosPar: ', q1acosPar
    q1acos = np.arccos(q1acosPar)
    q1atan2 = np.arctan2(E1p[1], E1p[0])
    q1 = q1acos + q1atan2
    #print 'q1: ', q1

    q2acosPar = ( np.power(normE2p, 2) + powerL1 - powerL2 ) / ( 2 * normE2p * L1 )
    q2acos = np.arccos(q2acosPar)
    q2atan2 = np.arctan2(E2p[1], E2p[0])
    q2 = q2acos + np.pi - q2atan2
    #print 'q2: ', q2
    q1 = q1 * 180./np.pi
    q2 = q2 * 180./np.pi
    return q1, q2



