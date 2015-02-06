#!/usr/bin/python2
#GPIOControl v5
#Richard McGregor 2014-10 Deepfriedice@gmail.com

import RPIO
import RPi.GPIO

import heapq
import math
import Queue
import threading
import time

class Button_event:
	def __init__(self, gpio_pin, event_type):
		self.gpio_pin = gpio_pin
		self.event_type = event_type
	def __str__(self):
		return "{} on pin {}".format(self.event_type, self.gpio_pin)


class Button_controller:
	def __init__(self, gpio_pin, debounce, handler, debug=False):
		
		with controller_lock:
			if gpio_pin not in controllers:
				controllers[gpio_pin] = self
			else:
				print "Already exists!" #TODO Handle duplicates
		
		self.gpio_pin = gpio_pin
		self.debounce = debounce / 1000.0
		self.handler = handler
		self.debug = debug
		
		self.state = False
		self.last_high = 0
		self.debounced_state = False
		
		self.interrupt_queue = Queue.Queue()
		self.control_thread = threading.Thread(target=self.direct_controller)
		self.control_thread.daemon = True
		self.control_thread.start()
		
		#FIXME PWM interferes with pull-down behaviour when multiple buttons are pressed
		#if pull_dir.lower() == "up":
		#	r_pull_dir = RPIO.PUD_UP
		#	self.invert = True
		#else:
		#	r_pull_dir = RPIO.PUD_DOWN
		#	self.invert = False
		r_pull_dir = RPIO.PUD_DOWN
		
		RPIO.setup(gpio_pin, RPIO.IN, pull_up_down=r_pull_dir)
		RPIO.add_interrupt_callback(gpio_pin, self.handle_interrupt, pull_up_down=r_pull_dir)
	
	
	def handle_interrupt(self, gpio_pin, value):
		now = time.time()
		new_state = bool(value)
		
		#ignore repeated interrupts
		if new_state == self.state:
			return
		self.state = not self.state
		
		#debounce highs
		if new_state == True:
			if now < self.last_high + self.debounce:
				return
			else:
				self.last_high = now
			
		#ignore repeated debounced interrupts
		if new_state == self.debounced_state:
			return
		self.debounced_state = not self.debounced_state
		
		self.interrupt_queue.put((now, new_state))
	
	
	def direct_controller(self):
		tolerance = 0.01 #How close is good enough
		running = True
		sleep_time = 0
		default_sleep = 10
		click_count = 0 # number of clicks detected before sending event
		events = [] #events that are going to occur
		
		while running:
			
			#Wait sleep_time seconds unless interrupted
			try:
				interrupt = self.interrupt_queue.get(True, sleep_time)
			except Queue.Empty:
				interrupt = None
			
			
			if interrupt == None: #if there wasn't an interrupt
				
				#deal with the next scheduled event
				if len(events) > 0 and events[0][0] - time.time() <= tolerance:
					event = heapq.heappop(events)
					text = event[1]
					
					#determine if this was a double or triple click
					if event[1] == "click":
						text = self.calc_click_type(click_count)
						click_count = 0
						
					#make repeat events actually repeat
					elif event[1] == "repeat":
						heapq.heappush(events, (event[0]+C_TIME_REPEAT, "repeat") )
					
					send_event(Button_event(self.gpio_pin, text), self.handler)
			
			
			elif interrupt[1] == True: #On Click
				click_count += 1
				
				if self.debug:
					print "High:", click_count, "on pin", self.gpio_pin
				
				now = interrupt[0]
				
				#don't change the send time if a click is already in progress
				send_click_time = now + C_TIME_BETWEEN_CONSECUTIVE_CLICKS
				for event in events:
					if event[1] == "click":
						send_click_time = event[0]
				
				#Recreate scheduled events
				events = [
					(send_click_time, "click"),
					(now + C_TIME_LONG1, "long_hold"),
					(now + C_TIME_LONG2, "very_long_hold"),
					(now + C_TIME_REPEAT, "repeat"),
				]
				heapq.heapify(events)
			
			
			elif interrupt[1] == False: #On Release
				if self.debug:
					print "Low on pin", self.gpio_pin
				
				#filter out any scheduled events the require the button to be held
				new_events = []
				for event in events:
					if event[1] == "click":
						new_events.append(event)
				events = new_events
			
			
			else: #Kill the controler on shutdown
				running = False
			
			
			#Finally, determine how long to sleep for until the next event
			if len(events) == 0:
				sleep_time = default_sleep
			else:
				sleep_time = max(0, events[0][0]-time.time())
			
			
			
	def calc_click_type(self, click_count):
		text = ""
		
		#generate the appropriate click event
		if click_count == 1:
			text = "click"
		elif click_count == 2:
			text = "doubleclick"
		elif click_count == 3:
			text = "tripleclick"
		elif click_count >= 4:
			text = "multiclick"
		else:
			print self.presses
			print "Something has gone wrong!"
			text = "ERROR"
		
		return text
	
	def cleanup(self):
		self.interrupt_queue.put("KILL")
		self.control_thread.join()
		#RPIO.del_interrupt_callback(self.gpio_pin) #FIXME


class LED_controller:
	def __init__(self, gpio_pin):
		
		with controller_lock:
			if gpio_pin not in controllers:
				controllers[gpio_pin] = self
			else:
				print "Already exists!" #TODO Handle duplicates
		
		self.gpio_pin = gpio_pin
		RPi.GPIO.setup(gpio_pin, RPi.GPIO.OUT)
		
		self.direct_controller = None
		self.direct_controller_kill = None
		
		self.state = "OFF"   # valid: "OFF" "ON" "BLINK" "HEART"
		self.set_state(False)
	
	def set_state(self, turn_on):
		self.stop()
		if turn_on:
			self.state = "ON"
			RPi.GPIO.output(self.gpio_pin, RPi.GPIO.HIGH)
		else:
			self.state = "OFF"
			RPi.GPIO.output(self.gpio_pin, RPi.GPIO.LOW)
	
	def toggle(self):
		self.set_state(self.state == "OFF")
	
	#start a blink direct_control thread
	def blink(self, timeOn, timeOff):
		self.stop()
		kill = threading.Event()
		self.direct_controller_kill = kill
		self.direct_controller = threading.Thread(target=self.direct_blink, args=(timeOn, timeOff, kill))
		self.direct_controller.daemon = True
		self.direct_controller.start()
	
	#start a heatbeat direct_control thread
	def heartbeat(self, period, steps, pwm_rate):
		self.stop()
		kill = threading.Event()
		self.direct_controller_kill = kill
		self.direct_controller = threading.Thread(target=self.direct_heartbeat, args=(period, steps, pwm_rate, kill))
		self.direct_controller.daemon = True
		self.direct_controller.start()
	
	#kills the current direct_control thread (if it exists)
	def stop(self):
		if self.direct_controller:
			self.direct_controller_kill.set()
			self.direct_controller.join()
			self.direct_controller = None
			self.direct_controller_kill = None
	
	def direct_blink(self, timeOn, timeOff, kill):
		#setup
		self.state = "BLINK"
		on = False
		RPi.GPIO.output(self.gpio_pin, RPi.GPIO.LOW)
		sleep_time = timeOff
		
		#Blink until killed
		while not kill.wait(sleep_time):
			if on:
				on = False
				RPi.GPIO.output(self.gpio_pin, RPi.GPIO.LOW)
				sleep_time = timeOff
			else:
				on = True
				RPi.GPIO.output(self.gpio_pin, RPi.GPIO.HIGH)
				sleep_time = timeOn
	
	def direct_heartbeat(self, period, steps, pwm_rate, kill): 
		#setup
		self.state = "BLINK"
		step_count = 0
		update_interval = float(period) / steps
		pwm = RPi.GPIO.PWM(self.gpio_pin, pwm_rate)
		pwm.start(0)
		
		#pulse until killed
		while not kill.wait(update_interval):
			phase = (2*math.pi) * (float(step_count)/steps)
			brightness = (1 + math.sin(phase)) * 50
			pwm.ChangeDutyCycle(brightness)
			step_count = (step_count+1) % steps
		
		pwm.stop()

	def cleanup(self):
		self.stop()
		RPi.GPIO.cleanup(self.gpio_pin)


#Neatly pass an event to a handler and append the event to a queue
def send_event(event, handler):
	try:
		event_queue.put_nowait(event)
		for i in range(event_queue.qsize()-C_QUEUE_LENGTH):
			event_queue.get_nowait()
	except (Queue.Empty, Queue.Full):
		pass
	
	handler(event)

#Take a handler function, and return a "handler wrapper" that will
#call the hanlder function with an argument in a new thread.
#This should be used to avoid doing heavy work in the callback threads.
def isolate(handler):
	def wrapper(event):
		threading.Thread(target=handler, args=[event]).start()
	return wrapper

#Call after using this library
def cleanup():
	with controller_lock:
		for controller in controllers.values():
			controller.cleanup()
	RPIO.cleanup()


C_TIME_BETWEEN_CONSECUTIVE_CLICKS = 0.3
C_TIME_LONG1                      = 0.5
C_TIME_LONG2                      = 1.5
C_TIME_REPEAT                     = 0.75
C_QUEUE_LENGTH                    = 100

RPIO.setmode(RPIO.BCM)
RPi.GPIO.setmode(RPIO.BCM)

event_queue = Queue.Queue()

controller_lock = threading.Lock()
controllers = {}

RPIO.wait_for_interrupts(threaded=True)
