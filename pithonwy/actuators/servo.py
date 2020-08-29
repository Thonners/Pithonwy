""" Servo class for setting the position of a standard servo """
import time
import pigpio

class Servo:
    def __init__(self, gpio_pin:int=17, duty_cycle_min:int=500, duty_cycle_max:int=2500, increment_delta:int = 1, centre_offset:int=0, invert_up_down:bool = False):
        """ Servo class
            gpio_pin: The GPIO pin number into which the servo is connected (Note this is the GPIO number, not just the pin number)
            increment_delta: The amount by which to change the angle when incrementing/decrementing its position
            invert_up_down: Boolean, whether to invert the signal instructions (i.e. swap the definition of -90/+90 for the position)
        """
        # Get an instance of the pigpio pi
        self.pi = pigpio.pi()
        # Details of which GPIO pin is used for the servo control
        self.gpio_pin = gpio_pin
        # Max/min values
        self.min_value = duty_cycle_min
        self.max_value = duty_cycle_max
        # Note the offset requried for calibration
        self.offset = centre_offset
        # Set the position to the middle to begin with (note the offset will be applied during the 'set_position' call)
        self.set_position(0)
        # Store whether we need to invert the signal instructions
        self.invert = invert_up_down
        self.delta = increment_delta
    def set_position(self, angle):
        """
            Sets the position of the servo to 'angle' (in degrees), assuming range -90 <= angle <= 90 and stores the 'current_position'.
            If the given angle is outside the range, the angle will be converted to the equivalent value within the range.
            Applies any relevant offset required according to this servo's calibration to the signal transparently
        """
        # Switch to using range 0 - 360, as we'll use that % to go between min and max pulse lengths (which correspond to -180 -> +180 respectively)
        angle += 90
        # Ensure the angle is within the required range
        while angle < 0:
            angle += 180
        if angle > 180:
            angle = angle % 180
        # Only apply the offset to the signal, so we don't corrupt the demand with the offset (otherwise we'd set it to 0 and its 'current position' will be =offset)
        # Turn the angle into a % so we can calculate the pulse width
        angle_pc = (angle + self.offset) / 180
        pulse_width = angle_pc * (self.max_value - self.min_value) + self.min_value
        # Set the pulse width
        self.pi.set_servo_pulsewidth(self.gpio_pin, pulse_width)
        # Store the current position (remove the 90 so we're back to using the -90 --> +90 range)
        self.current_position = angle - 90
    def centre(self):
        """ Centres the servo """
        self.set_position(0)
    def increment(self, delta = None):
        if delta == None:
            delta = self.delta
        # Get the new angle - multiply the delta by -1 ** invert, as this will = +1 if invert = False, -1 if invert = True
        new_angle = self.current_position + self.delta * ((-1)**self.invert)
        self.set_position(new_angle)
    def decrement(self, delta = None):
        if delta == None:
            delta = self.delta
        # Get the new angle - multiply the delta by -1 ** invert, as this will = +1 if invert = False, -1 if invert = True
        new_angle = self.current_position - self.delta * ((-1)**self.invert)
        self.set_position(new_angle)
        