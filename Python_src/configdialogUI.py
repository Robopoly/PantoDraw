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
# File:        configdialogUI.py
# Date:        2016-05-31
# Author:      Paul-Edouard Sarlin
# Website:	   https://github.com/Robopoly/PantoDraw
#
# Description: Graphics for the GUI configuration dialog. Generated from file
#              'configdialogUI.ui' using PYQt4 UI code generator (v. 4.9.3).
#
#######################################################################################

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Configuration(object):
    def setupUi(self, Configuration):
        Configuration.setObjectName(_fromUtf8("Configuration"))
        Configuration.resize(367, 585)
        self.verticalLayout = QtGui.QVBoxLayout(Configuration)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.drawing_controls_box = QtGui.QGroupBox(Configuration)
        self.drawing_controls_box.setObjectName(_fromUtf8("drawing_controls_box"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.drawing_controls_box)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.time_points_Layout = QtGui.QHBoxLayout()
        self.time_points_Layout.setObjectName(_fromUtf8("time_points_Layout"))
        self.time_points_label = QtGui.QLabel(self.drawing_controls_box)
        self.time_points_label.setObjectName(_fromUtf8("time_points_label"))
        self.time_points_Layout.addWidget(self.time_points_label)
        self.time_points_value = QtGui.QDoubleSpinBox(self.drawing_controls_box)
        self.time_points_value.setDecimals(4)
        self.time_points_value.setMinimum(0.0001)
        self.time_points_value.setMaximum(1.0)
        self.time_points_value.setSingleStep(0.0001)
        self.time_points_value.setProperty("value", 0.005)
        self.time_points_value.setObjectName(_fromUtf8("time_points_value"))
        self.time_points_Layout.addWidget(self.time_points_value)
        self.verticalLayout_3.addLayout(self.time_points_Layout)
        self.time_contours_Layout = QtGui.QHBoxLayout()
        self.time_contours_Layout.setObjectName(_fromUtf8("time_contours_Layout"))
        self.time_contours_label = QtGui.QLabel(self.drawing_controls_box)
        self.time_contours_label.setObjectName(_fromUtf8("time_contours_label"))
        self.time_contours_Layout.addWidget(self.time_contours_label)
        self.time_contours_value = QtGui.QDoubleSpinBox(self.drawing_controls_box)
        self.time_contours_value.setDecimals(4)
        self.time_contours_value.setMinimum(0.0001)
        self.time_contours_value.setMaximum(1.0)
        self.time_contours_value.setSingleStep(0.0001)
        self.time_contours_value.setProperty("value", 0.3)
        self.time_contours_value.setObjectName(_fromUtf8("time_contours_value"))
        self.time_contours_Layout.addWidget(self.time_contours_value)
        self.verticalLayout_3.addLayout(self.time_contours_Layout)
        self.x_offset_Layout = QtGui.QHBoxLayout()
        self.x_offset_Layout.setObjectName(_fromUtf8("x_offset_Layout"))
        self.x_offset_label = QtGui.QLabel(self.drawing_controls_box)
        self.x_offset_label.setObjectName(_fromUtf8("x_offset_label"))
        self.x_offset_Layout.addWidget(self.x_offset_label)
        self.x_offset_value = QtGui.QSpinBox(self.drawing_controls_box)
        self.x_offset_value.setPrefix(_fromUtf8(""))
        self.x_offset_value.setMinimum(-50)
        self.x_offset_value.setMaximum(50)
        self.x_offset_value.setObjectName(_fromUtf8("x_offset_value"))
        self.x_offset_Layout.addWidget(self.x_offset_value)
        self.verticalLayout_3.addLayout(self.x_offset_Layout)
        self.y_offset_Layout = QtGui.QHBoxLayout()
        self.y_offset_Layout.setObjectName(_fromUtf8("y_offset_Layout"))
        self.y_offset_label = QtGui.QLabel(self.drawing_controls_box)
        self.y_offset_label.setObjectName(_fromUtf8("y_offset_label"))
        self.y_offset_Layout.addWidget(self.y_offset_label)
        self.y_offset_value = QtGui.QSpinBox(self.drawing_controls_box)
        self.y_offset_value.setMinimum(-50)
        self.y_offset_value.setMaximum(50)
        self.y_offset_value.setProperty("value", 10)
        self.y_offset_value.setObjectName(_fromUtf8("y_offset_value"))
        self.y_offset_Layout.addWidget(self.y_offset_value)
        self.verticalLayout_3.addLayout(self.y_offset_Layout)
        self.max_width_Layout = QtGui.QHBoxLayout()
        self.max_width_Layout.setObjectName(_fromUtf8("max_width_Layout"))
        self.max_width_label = QtGui.QLabel(self.drawing_controls_box)
        self.max_width_label.setObjectName(_fromUtf8("max_width_label"))
        self.max_width_Layout.addWidget(self.max_width_label)
        self.max_width_value = QtGui.QSpinBox(self.drawing_controls_box)
        self.max_width_value.setMinimum(1)
        self.max_width_value.setMaximum(500)
        self.max_width_value.setProperty("value", 150)
        self.max_width_value.setObjectName(_fromUtf8("max_width_value"))
        self.max_width_Layout.addWidget(self.max_width_value)
        self.verticalLayout_3.addLayout(self.max_width_Layout)
        self.max_height_Layout = QtGui.QHBoxLayout()
        self.max_height_Layout.setObjectName(_fromUtf8("max_height_Layout"))
        self.max_height_label = QtGui.QLabel(self.drawing_controls_box)
        self.max_height_label.setObjectName(_fromUtf8("max_height_label"))
        self.max_height_Layout.addWidget(self.max_height_label)
        self.max_height_value = QtGui.QSpinBox(self.drawing_controls_box)
        self.max_height_value.setMinimum(1)
        self.max_height_value.setMaximum(500)
        self.max_height_value.setProperty("value", 70)
        self.max_height_value.setObjectName(_fromUtf8("max_height_value"))
        self.max_height_Layout.addWidget(self.max_height_value)
        self.verticalLayout_3.addLayout(self.max_height_Layout)
        self.verticalLayout.addWidget(self.drawing_controls_box)
        self.image_proc_box = QtGui.QGroupBox(Configuration)
        self.image_proc_box.setObjectName(_fromUtf8("image_proc_box"))
        self.verticalLayout_6 = QtGui.QVBoxLayout(self.image_proc_box)
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
        self.cam_width_Layout = QtGui.QHBoxLayout()
        self.cam_width_Layout.setObjectName(_fromUtf8("cam_width_Layout"))
        self.cam_width_label = QtGui.QLabel(self.image_proc_box)
        self.cam_width_label.setObjectName(_fromUtf8("cam_width_label"))
        self.cam_width_Layout.addWidget(self.cam_width_label)
        self.cam_width_value = QtGui.QSpinBox(self.image_proc_box)
        self.cam_width_value.setMinimum(1)
        self.cam_width_value.setMaximum(2000)
        self.cam_width_value.setProperty("value", 320)
        self.cam_width_value.setObjectName(_fromUtf8("cam_width_value"))
        self.cam_width_Layout.addWidget(self.cam_width_value)
        self.verticalLayout_6.addLayout(self.cam_width_Layout)
        self.cam_height_Layout = QtGui.QHBoxLayout()
        self.cam_height_Layout.setObjectName(_fromUtf8("cam_height_Layout"))
        self.cam_height_label = QtGui.QLabel(self.image_proc_box)
        self.cam_height_label.setObjectName(_fromUtf8("cam_height_label"))
        self.cam_height_Layout.addWidget(self.cam_height_label)
        self.cam_height_value = QtGui.QSpinBox(self.image_proc_box)
        self.cam_height_value.setMinimum(1)
        self.cam_height_value.setMaximum(2000)
        self.cam_height_value.setProperty("value", 240)
        self.cam_height_value.setObjectName(_fromUtf8("cam_height_value"))
        self.cam_height_Layout.addWidget(self.cam_height_value)
        self.verticalLayout_6.addLayout(self.cam_height_Layout)
        self.verticalLayout.addWidget(self.image_proc_box)
        self.motors_controls_box = QtGui.QGroupBox(Configuration)
        self.motors_controls_box.setObjectName(_fromUtf8("motors_controls_box"))
        self.verticalLayout_7 = QtGui.QVBoxLayout(self.motors_controls_box)
        self.verticalLayout_7.setObjectName(_fromUtf8("verticalLayout_7"))
        self.up_table_Layout = QtGui.QHBoxLayout()
        self.up_table_Layout.setObjectName(_fromUtf8("up_table_Layout"))
        self.up_table_label = QtGui.QLabel(self.motors_controls_box)
        self.up_table_label.setObjectName(_fromUtf8("up_table_label"))
        self.up_table_Layout.addWidget(self.up_table_label)
        self.up_angle_value = QtGui.QSpinBox(self.motors_controls_box)
        self.up_angle_value.setMinimum(0)
        self.up_angle_value.setMaximum(180)
        self.up_angle_value.setProperty("value", 130)
        self.up_angle_value.setObjectName(_fromUtf8("up_angle_value"))
        self.up_table_Layout.addWidget(self.up_angle_value)
        self.verticalLayout_7.addLayout(self.up_table_Layout)
        self.down_table_Layout = QtGui.QHBoxLayout()
        self.down_table_Layout.setObjectName(_fromUtf8("down_table_Layout"))
        self.down_table_label = QtGui.QLabel(self.motors_controls_box)
        self.down_table_label.setObjectName(_fromUtf8("down_table_label"))
        self.down_table_Layout.addWidget(self.down_table_label)
        self.down_angle_value = QtGui.QSpinBox(self.motors_controls_box)
        self.down_angle_value.setMinimum(0)
        self.down_angle_value.setMaximum(180)
        self.down_angle_value.setProperty("value", 80)
        self.down_angle_value.setObjectName(_fromUtf8("down_angle_value"))
        self.down_table_Layout.addWidget(self.down_angle_value)
        self.verticalLayout_7.addLayout(self.down_table_Layout)
        self.home_angle_Layout = QtGui.QHBoxLayout()
        self.home_angle_Layout.setObjectName(_fromUtf8("home_angle_Layout"))
        self.home_angle_label = QtGui.QLabel(self.motors_controls_box)
        self.home_angle_label.setObjectName(_fromUtf8("home_angle_label"))
        self.home_angle_Layout.addWidget(self.home_angle_label)
        self.home_angle_value = QtGui.QSpinBox(self.motors_controls_box)
        self.home_angle_value.setMinimum(0)
        self.home_angle_value.setMaximum(180)
        self.home_angle_value.setProperty("value", 90)
        self.home_angle_value.setObjectName(_fromUtf8("home_angle_value"))
        self.home_angle_Layout.addWidget(self.home_angle_value)
        self.verticalLayout_7.addLayout(self.home_angle_Layout)
        self.resolution_Layout = QtGui.QHBoxLayout()
        self.resolution_Layout.setObjectName(_fromUtf8("resolution_Layout"))
        self.resolution_label = QtGui.QLabel(self.motors_controls_box)
        self.resolution_label.setObjectName(_fromUtf8("resolution_label"))
        self.resolution_Layout.addWidget(self.resolution_label)
        self.resolution_value = QtGui.QSpinBox(self.motors_controls_box)
        self.resolution_value.setMinimum(1)
        self.resolution_value.setMaximum(32)
        self.resolution_value.setProperty("value", 4)
        self.resolution_value.setObjectName(_fromUtf8("resolution_value"))
        self.resolution_Layout.addWidget(self.resolution_value)
        self.verticalLayout_7.addLayout(self.resolution_Layout)
        self.time_steps_Layout = QtGui.QHBoxLayout()
        self.time_steps_Layout.setObjectName(_fromUtf8("time_steps_Layout"))
        self.time_steps_label = QtGui.QLabel(self.motors_controls_box)
        self.time_steps_label.setObjectName(_fromUtf8("time_steps_label"))
        self.time_steps_Layout.addWidget(self.time_steps_label)
        self.time_steps_value = QtGui.QDoubleSpinBox(self.motors_controls_box)
        self.time_steps_value.setDecimals(4)
        self.time_steps_value.setMinimum(0.0001)
        self.time_steps_value.setMaximum(2.0)
        self.time_steps_value.setSingleStep(0.0001)
        self.time_steps_value.setProperty("value", 0.005)
        self.time_steps_value.setObjectName(_fromUtf8("time_steps_value"))
        self.time_steps_Layout.addWidget(self.time_steps_value)
        self.verticalLayout_7.addLayout(self.time_steps_Layout)
        self.verticalLayout.addWidget(self.motors_controls_box)
        self.buttons_Layout = QtGui.QHBoxLayout()
        self.buttons_Layout.setObjectName(_fromUtf8("buttons_Layout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.buttons_Layout.addItem(spacerItem)
        self.dialog_buttons = QtGui.QDialogButtonBox(Configuration)
        self.dialog_buttons.setOrientation(QtCore.Qt.Horizontal)
        self.dialog_buttons.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.dialog_buttons.setObjectName(_fromUtf8("dialog_buttons"))
        self.buttons_Layout.addWidget(self.dialog_buttons)
        self.verticalLayout.addLayout(self.buttons_Layout)

        self.retranslateUi(Configuration)
        QtCore.QObject.connect(self.dialog_buttons, QtCore.SIGNAL(_fromUtf8("accepted()")), Configuration.accept)
        QtCore.QObject.connect(self.dialog_buttons, QtCore.SIGNAL(_fromUtf8("rejected()")), Configuration.reject)
        QtCore.QMetaObject.connectSlotsByName(Configuration)

    def retranslateUi(self, Configuration):
        Configuration.setWindowTitle(QtGui.QApplication.translate("Configuration", "Configuration", None, QtGui.QApplication.UnicodeUTF8))
        self.drawing_controls_box.setTitle(QtGui.QApplication.translate("Configuration", "Drawing settings", None, QtGui.QApplication.UnicodeUTF8))
        self.time_points_label.setText(QtGui.QApplication.translate("Configuration", "Time between points:", None, QtGui.QApplication.UnicodeUTF8))
        self.time_points_value.setSuffix(QtGui.QApplication.translate("Configuration", " second", None, QtGui.QApplication.UnicodeUTF8))
        self.time_contours_label.setText(QtGui.QApplication.translate("Configuration", "Time between contours:", None, QtGui.QApplication.UnicodeUTF8))
        self.time_contours_value.setSuffix(QtGui.QApplication.translate("Configuration", " second", None, QtGui.QApplication.UnicodeUTF8))
        self.x_offset_label.setText(QtGui.QApplication.translate("Configuration", "Horizontal offset:", None, QtGui.QApplication.UnicodeUTF8))
        self.x_offset_value.setSuffix(QtGui.QApplication.translate("Configuration", " pixels", None, QtGui.QApplication.UnicodeUTF8))
        self.y_offset_label.setText(QtGui.QApplication.translate("Configuration", "Vertical offset:", None, QtGui.QApplication.UnicodeUTF8))
        self.y_offset_value.setSuffix(QtGui.QApplication.translate("Configuration", " pixels", None, QtGui.QApplication.UnicodeUTF8))
        self.max_width_label.setText(QtGui.QApplication.translate("Configuration", "Maximum table width:", None, QtGui.QApplication.UnicodeUTF8))
        self.max_height_label.setText(QtGui.QApplication.translate("Configuration", "Maximum table height:", None, QtGui.QApplication.UnicodeUTF8))
        self.image_proc_box.setTitle(QtGui.QApplication.translate("Configuration", "Image processing", None, QtGui.QApplication.UnicodeUTF8))
        self.cam_width_label.setText(QtGui.QApplication.translate("Configuration", "Camera width:", None, QtGui.QApplication.UnicodeUTF8))
        self.cam_width_value.setSuffix(QtGui.QApplication.translate("Configuration", " pixels", None, QtGui.QApplication.UnicodeUTF8))
        self.cam_height_label.setText(QtGui.QApplication.translate("Configuration", "Camera height:", None, QtGui.QApplication.UnicodeUTF8))
        self.cam_height_value.setSuffix(QtGui.QApplication.translate("Configuration", " pixels", None, QtGui.QApplication.UnicodeUTF8))
        self.motors_controls_box.setTitle(QtGui.QApplication.translate("Configuration", "Motors control", None, QtGui.QApplication.UnicodeUTF8))
        self.up_table_label.setText(QtGui.QApplication.translate("Configuration", "Table up angle:", None, QtGui.QApplication.UnicodeUTF8))
        self.up_angle_value.setSuffix(QtGui.QApplication.translate("Configuration", " deg.", None, QtGui.QApplication.UnicodeUTF8))
        self.down_table_label.setText(QtGui.QApplication.translate("Configuration", "Table down angle:", None, QtGui.QApplication.UnicodeUTF8))
        self.down_angle_value.setSuffix(QtGui.QApplication.translate("Configuration", " deg.", None, QtGui.QApplication.UnicodeUTF8))
        self.home_angle_label.setText(QtGui.QApplication.translate("Configuration", "Arms home angle:", None, QtGui.QApplication.UnicodeUTF8))
        self.home_angle_value.setSuffix(QtGui.QApplication.translate("Configuration", " deg.", None, QtGui.QApplication.UnicodeUTF8))
        self.resolution_label.setText(QtGui.QApplication.translate("Configuration", "Microstep resolution:", None, QtGui.QApplication.UnicodeUTF8))
        self.resolution_value.setPrefix(QtGui.QApplication.translate("Configuration", "1 / ", None, QtGui.QApplication.UnicodeUTF8))
        self.time_steps_label.setText(QtGui.QApplication.translate("Configuration", "Time between steps:", None, QtGui.QApplication.UnicodeUTF8))
        self.time_steps_value.setSuffix(QtGui.QApplication.translate("Configuration", " second(s)", None, QtGui.QApplication.UnicodeUTF8))

