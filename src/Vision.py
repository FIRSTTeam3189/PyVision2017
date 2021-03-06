import cv2, numpy , VisionProcessor, VisionConfiguration, FrameGrabbers
from BoxInfo import BoxInfo
from time import sleep
from StatusLights import StatusLights
from imutils.video import FPS
from SerialComm import RoboSerial
import subprocess
import sys
import traceback
import struct

ENABLE_UART = "echo | exec /var/opt/uart-enable/uart-enable"
print("Enabling UART")
out = subprocess.check_output(ENABLE_UART, shell=True)
print(out)
sleep(1)
print("Starting Vision...")

status = StatusLights()
config = VisionConfiguration.VisionConfiguration()
serial = RoboSerial()
status.set_starting_up(True)

def shutdown(error=0, blinks=10):
    status.set_running(False)
    status.set_starting_up(False)
                                             
    if error:
        for _ in xrange(blinks):
            status.set_crashed(True)
            sleep(.1)
            status.set_crashed(False)
            sleep(.1)

    # Release status lights and exit
    status.release()
    exit(error)

grabber = None

try:
    grabber = FrameGrabbers.MultithreadedFrameGrabber(config=config).start()
except Exception as e:
    traceback.print_exc()
    print(e)
    print("Failed to setup grabber")
    shutdown(1, 10)

while grabber.current_frame is None:
    continue
   
loops = 0
fails = 0
should_shutdown = False

try:
    # Set running light on, startup off
    status.set_running(True)
    status.set_starting_up(False)
    
    while not should_shutdown:
        # Process image read
        frame = grabber.current_frame
        if frame is None:
            fails += 1
            sleep(.1)
            if fails > 200:
                shutdown(2, 6)
            continue
        boxes = VisionProcessor.process_image(frame, config)

        # Send how many images processed, and send how many boxes found
        loops += 1

        # See if we should shut down
        should_shutdown = False

        if loops % 100 == 0:
            print loops

        if config.show_image:
            frame = VisionProcessor.draw_box_info(frame, boxes)
            cv2.imshow('Original', frame)
            if cv2.waitKey(1) & 0xff == ord("q"):
                break
    
        serial.send(boxes)
            
except Exception as e:
    traceback.print_exc()
    print(e)
    grabber.stop()
    shutdown(69, 3)

if config.show_image:
    cv2.destroyAllWindows()
grabber.stop()
status.release()
sleep(.5)
