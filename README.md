# Pithonwy
Collection of scripts to run on Rasberry Pi(s)

## Installation
If permissions errors are experienced when trying to access /dev/spidev0.[0-1] or /dev/i2c-1, copy the pithonwy.rules file in ./udev/ to /etc/udev/rules.d/.
Reload the udev rules with: `udevcontrol --reload && udevcontrol --trigger`
Ensure your user belongs to the 'spi' group. (You may need to create this group if it doesn't exist)
