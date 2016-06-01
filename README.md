# The PantoDraw

The Pantodraw is a device capable of drawing the portrait of people interacting with it. 

As visitors always enjoy interacting with robots when visiting Robopoly’s booth at EPFL events, the goal of this project is to give them the opportunity to spend a pleasant time being drawn by a robot-like device. 
* A6 paper
| Name | Pin |
| --- | --- | 
| Driver Data | P9_11 |

The Vbat pin of the driver has to be connected to a DC source which will provide the power for the motors. No exact value is needed since the IC performs a current chop regulation, but there are some conditions: if Vbat is too low, current ramp will be too slow and steps could be missed, but, if V_bat is too high, the driver will dissipate too much heat and its internal thermal shutdown will quickly activate. 20V seems to be working well.