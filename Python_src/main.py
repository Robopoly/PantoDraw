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
# File:        main.py
# Date:        2016-05-31
# Author:      Paul-Edouard Sarlin
# Website:	   https://github.com/Robopoly/PantoDraw
#
# Description: Main application managing the GUI and interfacing with the
#              processing module.
#
#######################################################################################


import sys
import cv2
import numpy as np
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import config
from mainwindow import Ui_MainWindow
from configdialog import ConfigDialog
import image_processing as imgproc

GREEN = "background-color: rgb(0,200,0,200)"
ORANGE = "background-color: rgb(255,170,0,200)"
WHITE = "background-color: rgb(255, 255, 255,200)"

# Main application window
class MainApp(QWidget):
	def __init__(self, parent=None):
		super(MainApp, self).__init__(parent)

		self.createUi()
		self.setConnections()
		self.setFSM()

		self.pathTimer = QTimer()
		self.pathTimer.timeout.connect(self.pathCheckThread)

		self.drawTimer = QTimer()
		self.drawTimer.timeout.connect(self.drawCheckThread)
		self.drawing = False

	# Manage graphical details not assessed in the QtDesigner file
	def createUi(self):
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		
		# add graphical ressources used here
		self.logo_robopoly = QPixmap("graphical_ressources/logo_robopoly.png")
		self.pic_bobo = QPixmap("graphical_ressources/bobo.png")

		self.setWindowIcon(QIcon(self.pic_bobo))

		self.ui.Robopoly_logo_label.setScaledContents(False)
		self.ui.Robopoly_logo_label.setPixmap(self.logo_robopoly.scaledToWidth(300,Qt.SmoothTransformation))
		self.ui.image_box.setStyleSheet("")
		self.pic_current = None

		self.ui.canny_thresh1.setValue(2000)
		self.ui.canny_thresh2.setValue(4000)

		# set default window size
		dw = QDesktopWidget()
		self.setFixedSize(dw.width()*0.9,dw.height()*0.7)

	# Manage Signals and Slots
	def setConnections(self):
		self.ui.side_push_exit.clicked.connect(self.exitApp)
		self.ui.side_push_config.clicked.connect(self.configuration)
		self.ui.capture_but.clicked.connect(self.captureImage)
		self.ui.import_but.clicked.connect(self.importImage)
		self.ui.canny_thresh1.sliderMoved.connect(self.displayCanny)
		self.ui.canny_thresh2.sliderMoved.connect(self.displayCanny)
		self.ui.state5_pause_but.clicked.connect(self.pauseDrawing)

	# Manage the FSM parameters
	def setFSM(self):
		self.FSM = QStateMachine()

		self.states = [QState() for i in range(6)] # create a list of 6 states
		self.lastState = 0
		
		# add transition between states with 'Previous', 'Next' and 'Restart' buttons
		for i in self.states:
			self.FSM.addState(i)
			i.setObjectName(str(self.states.index(i)))
		for i in range(0,5):
			self.states[i].addTransition(self.ui.next_but.clicked,self.states[i+1])
		for i in range(1,6):
			self.states[i].addTransition(self.ui.prev_but.clicked,self.states[i-1])
			self.states[i].addTransition(self.ui.side_push_restart.clicked,self.states[0])
		self.states[-1].addTransition(self.ui.next_but.clicked,self.states[0])

		# Set transition Slot
		for i in self.states:
			i.entered.connect(self.enter_state)

		self.FSM.setInitialState(self.states[0])
		self.FSM.start()		

	def reset(self):
		self.ui.canny_thresh1.setValue(2000)
		self.ui.canny_thresh2.setValue(4000)
		self.pic_current = None
		self.pathTimer.stop()
		self.drawTimer.stop()
		imgproc.end()
		imgproc.init()
		self.ui.side_push_config.setEnabled(True)

	# Slot for transition between states
	@pyqtSlot()
	def enter_state(self):
		self.ui.prev_but.setEnabled(True)
		self.ui.next_but.setEnabled(True)
		self.ui.prev_but.setText("Previous")
		self.ui.next_but.setText("Next")

		i = self.states.index(self.FSM.configuration()[0])
		print "State ", i

		if i == 0: # State: Start
			self.reset()

			self.ui.list_state1_label.setStyleSheet(ORANGE)
			self.ui.list_state2_label.setStyleSheet(WHITE)
			self.ui.list_state2_label.setStyleSheet(WHITE)
			self.ui.list_state3_label.setStyleSheet(WHITE)
			self.ui.list_state4_label.setStyleSheet(WHITE)
			self.ui.list_state5_label.setStyleSheet(WHITE)
			self.ui.list_state6_label.setStyleSheet(WHITE)
			self.ui.prev_but.setEnabled(False)
			self.pic_current = self.pic_bobo
			self.dispCurrentPic()

		elif i == 1: # State: Capture
			self.ui.list_state2_label.setStyleSheet(ORANGE)
			if self.lastState == 0:
				self.ui.list_state1_label.setStyleSheet(GREEN)
				self.ui.next_but.setEnabled(False)
				self.ui.image_box.setText("Capture or import a new image")
			else:
				self.ui.list_state3_label.setStyleSheet(WHITE)
				self.pic_current = self.mat2QImage(imgproc.getImage(new=False))
				self.dispCurrentPic()

		elif i == 2: # State: Contour Detection
			self.ui.list_state3_label.setStyleSheet(ORANGE)
			if self.lastState == 1:
				self.ui.list_state2_label.setStyleSheet(GREEN)
			else:
				self.ui.list_state4_label.setStyleSheet(WHITE)
				self.ui.side_push_config.setEnabled(True)

			self.displayCanny(None)

		elif i == 3: # State: Path Computation
			self.ui.list_state4_label.setStyleSheet(ORANGE)
			self.ui.side_push_config.setEnabled(False)
			if self.lastState == 2:
				self.ui.list_state3_label.setStyleSheet(GREEN)
				self.ui.image_box.setText("Computing path... Please wait.")
				self.ui.next_but.setEnabled(False)
				self.ui.prev_but.setEnabled(False)
				imgproc.computePath_launch()
				self.pathTimer.start(0)
			else:
				self.ui.list_state5_label.setStyleSheet(WHITE)
				self.pathCheckThread()

		elif i == 4: # State: Draw
			self.ui.list_state5_label.setStyleSheet(ORANGE)
			self.ui.side_push_config.setEnabled(False)
			if self.lastState == 3:
				self.ui.list_state4_label.setStyleSheet(GREEN)
			else:
				self.ui.list_state6_label.setStyleSheet(WHITE)
				temp, nb_countours = imgproc.computePath_result()
				self.pic_current = self.mat2QImage(temp)
				self.dispCurrentPic()
			self.ui.state5_pause_but.setText("Pause drawing")
			self.ui.prev_but.setEnabled(False)
			self.ui.next_but.setEnabled(False)
			imgproc.draw_launch()
			self.drawing = True
			self.drawTimer.start(0)

		else: # State: Finish
			self.ui.side_push_config.setEnabled(True)
			self.ui.next_but.setText("New drawing")
			self.ui.prev_but.setText("Draw again")
			self.ui.list_state6_label.setStyleSheet(ORANGE)
			self.ui.list_state5_label.setStyleSheet(GREEN)
			self.pic_current = self.pic_bobo
			self.dispCurrentPic()

		self.ui.stackedWidget.setCurrentIndex(i)
		self.lastState = i
		self.repaint()

	# Capture button
	@pyqtSlot()
	def captureImage(self):
		self.pic_current = self.mat2QImage(imgproc.getImage(new=True, capture=True))
		self.dispCurrentPic()
		self.ui.next_but.setEnabled(True)
	# Import button
	@pyqtSlot()
	def importImage(self):
		fileName = QFileDialog.getOpenFileName(self, "Import image", "", "Images (*.png *.xpm *.jpg)")
		if not fileName.isEmpty():
			self.pic_current = self.mat2QImage(imgproc.getImage(new=True, capture=False, path=fileName.toAscii().data()))
			self.dispCurrentPic()
			self.ui.next_but.setEnabled(True)
	# Canny sliders moved
	@pyqtSlot(int)
	def displayCanny(self, thresh):
		self.pic_current = self.mat2QImage(imgproc.computeCanny(self.ui.canny_thresh1.value(), self.ui.canny_thresh2.value()))
		self.dispCurrentPic()		
	# Pause button during drawing
	@pyqtSlot()
	def pauseDrawing(self):
		if self.drawing:
			self.ui.state5_pause_but.setText("Resume drawing")
			self.ui.prev_but.setEnabled(True)
			self.drawing = False
		else:
			self.ui.state5_pause_but.setText("Pause drawing")
			self.ui.prev_but.setEnabled(False)
			self.drawing = True
		imgproc.draw_pause(not self.drawing)
		self.repaint()

	# Check progression during Path Computation
	@pyqtSlot()
	def pathCheckThread(self):
		if not imgproc.computePath_hasFinished():
			progress = imgproc.computePath_progress()
			self.ui.state4_progress.setValue(progress)
			self.ui.state4_label.setText('<html><head/><body><p><span style=" font-size:14pt;">Progress: {0}%</span></p></body></html>'.format(progress))
			self.ui.side_push_restart.setEnabled(False)
		else:
			temp, nb_contours = imgproc.computePath_result()
			self.pic_current = self.mat2QImage(temp)
			self.dispCurrentPic()
			self.ui.state4_progress.setValue(100)
			self.ui.state4_label.setText('<html><head/><body><p><span style=" font-size:14pt;">{0} contours found</span></p></body></html>'.format(nb_contours))
			self.ui.next_but.setEnabled(True)
			self.ui.prev_but.setEnabled(True)
			self.ui.side_push_restart.setEnabled(True)
			self.pathTimer.stop()

	# Check progression during Drawing
	@pyqtSlot()
	def drawCheckThread(self):
		if imgproc.draw_hasFinished():
			self.ui.next_but.setEnabled(True) # manually move to next state
			self.ui.next_but.click()
			self.drawTimer.stop()

	# Start configuration window and gather the new parameters
	@pyqtSlot()
	def configuration(self):
		dialog = ConfigDialog()
		dialog.setWindowModality(False)

		dialog.ui.time_points_value.setValue(config.TIME_BETWEEN_POINTS)
		dialog.ui.time_contours_value.setValue(config.TIME_BETWEEN_CONTOURS)
		dialog.ui.x_offset_value.setValue(config.X_OFFSET)
		dialog.ui.y_offset_value.setValue(config.Y_OFFSET)
		dialog.ui.max_width_value.setValue(config.MAX_WIDTH)
		dialog.ui.max_height_value.setValue(config.MAX_HEIGHT)
		dialog.ui.cam_width_value.setValue(config.CAM_WIDTH)
		dialog.ui.cam_height_value.setValue(config.CAM_HEIGHT)
		dialog.ui.up_angle_value.setValue(config.UP_TABLE)
		dialog.ui.down_angle_value.setValue(config.DOWN_TABLE)
		dialog.ui.home_angle_value.setValue(config.HOME_ANGLE)
		dialog.ui.resolution_value.setValue(config.RESOLUTION)
		dialog.ui.time_steps_value.setValue(config.WAIT_STEP)
		
		if dialog.exec_():
			print "New configuration accepted"

			config.TIME_BETWEEN_POINTS = dialog.ui.time_points_value.value()
			config.TIME_BETWEEN_CONTOURS = dialog.ui.time_contours_value.value()
			config.X_OFFSET = dialog.ui.x_offset_value.value()
			config.Y_OFFSET = dialog.ui.y_offset_value.value()
			config.MAX_WIDTH = dialog.ui.max_width_value.value()
			config.MAX_HEIGHT = dialog.ui.max_height_value.value()
			config.CAM_WIDTH = dialog.ui.cam_width_value.value()
			config.CAM_HEIGHT = dialog.ui.cam_height_value.value()
			config.UP_TABLE = dialog.ui.up_angle_value.value()
			config.DOWN_TABLE = dialog.ui.down_angle_value.value()
			config.HOME_ANGLE = dialog.ui.home_angle_value.value()
			config.RESOLUTION = dialog.ui.resolution_value.value()
			print "New config: ", config.UP_TABLE

	@pyqtSlot()
	def exitApp(self):
		imgproc.end()
		qApp.quit()

	# Utility function for converting OpenCV images (Mat) into Qt ones (QImage)
	def mat2QImage(self,temp):
		temp = cv2.cvtColor(temp, cv2.COLOR_BGR2RGB)
		img = QImage(temp.data, temp.shape[1], temp.shape[0], QImage.Format_RGB888)
		img.bits()
		return QPixmap.fromImage(img)
	# Handle aspect ratio concerns when displaying an image stored in self.pic_current
	def dispCurrentPic(self):
			pic_ratio = self.pic_current.height()/self.pic_current.width()
			size = self.ui.image_box.size()
			label_ratio = size.height()/size.width()
			
			if pic_ratio > label_ratio:
				self.ui.image_box.setPixmap(self.pic_current.scaledToHeight(size.height(),Qt.SmoothTransformation))
			else:
				self.ui.image_box.setPixmap(self.pic_current.scaledToWidth(size.width(),Qt.SmoothTransformation))
			
if __name__ == '__main__':
	qApp = QApplication(sys.argv)
	mainApp = MainApp()
	mainApp.show()
	sys.exit(qApp.exec_())
