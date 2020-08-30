""" Assumes the Adafruit MPU 6050 """
import board
import busio
import adafruit_mpu6050
from time import sleep

class Gyro:
    """ Gyro class for both rotational and linear acceleration measurements """

    def __init__(self, normalise_rates=False, gyro_normalisation_values=[1,1,1], acceleration_normalisation_values=[1,1,1]):
        """
            Constructor for a Gyro object

            Parameters:
                gyro_normalisation_values: array            The raw value at which the normalised rate = 1. Default=[1,1,1] implies raw values are returned
                acceleration_normalisation_values: array    The raw value at which the normalised rate = 1. Default=[1,1,1] implies raw values are returned
        """
        i2c = busio.I2C(board.SCL, board.SDA)
        self.mpu = adafruit_mpu6050.MPU6050(i2c)
        self.normalise_rates = normalise_rates
        self.gyro_normalisation_values = gyro_normalisation_values
        self.acceleration_normalisation_values = acceleration_normalisation_values
    
    def calibrate(self):
        """ Calibrates the readings when the gyro is stationary, so it can be properly 'zeroed' """
        print("Calibrating Gyro. Please ensure the device is stationary, and the axes are aligned X forward, Y left, Z up")
        print("Calbration starting in 3... ", end="")
        sleep(1)
        print("2... ", end="")
        sleep(1)
        print("1... ", end="")
        sleep(1)
        print("Calibration starting. Please keep the accelerometer completely stationary.")
        #TODO: Write the jazz here to zero the readings

    def get_acceleration(self):
        return self.mpu.acceleration

    def get_gyro(self):
        gyro = self.mpu.gyro
        normalised_gyro = [gyro[i] / self.gyro_normalisation_values[i] for i in range(3) ]
        return normalised_gyro

    def get_temperature(self):
        return self.mpu.temperature
