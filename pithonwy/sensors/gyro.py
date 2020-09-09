""" Assumes the Adafruit MPU 6050 """
import board
import busio
import adafruit_mpu6050
from time import sleep
from threading import Thread, Timer

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
        # Initialise calibration stuff
        self._calibrating = False
        self.calibration_gyro = (0,0,0)
        self.calibration_acc = (0,0,0)
    
    def calibrate(self, min_timestep:float = 0.01, calibration_time:float = 3, max_readings_count:int = 1000):
        """ Calibrates the readings when the gyro is stationary, so it can be properly 'zeroed' """
        if self._calibrating:
            print("Calibration already running. Please wait for it to finish before running calibration again")
            return
        # Get the timestep
        timestep = max(min_timestep, calibration_time / max_readings_count)
        timestep_count = min(max_readings_count, calibration_time / timestep)
        # Start a separate thread to take the calibration readings so we don't block the main thread
        self.calibration_thread = Thread(target=self._take_calibration_readings, daemon=True, args=(self, timestep, timestep_count))
        self.calibration_thread.start()

    def _take_calibration_readings(self, timestep:float, n_timesteps:int, countdown:bool=True):
        """ Takes continual readings which can be used for calibration """
        self._calibrating = True   # Make a note that this is currently running so we can't try to run it again
        print("Calibrating Gyro. Please ensure the device is stationary, and the axes are aligned X forward, Y left, Z up")
        if countdown:
            print("Calbration starting in 3... ", end="")
            sleep(1)
            print("2... ", end="")
            sleep(1)
            print("1... ", end="")
            sleep(1)
            print("Calibration starting. Please keep the accelerometer completely stationary.")
        gyro_readings = []
        acc_readings = []
        # Take the readings
        for i in range(n_timesteps):
            gyro_readings.append(self.get_gyro())
            acc_readings.append(self.get_acceleration())
            sleep(timestep)
        # Get the averages
        gyro_mean = sum(gyro_readings) / n_timesteps
        acc_mean = sum(acc_readings) / n_timesteps
        # Store gyro means for use in correcting the values
        self.calibration_gyro = gyro_mean
        self.calibration_acc = acc_mean

    def get_acceleration(self):
        acc_raw = self.mpu.acceleration
        acc_calibrated = (acc_raw[0] - self.calibration_gyro[0],acc_raw[1] - self.calibration_gyro[1],acc_raw[2] - self.calibration_gyro[2])
        return acc_calibrated

    def get_gyro(self):
        gyro = self.mpu.gyro
        normalised_gyro = [gyro[i] / self.gyro_normalisation_values[i] for i in range(3) ]
        return normalised_gyro

    def get_temperature(self):
        return self.mpu.temperature
