# Pithonwy
Collection of scripts to provide a nicer interface to breakouts on Rasberry Pi(s)

## Installation
Ensure Camera, SPI & I2C interfaces are enabled in raspi-config
If permissions errors are experienced when trying to access /dev/spidev0.[0-1] or /dev/i2c-1, copy the pithonwy.rules file in ./udev/ to /etc/udev/rules.d/.
Reload the udev rules with: `udevcontrol --reload && udevcontrol --trigger`
Ensure your user belongs to the 'spi', 'i2c', 'mem' (& 'kmem') groups. (You may need to create the spi & i2c groups if they doesn't exist)

### Other requirements
Optional dependencies requried for various sensors/actuators/etc. The supported breakouts are:
Gyro: Adafruit MPU6050
Thermocouple: Adafruit MAX31856

To use other versions, simply install the relevant circuit-python packages and update the `import ` statements in the appropriate script.
