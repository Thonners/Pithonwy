"""
	Basic use of the camera module
	Instructions: https://projects.raspberrypi.org/en/projects/getting-started-with-picamera/7
"""

from picamera import PiCamera
from time import time, sleep

SAVE_PATH = '/home/thonners/images'
ROTATION = 180
WARMUP_TIME = 5 	# Length of time to let the camera adjust to the light 
IMG_RES = (2592, 1944)
VID_RES = (1920, 1080)
VID_FRAME_RATE = 15 # This is the max for the max video res

TIMELAPSE_INTERVAL = 60*5

def main():
    camera = PiCamera()
    # Set the res
    camera.resolution = IMG_RES
    camera.framerate = VID_FRAME_RATE
    # Set the rotation
    camera.rotation = ROTATION

    # Start a preview to let the camera adjust to the light (apparently)
    camera.start_preview()
    
#    camera.iso = 250
    
    
    # Wait for the automatic gain control to settle
    sleep(WARMUP_TIME)

    # Now fix the values
#    camera.shutter_speed = 8000 #camera.exposure_speed
#    camera.exposure_mode = 'off'
#    g = camera.awb_gains
#    camera.awb_mode = 'sunlight'
#    camera.awb_mode = 'off'
#    camera.awb_gains = g

    print(f'camera.exposure_speed = {camera.exposure_speed}, camera.shutter_speed = {camera.shutter_speed}, camera.exposure_mode = {camera.exposure_mode}, camera.awb_gains = {camera.awb_gains}')
#    counter = 2286 # Nasturtium count
    counter = 4047
    plant_type = "tomato"

    while True:
        full_path = '{}/{}_{:05d}.jpg'.format(SAVE_PATH, plant_type, counter)

        if camera.exposure_speed < 8000:
          # Limit exposure in case it's heavily backlit
          camera.shutter_speed = 8000
          camera.exposure_mode = 'off'

        camera.capture(full_path)
        print("Image saved to: {}".format(full_path))
        counter += 1

        # Turn it back to auto so we can check the values again on the next photo
        camera.exposure_mode = 'auto'

        sleep(TIMELAPSE_INTERVAL)



    camera.stop_preview()



if __name__ == '__main__':
    main()
