from picamera2 import Picamera2
from threading import Thread
import time

class VideoStream:
    def __init__(self, resolution=(480, 360), framerate=5):
        self.camera = Picamera2()
        self.camera.configure(self.camera.create_preview_configuration(main={"size": resolution}))
        self.camera.start()

        self.frame = None
        self.stopped = False

        # Start a thread to continuously capture frames
        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()

    def update(self):
        # Continuously capture frames until stopped
        while not self.stopped:
            self.frame = self.camera.capture_array()
            time.sleep(1 / 15)  # Limit the capture rate to the desired framerate

    def read(self):
        # Return the latest frame
        return self.frame

    def stop(self):
        # Stop the camera and thread
        self.stopped = True
        self.thread.join()
        self.camera.close()
