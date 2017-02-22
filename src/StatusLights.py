import RPi.GPIO as gpio

RUNNING_PIN = 12
STARTING_UP_PIN = 26
CRASH_PIN = 16

class StatusLights(object):
    def __init__(self):
        gpio.setmode(gpio.BCM)
        gpio.setup(RUNNING_PIN, gpio.OUT)
        gpio.setup(STARTING_UP_PIN, gpio.OUT)
        gpio.setup(CRASH_PIN, gpio.OUT)

    def set_running(self, value):
        gpio.output(RUNNING_PIN, bool(value))

    def set_starting_up(self, value):
        gpio.output(STARTING_UP_PIN, bool(value))

    def set_crashed(self, value):
        gpio.output(CRASH_PIN, bool(value))

    def release(self):
        self.set_running(False)
        self.set_starting_up(False)
        self.set_crashed(False)
        gpio.cleanup()
