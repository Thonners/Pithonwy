from setuptools import setup

setup(name='pithonwy',
      version='0.1',
      description='Collection of scripts to run on Rasberry Pi(s) for GPIO/camera/etc.',
      url='http://github.com/Thonners/Pithonwy',
      author='Mathonwy Thomas',
      author_email='mathonwy.thomas@gmail.com',
      license='GPLv3',
      packages=['pithonwy', 'pithonwy.sensors','pithonwy.motors','pithonwy.camera'],
      install_requires=[
        'adafruit-circuitpython-max31856',
        'RPi.GPIO',
        'pigpio',
        'picamera',
      ],
      zip_safe=False)