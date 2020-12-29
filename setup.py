from setuptools import setup

setup(name='pithonwy',
      version='0.1',
      description='Collection of scripts to run on Rasberry Pi(s) for GPIO/camera/etc.',
      url='http://github.com/Thonners/Pithonwy',
      author='Mathonwy Thomas',
      author_email='mathonwy.thomas@gmail.com',
      packages=['pithonwy', 'pithonwy.sensors','pithonwy.actuators','pithonwy.camera'],
      license='GPLv3',
      install_requires=[
        'RPi.GPIO',
        'pigpio',
      ],
      extras_require={
        'Camera':['picamera'],
        'Thermocouple':['adafruit-circuitpython-max31856'],
        'Gyro/Accelerometer':['adafruit-circuitpython-mpu6050'],
      },
      zip_safe=False)