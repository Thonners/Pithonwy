"""
	Basic use of the camera module
	Instructions: https://projects.raspberrypi.org/en/projects/getting-started-with-picamera/7
"""

from picamera import PiCamera
from time import time, sleep

class Camera:
    # TODO: Make this a subclass of PiCamera instead?

    def __init__(self, image_resolution=(2592, 1944), video_framerate=15, rotation=180, warmup_time=5):
        """ Create the camera instance
            - image_resolution: Resoultion for still image capture. Default = (2592, 1944) (the max for the standard camera module)
            - video_framerate: Framerate for video capture. Default = 15 = max frame rate for max video res
            - rotation: The rotation (in degrees) to apply to the feed. Default = 180 deg
            - warmup_time: The amount of time (in seconds) to wait for the camera to come online. Default=5s
        """
        self.camera = PiCamera()
        # Set the res
        self.camera.resolution = image_resolution
        self.camera.framerate = video_framerate
        # Set the rotation
        self.camera.rotation = rotation
        # Start a preview to let the camera adjust to the light (apparently)
        self.camera.start_preview()
        # Wait for the automatic gain control to settle
        sleep(warmup_time)

    def capture(self, output_path):
        self.camera.capture(output_path)

    def stop_camera(self):
        self.camera.stop_preview()

    def __str__(self):
        output_str = ('Pithonwy Camera instance:' + '\n' + 
                        f'Input settings:' + '\n' + 
                        f'\tImage Resolution = {self.camera.resolution},' + '\n' + 
                        f'\tVideo Framerate  = {self.camera.framerate}, ' + '\n' + 
                        f'\tRotation         = {self.camera.rotation}, ' + '\n' + 
                        f'Current auto-settings:' + '\n' + 
                        f'\tcamera.exposure_speed = {self.camera.exposure_speed},' + '\n' + 
                        f'\tcamera.shutter_speed  = {self.camera.shutter_speed}, ' + '\n' + 
                        f'\tcamera.exposure_mode  = {self.camera.exposure_mode}, ' + '\n' + 
                        f'\tcamera.awb_gains      = {self.camera.awb_gains}' + '\n')
        return output_str
    

class TimelapseCamera(Camera):

    def __init__(self, time_interval, output_path, output_filename_stem, starting_image_index=0, image_resolution=(2592, 1944), video_framerate=15, rotation=180, warmup_time=5):
        """ Creates a timelapse camera instance

            - time_interval: Time in seconds between images
            - output_path: The directory into which the images should be saved
            - output_filename_stem: The first part of the filename to save the images to. They'll be suffixed by their image index number
            - starting_image_index: The number to be used for the first image. All subsequent images will be invcremented from there
        """
        print("Creating a TimelapseCamera instance... ")
        super().__init__(image_resolution, video_framerate, rotation, warmup_time)
        self.time_interval = time_interval
        # TODO: Check these aren't null
        self.output_path = output_path
        self.output_filename_stem = output_filename_stem
        # Initialise the counter
        self.counter = starting_image_index
        # Show some output to give the user feedback about what they've just created
        print(self)

    def __str__(self):
        """ Human readable output describing the TimelapseCamera """
        output_str = ("\nTimelapseCamera instance: \n" + 
                        f"\tTime Interval (s)  : {self.time_interval}" + "\n" + 
                        f"\tOutput Path        : {self.output_path}" + "\n" + 
                        f"\tFilename Stem      : {self.output_filename_stem}" + "\n" + 
                        f"\tCurrent Image Count: {self.counter}" + "\n")
        return output_str

    def start_timelapse(self):
        # Init the 'timelapse_running' variable
        timelapse_running = True
        try:
            while timelapse_running:
                # TODO: Get next available image - check whether the current a file for the current count exists or not and increment / add more variables to determine whether to overwrite or not
                full_path = '{}/{}_{:05d}.jpg'.format(self.output_path, self.output_filename_stem, self.counter)

                if self.camera.exposure_speed < 8000:
                    # Limit exposure in case it's heavily backlit
                    self.camera.shutter_speed = 8000
                    self.camera.exposure_mode = 'off'

                self.capture(full_path)
                print("Image saved to: {}".format(full_path))
                self.counter += 1

                # Turn it back to auto so we can check the values again on the next photo
                self.camera.exposure_mode = 'auto'

                sleep(self.time_interval)
        except KeyboardInterrupt:
            print("\nKeyboardInterrupt caught, stopping the timelapse.")
            print(f"We've taken {self.counter} pictures!")
            self.stop_camera()


if __name__ == '__main__':
    tlc = TimelapseCamera(60*5, '/home/thonners/images', 'birdwatching', 1)
    tlc.start_timelapse()