import RPi.GPIO as GPIO
from time import sleep

pin_no = 3
pwm_freq = 50 

GPIO.setmode(GPIO.BOARD)

GPIO.setup(pin_no, GPIO.OUT)
# setup PWM on pin #3 at 50Hz
pwm=GPIO.PWM(pin_no, pwm_freq)
# start it with 0 duty cycle so it doesn't set any angles on startup
pwm.start(0)

def set_angle(angle):
    duty = angle / 18 + 2
    GPIO.output(pin_no, True)
    pwm.ChangeDutyCycle(duty)
    sleep(1)
    GPIO.output(pin_no, False)
    pwm.ChangeDutyCycle(0)
