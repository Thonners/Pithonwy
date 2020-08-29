""" 
Motor class for driving a brushless motor via an ESC.

ENSURE THE BATTERY IS NOT CONNECTED UNTIL TOLD TO DO SO!

Also make sure the motor is in a safe condition to spin.

Initial script from https://www.instructables.com/id/Driving-an-ESCBrushless-Motor-Using-Raspberry-Pi/
"""

import time
from time import sleep
import pigpio

class Motor:

    def __init__(self, gpio_pin=4, esc_max_pulse_length=2000, esc_min_pulse_length=700):
        # Get an instance of the pigpio pi
        self.pi = pigpio.pi()
        # Details of which pin is used for PWM
        self.gpio_pin = gpio_pin
        # Max/min values
        self.max_value = esc_max_pulse_length
        self.min_value = esc_min_pulse_length
        # Set the PWM to 0 to start with so we're not armed
        self.pi.set_servo_pulsewidth(gpio_pin, 0)
        # Warning!
        print("Motor instance created. Please ensure the battery is currently DISCONNECTED")

    def arm(self):
        """ Sets the PWM ready for action (requires calibration to have been run at least once before) """
        self.pi.set_servo_pulsewidth(self.gpio_pin,self.min_value)
        print("ESC ready for battery connection now")

    def calibrate_esc(self):
        """ This is the auto calibration procedure of a Aerostar ESC """
        self.pi.set_servo_pulsewidth(self.gpio_pin, 0)
        print("Disconnect the battery and press Enter")
        inp = input()
        if inp == '':
            self.pi.set_servo_pulsewidth(self.gpio_pin, self.max_value)
            print("Connect the battery NOW.. you will here two beeps, then press Enter. (Note: you may need to do this within a time limit to enter calibration mode)")
            inp = input()
            if inp == '':            
                self.pi.set_servo_pulsewidth(self.gpio_pin,self.min_value)
                time.sleep(2)
                print("Aerostar ESC should now be configured.")
                # The rest of this was from the original instuctions... may or may not be generalisable?
                time.sleep(5)
                print( "Wait for it ....")
                time.sleep (5)
                print("Im working on it, DONT WORRY JUST WAIT.....")
                self.pi.set_servo_pulsewidth(self.gpio_pin, 0)
                time.sleep(2)
                print("Arming ESC now...")
                self.pi.set_servo_pulsewidth(self.gpio_pin, self.min_value)
                time.sleep(1)
                print("Calibration complete.")

    def set_motor_speed(self, speed):
        """ Set the speed to value between 0-1 (i.e. 0-100% of the max speed) """
        # Force the value to within the legal limits
        if speed < 0:
            speed = 0
        elif speed > 1:
            speed = 1
        # Calculate the required pulse width to achieve the speed
        pulse_width = self.min_value + speed*(self.max_value - self.min_value)
        # Set the speed
        self.pi.set_servo_pulsewidth(self.gpio_pin, pulse_width)

    def stop(self):
        """ Stops the motor from running """
        self.pi.set_servo_pulsewidth(self.gpio_pin, 0)
        print("Motor should have stopped (or at least be spinning down) now.\n\nIf not, unplug the battery NOW!")

    def spin_up(self,time=3, limit=0.5):
        increment = 0.001
        t_step_count = int(limit / increment)
        t_step_size = time / t_step_count
        for t_step in range(t_step_count):
            value = increment * t_step
            self.set_motor_speed(value)
            sleep(t_step_size)
        self.arm()

