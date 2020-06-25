""" Assumes the Adafruit MPU 6050 """
import board
import busio
import adafruit_mpu6050

class Gyro:
    """ Gyro class for both rotational and linear acceleration measurements """

    def __init__(self):
        i2c = busio.I2C(board.SCL, board.SDA)
        self.mpu = adafruit_mpu6050.MPU6050(i2c)

    def get_acceleration(self):
        return self.mpu.acceleration

    def get_gyro(self):
        return self.mpu.gyro

    def get_temperature(self):
        return self.mpu.temperature
