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
# File:        stepper.py
# Date:        2016-05-31
# Authors:     Paul-Edouard Sarlin
# Website:     https://github.com/Robopoly/PantoDraw
#
# Description: Low-level stepper motors control module with class implementation.
#
#######################################################################################

import Adafruit_BBIO.GPIO as GPIO


AEN = 0
APH = 1
BEN = 6
BPH = 7

A10 = 2
B10 = 8

ADEC = 5
BDEC = 11

ADDR = 12

DATA = "P9_11"
CLCK = "P9_13"
SSTB = "P9_15"

# for 20% / 71% / 98% / 100%
current = [0b001, 0b011, 0b101, 0b111]

class Stepper:
        def __init__(self, id=1, resolution=2):
                self.id = id-1 # can be either 1 or 0
                self.count = -1
                self.offset = 0
                self.res = resolution # e.g 2 for half-steps

                GPIO.setup(DATA, GPIO.OUT)
                GPIO.setup(CLCK, GPIO.OUT)
                GPIO.setup(SSTB, GPIO.OUT)
                GPIO.output(DATA, GPIO.LOW)
                GPIO.output(CLCK, GPIO.LOW)
                GPIO.output(SSTB, GPIO.LOW)

        def sendCommand(self, base):
                for i in range(0,16):
                        data = (base & (1 << i)) >> i
                        if data == 1:
                                out = GPIO.HIGH
                        else:
                                out = GPIO.LOW

                        GPIO.output(DATA, out)
                        GPIO.output(CLCK, GPIO.HIGH)
                        GPIO.output(CLCK, GPIO.LOW)
                        GPIO.output(DATA, GPIO.LOW)

                GPIO.output(SSTB, GPIO.HIGH)
                GPIO.output(SSTB, GPIO.LOW)

	# Current sequence is hardcoded for 1/2, 1/4 and 1/8 microsteps
        def computeSeq(self):
                state = (self.count + self.offset)%(4*self.res)
                base = (self.id << ADDR)
		base |= (1 << ADEC) | (1 << BDEC)
	
                if self.res == 2:
                        if state == 0:
                                base |= (1 << AEN) | (1 << APH)
                                base |= (current[3] << A10)
                        if state == 1:
                                base |= (1 << AEN) | (1 << APH) | (1 << BEN) | (1 << BPH)
                                base |= (current[1] << A10) | (current[1] << B10)
                        if state == 2:
                                base |= (1 << BEN) | (1 << BPH)
                                base |= (current[3] << B10)
                        if state == 3:
                                base |= (1 << AEN) | (1 << BEN) | (1 << BPH)
                                base |= (current[1] << A10) | (current[1] << B10)
                        if state == 4:
                                base |= (1 << AEN)
                                base |= (current[3] << A10)
                        if state == 5:
                                base |= (1 << AEN) | (1 << BEN)
                                base |= (current[1] << A10) | (current[1] << B10)
                        if state == 6:
                                base |= (1 << BEN)
                                base |= (current[3] << B10)
                        if state == 7:
                                base |= (1 << AEN) | (1 << APH) | (1 << BEN)
                                base |= (current[1] << A10) | (current[1] << B10)

                if self.res == 4:
                        if state == 0:
                                base |= (1 << AEN) | (1 << APH)
                                base |= (current[3] << A10)
                        if (state > 0) and (state < 4):
                                base |= (1 << AEN) | (1 << APH) | (1 << BEN) | (1 << BPH)
                                base |= (current[3-state] << A10) | (current[state-1] << B10)
                        if state == 4:
                                base |= (1 << BEN) | (1 << BPH)
                                base |= (current[3] << B10)
                        if (state > 4) and (state < 8):
                                base |= (1 << AEN) | (1 << BEN) | (1 << BPH)
                                base |= (current[state-5] << A10) | (current[7-state] << B10)
                        if state == 8:
                                base |= (1 << AEN)
                                base |= (current[3] << A10)
                        if (state > 8) and (state < 12):
                                base |= (1 << AEN) | (1 << BEN)
                                base |= (current[11-state] << A10) | (current[state-9] << B10)
                        if state == 12:
                                base |= (1 << BEN)
                                base |= (current[3] << B10)
                        if (state > 12) and (state < 16):
                                base |= (1 << AEN) | (1 << APH) | (1 << BEN)
                                base |= (current[state-13] << A10) | (current[15-state] << B10)

                if self.res == 8:
                        if state == 0:
                               base |= (1 << AEN) | (1 << APH)
                               base |= (0b111 << A10)
                        if (state > 0) and (state < 8 ):
                               base |= (1 << AEN) | (1 << APH) | (1 << BEN) | (1 << BPH)
                               base |= ((7-state) << A10) | ((state-1) << B10)
                        if state == 8:
                               base |= (1 << BEN) | (1 << BPH)
                               base |= (0b111 << B10)
                     	if (state > 8) and (state < 16):
                               base |= (1 << AEN) | (1 << BEN) | (1 << BPH)
                               base |= ((state-9) << A10) | ((15-state) << B10)
                        if state == 16:
                               base |= (1 << AEN)
                               base |= (0b111 << A10)
                        if (state > 16) and (state < 24):
                               base |= (1 << AEN) | (1 << BEN)
                               base |= ((23-state) << A10) | ((state-17) << B10)
                        if state == 24:
                               base |= (1 << BEN)
                               base |= (0b111 << B10)
                        if (state > 24) and (state < 32):
                               base |= (1 << AEN) | (1 << APH) | (1 << BEN)
                               base |= ((state-25) << A10) | ((31-state) << B10)

                #print bin(base)
                return base

        def inc(self):
                self.count += 1
                self.sendCommand(self.computeSeq())
        def dec(self):
                self.count -= 1
                self.sendCommand(self.computeSeq())

        def get(self):
                return self.count
        def set(self, newCount):
                self.offset = int((newCount - self.count)%(4*self.res))
                self.count = newCount
	
	def wait(self):
		base = self.computeSeq()
		if ((self.count+self.offset)%self.res) == 0:
			base &= ~((0b111 << A10) | (0b111 << B10)) #set current to min
		self.sendCommand(base)
        def end(self):
                self.sendCommand(self.id << ADDR)

