#!/usr/bin/python2
#GPIOControl test v5
#Richard McGregor 2014-10 Deepfriedice@gmail.com

import time
import GPIOControl

def foobar(ev):
	print "received: " + str(ev)



#These numbers are for my system, you'll need to fill in the GPIO numbers you are using.
a = GPIOControl.LED_controller(17)
b = GPIOControl.LED_controller(18)
c = GPIOControl.Button_controller(21, 5, foobar, debug=True)			#button with debugging
d = GPIOControl.Button_controller(22, 5, GPIOControl.isolate(foobar))	#button with thread-isolated callbacks


#30 second LED test pattern
a.heartbeat(2,45,40)
b.set_state(True)
time.sleep(5)
b.set_state(False)
time.sleep(5)
b.blink(1,0.5)
time.sleep(20)


#time.sleep(60)

GPIOControl.cleanup()

#Dump the contents of GPIOControl.event_queue
events = []
while not GPIOControl.event_queue.empty(): #Note this isn't generally safe to do.
	events.append(str(GPIOControl.event_queue.get()))
print
print "Events Queue:"
print events
