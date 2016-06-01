# The PantoDrawThe Pantodraw is a device capable of drawing the portrait of people interacting with it. <img align=“center” src="https://github.com/Robopoly/PantoDraw/blob/version_2/Documents/image_1.JPG" width=“250”>## Main conceptAs visitors always enjoy interacting with robots when visiting Robopoly’s booth at EPFL events, the goal of this project is to give them the opportunity to spend a pleasant time being drawn by a robot-like device. By exploiting the capabilities of the [Beagle Bone Black](https://beagleboard.org/black) (BBB), a Texas Instrument single-board powerful computer, and Python programming language, the development team ended up with an original and easy-to-use demonstration of the various skills found at Robopoly.Operated by a competent user, the device is able to determine the contour of one’s face, compute the optimal path for the pen, and draw the result on a paper the visitor can return with.An inexpensive webcam and the [OpenCV](http://opencv.org/) image processing library are used for the contours detection. The input image is first converted to grayscale and then goes through a Canny edge detection algorithm, whose parameters can be manually adjusted.Based on the resulting contours map, a custom algorithm computes the trajectory and minimises the number of branching and raise/drop of the pen.The resulting image is finally drawn on a paper using three motors: two for the planar movement of the pen and one for the linear movement of the paper support.## Version 1The first version of the device was developed for Robopoly’s booth at [Japan Impact](http://www.japan-impact.ch/en/), the annual Japanese convention at EPFL. The process was supervised and control through the Linux terminal using a set of screen, keyboard and mouse connected via a USB hub to the BBB.The code was rather rudimentary since it was not possible to jump to the previous step, redo the current one or stop the execution. Inverse kinematics equations were computed using a Matlab script, which was also used to optimise the size of the arms.On the hardware side, servomotors were used, allowing to easily control the pen position with only a few lines of code using the [Adafruit BBB library](https://learn.adafruit.com/setting-up-io-python-library-on-beaglebone-black). Paper was attached to its support by sliding its corners into tiny slits and the complete structure had been 3D printed at Robopoly.## Version 2In order to improve the precision - and thus the quality - of the drawing and the usability of the device, both the software and the hardware part have been improved in a second version.Some servos were replaced by stepper motors, which do not present the internal slack that servos had.A graphical user interface (GUI) has been designed with Qt Designer and converted to Python using [PyQt4](https://www.riverbankcomputing.com/software/pyqt/intro). It now allows a smooth interaction with the program: it is thus possible to import an image from a file on disk, visualise the different stages of the image, jump to a previous step, change various settings and save them for a future use.A complete stepper driver module was written with multiple micro-stepping resolutions and a PCB was resigned for the driver integrated chip.<img align=“center” src="https://github.com/Robopoly/PantoDraw/blob/version_2/GUI_src/gui_screenshot_1.jpg" width=“10”>## Hardware* BeagleBone Black rev. C* Texas Instrument DRV8823 motor driver* Bipolar stepper motor 17HM19-2004S (x2)* Servomotor RS2 MG/BB* 3D-printed structure* Folex plotter pen* A6 paper## WiringThe connections to the BBB are:| Name               | Pin    || -------------------| ------ | | Driver Data        | P9_11  || Driver Clock       | P9_13  || Driver SSTB        | P9_15  || Driver Chip Select | 5V     || Servo signal       | P9_ 42 || VCC                | 5V     || Ground             | GND    |The Vbat pin of the driver has to be connected to a DC source which will provide the power for the motors. No exact value is needed since the IC performs a current chop regulation, but there are some conditions: if Vbat is too low, current ramp will be too slow and steps could be missed, but, if V_bat is too high, the driver will dissipate too much heat and its internal thermal shutdown will quickly activate. 20V seems to be working well.The BBB and the servo have to be powered with a 5V DC source.The GUI can be accessed with a set of screen/keyboard/mouse or by SSH and VNC with a laptop.## UseAfter boot, the BBB can be access using a simple USB cable connected to a laptop running a VNC client such as Tight VNC Viewer. The address is `192.168.7.2` on port `5900`. The connection requires `X11VNC` to be installed on the board and a simple script to be executed (see folder Documents).The execution of `main.py` starts the software, including the GUI and the stepper driver module. The user has to make sure both arms are perfectly vertical before launching the drawing.Future improvement* Add Endstop micro-switches, allowing to perform an automated calibration of the arms’ position.* Try a small LCD touchscreen, freeing the operator from the constraint of using a laptop or a screen.* Improve the pivots could by replacing the 3D printed joints with real bearings.* Clear the command line script and make it compatible with the modifications introduced by the implementation of the GUI.* Change the configuration file format from `.py` to `.json` to allow saving of the parameters.## CreditsOriginal idea and the first version were developed by Jean-Luc Liardon and Marco Pagnamenta with the help of Pablo Garcia Del Valle, both three members of the Robopoly committee then.For the second version, the mechanics were designed by Loïs Bosson and Patrick Bobbink, the driver PCB by Yoann Lapijover and the software by Paul-Edouard Sarlin.