import board
import busio
import digitalio
import adafruit_max31856
from .exceptions import ThermocoupleError, OpenThermocoupleError

class Thermocouple:
    """ Thermocouple class to centrally handle error checking before distributing the temperature reading. """

    def __init__(self, cs_digital_pin_no=5, ignore_faults=False):
        """ 
            cs_digital_pin_no: GPIO Pin number on the R Pi which is connected to the CS channel on the adafruit_max31856
            ignore_faults: Whether or not to ignore errors reported by the chip. Will raise a ThermocoupleError exception if an error reported (and not ignored).
        """
        # Note whether to ignore faults
        self.ignore_faults = ignore_faults
        
        # TODO: Wrap this in a try/except block to handle PermissionErrors (and print a solution - add user to group that owns /dev/spidev0.*)
        # create a spi object
        spi = busio.SPI(board.SCK, board.MOSI, board.MISO)

        # allocate a CS pin and set the direction
        cs = digitalio.DigitalInOut(getattr(board, f'D{cs_digital_pin_no}'))
        cs.direction = digitalio.Direction.OUTPUT

        # create a thermocouple object with the above
        self.thermocouple = adafruit_max31856.MAX31856(spi, cs)

        # Check for any faults
        self.update_faults()

    def update_faults(self):
        """
            Read the current status of faults reported on the chip. 
            
            If not ignoring errors, raises a ThermocoupleError exception if any errors found.
        """
        self.faults = [fault for fault in self.thermocouple.fault if self.thermocouple.fault[fault]]
        if self.faults and not self.ignore_faults:
            raise ThermocoupleError(f"Warning: The thermocouple is reporting an error: {self.faults}")

    def get_faults(self):
        return self.faults

    def get_temperature(self):
        return self.thermocouple.temperature


if __name__ == '__main__':
    thermocouple = Thermocouple(5)
    # print the temperature!
    print(thermocouple.get_temperature())
