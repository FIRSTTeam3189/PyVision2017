from SerialComm import RoboSerial
from binascii import hexlify
from time import sleep

s = RoboSerial()

i = 0
while i < 200:
    print("Sending has_boxes: %s point: %d" % (str(i%2==0), i*10-1000))
    ba = s.send_raw(i%2==0, i*10-1000)
    print(hexlify(ba))
    sleep(.5)
    i+=1
