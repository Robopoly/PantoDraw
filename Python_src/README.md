# Software

<img align=“center” src="https://github.com/Robopoly/PantoDraw/blob/version_2/GUI_src/gui_screenshot_2.jpg" width=“10”>

The core application is built around a Finite State Machine (FSM) composed of six states:
* State 1: the starting picture of the software.
* State 2: the acquisition of the image (capture from camera or import from a file on disk).
* State 3: contour detection using the Canny algorithm.
* State 4: path computation and optimisation with display of the different trajectories with various colours.
* State 5: drawing of the result.
* State 6: drawing is finished!


The FSM is directly managed by Qt, running with `main.py`. All the image processing algorithms and OpenCV tools are run in `imageprocessing.py`, which then controls the motor interface (`pantolib_stepper.py` and `stepper.py`).

To ensure that interactions with the GUI are smooth enough even during heavy processing phases, the computations are performed in a separate thread using Python native threading library. The GUI is continuously updated during these phases using `get` functions from the processing module.

Parameters which can be modified by a configuration dialog window in the main application are stored in the `config.py` file and can be easily accessed by the other modules.