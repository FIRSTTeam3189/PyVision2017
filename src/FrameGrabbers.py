import cv2
import numpy as np
from time import sleep
from threading import Thread


READ_FAILS_TIL_SHUTDOWN = 10

class MultithreadedFrameGrabber(object):
    def __init__(self, port=0, config=None):
        self.port = port
        self.config = config
        self.stream = cv2.VideoCapture(port)
        fails = 0
	while not self.stream.isOpened():
            print("Stream could not open")
            fails += 1
            if fails > 50:
                raise RuntimeError("Failed to open stream")
            try:
                self.stream.release()
                self.stream = cv2.VideoCapture(port)
                sleep(.1)
            except:
                pass
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.stream.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0)
        self.stream.set(cv2.CAP_PROP_FPS, 20)
        
        if config is None:
            self.stream.set(cv2.CAP_PROP_EXPOSURE, 0.69)
            self.stream.set(cv2.CAP_PROP_CONTRAST, 0.69)
            self.stream.set(cv2.CAP_PROP_WHITE_BALANCE_BLUE_U, 0.69)
            self.stream.set(cv2.CAP_PROP_WHITE_BALANCE_RED_V, -0.69)
            self.stream.set(cv2.CAP_PROP_BRIGHTNESS, -0.69)
        else:
            self.stream.set(cv2.CAP_PROP_EXPOSURE, config.exposure)
            self.stream.set(cv2.CAP_PROP_CONTRAST, config.contrast)
            self.stream.set(cv2.CAP_PROP_WHITE_BALANCE_BLUE_U, config.white_balance_blue)
            self.stream.set(cv2.CAP_PROP_WHITE_BALANCE_RED_V, config.white_balance_red)
            self.stream.set(cv2.CAP_PROP_BRIGHTNESS, config.brightness)
            
        self.grabbed, self.frame = self.stream.read()
        self.read_fails = 0
        self.should_stop = False

    def stop(self):
        self.should_stop = True

    def sync_camera_props(self):
        if self.config is not None:
            self.config.exposure = np.clip(self.stream.get(cv2.CAP_PROP_EXPOSURE), -1, 1)
            self.config.contrast = np.clip(self.stream.get(cv2.CAP_PROP_CONTRAST), -1, 1)
            self.config.white_balance_blue = np.clip(self.stream.get(cv2.CAP_PROP_WHITE_BALANCE_BLUE_U), -1, 1)
            self.config.white_balance_red = np.clip(self.stream.get(cv2.CAP_PROP_WHITE_BALANCE_RED_V), -1, 1)
            self.config.brightness = np.clip(self.stream.get(cv2.CAP_PROP_BRIGHTNESS), -1, 1)

        
    def start(self):
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        while not self.should_stop:
            (self.grabbed, self.frame) = self.stream.read()

            if not self.grabbed:
                self.read_fails += 1
            else:
                self.read_fails = 0

            if self.read_fails > READ_FAILS_TIL_SHUTDOWN:
                self.stop()

        self.stream.release()

    @property
    def current_frame(self):
        return self.frame
    
