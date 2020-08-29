""" Assumes the Adafruit MPU 6050 """
import board
import busio
import adafruit_mpu6050
from time import sleep

class Gyro:
    """ Gyro class for both rotational and linear acceleration measurements """

    def __init__(self):
        i2c = busio.I2C(board.SCL, board.SDA)
        self.mpu = adafruit_mpu6050.MPU6050(i2c)
    
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
        return self.mpu.gyro

    def get_temperature(self):
        return self.mpu.temperature
