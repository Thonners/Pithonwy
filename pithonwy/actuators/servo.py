""" Servo class for setting the position of a standard servo """
import time
import pigpio

class Servo:
    def __init__(self, gpio_pwm_pin=17, pwm_freq=50, duty_cycle_min=500, duty_cycle_max=2500):
        # Get an instance of the pigpio pi
        self.pi = pigpio.pi()
        # Details of which pin is used for PWM
        self.gpio_pwm_pin = gpio_pwm_pin
        # Max/min values
        self.min_value = duty_cycle_min
        self.max_value = duty_cycle_max
        # Set the position to the middle to begin with
        self.set_position(0)
    def set_position(self, angle):
        """
            Sets the position of the servo to 'angle' (in degrees), assuming range -90 <= angle <= 90.
            If the given angle is outside the range, the angle will be converted to the equivalent value within the range
        """
        # Switch to using range 0 - 360, as we'll use that % to go between min and max pulse lengths (which correspond to -180 -> +180 respectively)
        angle += 90
        # Ensure the angle is within the required range
        while angle < 0:
            angle += 180
        if angle > 180:
            angle = angle % 180
        # Turn the angle into a % so we can calculate the pulse width
        angle_pc = angle / 180
        pulse_width = angle_pc * (self.max_value - self.min_value) + self.min_value
        # Set the pulse width
        self.pi.set_servo_pulsewidth(self.gpio_pwm_pin, pulse_width)
