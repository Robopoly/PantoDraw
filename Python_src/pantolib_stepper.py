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
# File:        pantolib_stepper.py
# Date:        2016-05-31
# Authors:     Jean-Luc Liardon, Marco Pagnamenta,
#              Pablo Garcia del Valle, Paul-Edouard Sarlin
# Website:     https://github.com/Robopoly/PantoDraw
#
# Description: High-level stepper and servo motors control module.
#
#######################################################################################

import Adafruit_BBIO.PWM as PWM
import Adafruit_BBIO.GPIO as GPIO
from stepper import Stepper
import config
from time import sleep

# servo parameters
a_min = 67.
duty0 = 3.
duty180 = 12.
ratio1 = (duty180-duty0)/180
pwm_f = 50

# define pin numbers
B_1 = "P9_12"
B_2 = "P9_14"
SUPPORT = "P9_42"

# define angles
iddleAngle = 150
endAngle1 = 210
endAngle2 = 192

# instantiate stepper objects
s1 = Stepper(1, config.RESOLUTION)
s2 = Stepper(2, config.RESOLUTION)

def Init():
	PWM.start(SUPPORT, ratio1 *  config.DOWN_TABLE + duty0, pwm_f)
        GPIO.setup(B_1, GPIO.IN)
        GPIO.setup(B_2, GPIO.IN)

# WIP function
def NewLaunchCalib():
	s2.inc() #block stepper 2
	Calibrate(s1, B_1, endAngle1)
	Calibrate(s2, B_2, endAngle2)
	sleep(0.5)

#WIP function
def LaunchCalib():
	s1.set(AngleToStep(config.HOME_ANGLE))
	s2.set(AngleToStep(config.HOME_ANGLE))
	Dec1()
	Dec2()

	#s1.wait()
	#s2.wait()
	#GoTo(startAngle, startAngle)

# WIP function
def Calibrate(s, button, endAngle):
        while GPIO.input(button): # buttons are at Vcc when released
                s.inc()
                sleep(config.WAIT_STEP)
        while not GPIO.input(button):
                s.dec()
                sleep(config.WAIT_STEP)
        s.set(AngleToStep(endAngle))
        while s.get() > AngleToStep(startAngle):
                s.dec()
                sleep(config.WAIT_STEP)

def GoTo(a1,a2):
        q1 = AngleToStep(a1)
        q2 = AngleToStep(a2)
        while (s1.get() != q1) or (s2.get() != q2):
                if s1.get() < q1:
                        s1.inc()
                elif s1.get() > q1:
                        s1.dec()

                if s2.get() < q2:
                        s2.inc()
                elif s2.get() > q2:
                 	s2.dec()

                sleep(config.WAIT_STEP)

def SetHome():
	GoTo(config.HOME_ANGLE, config.HOME_ANGLE)

def Inc1():
	s1.inc()
	sleep(config.WAIT_STEP)
def Inc2():
	s2.inc()
	sleep(config.WAIT_STEP)
def Dec1():
	s1.dec()
	sleep(config.WAIT_STEP)
def Dec2():
	s2.dec()
	sleep(config.WAIT_STEP)

# Bring table up
def Up():
	for i in range(config.DOWN_TABLE, config.UP_TABLE+1):
        	PWM.set_duty_cycle(SUPPORT, ratio1 * i + duty0)
		sleep(0.01)
# Bring table down
def Down():
        PWM.set_duty_cycle(SUPPORT, ratio1 * config.DOWN_TABLE + duty0)

# Set coils current to minimum if possible
def Wait():
	s1.wait()
	s2.wait()
# Set coils current to zero
def End():
        s1.end()
        s2.end()

def AngleToStep(a):
        return int(round(a*config.RESOLUTION/0.9))
