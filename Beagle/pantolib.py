import Adafruit_BBIO.PWM as PWM
a_min = 67.
duty0 = 3.
duty180 = 12.
a1_pin = "P9_14"
a2_pin = "P9_22"
t_pin = "P9_42"
ratio1 = (duty180-duty0)/180
offset1 = duty0 - a_min * ratio1
ratio2 = -ratio1
offset2 = duty180 - a_min * ratio2
pwm_f = 50
up_d = 105
down_d = 80
def Init():
	PWM.start(a1_pin, (duty180 + duty0)/2, pwm_f)
	PWM.start(a2_pin, (duty180 + duty0)/2, pwm_f)
	PWM.start(t_pin, ratio1 *  down_d + duty0, pwm_f)	
def GoTo(a1,a2):
	PWM.set_duty_cycle(a1_pin, ratio1 * a1 + offset1)
	PWM.set_duty_cycle(a2_pin, ratio2 * a2 + offset2)
def Up():
	PWM.set_duty_cycle(t_pin, ratio1 * up_d + duty0)
def Down():
	PWM.set_duty_cycle(t_pin, ratio1 * down_d + duty0)

		
