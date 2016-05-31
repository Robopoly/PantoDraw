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
# File:        config.py
# Date:        2016-05-31
# Author:      Paul-Edouard Sarlin
# Website:     https://github.com/Robopoly/PantoDraw
#
# Description: Configuration file containing the main parameters.
#              These are accessible from the 'Configuration' panel in the GUI.
#
#######################################################################################



PLATFORM = 'BEAGLE' #'PC'

# Drawing controls
TIME_BETWEEN_POINTS = 0.005
TIME_BETWEEN_CONTOURS = 0.3

X_OFFSET = 0
Y_OFFSET = 10
MAX_WIDTH = 150
MAX_HEIGHT = 70

CAM_WIDTH = 320
CAM_HEIGHT = 240

# Motors controls
UP_TABLE = 100
DOWN_TABLE = 80
HOME_ANGLE = 90

RESOLUTION = 4
WAIT_STEP = 0.005
