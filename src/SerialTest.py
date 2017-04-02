from SerialComm import RoboSerial
from time import sleep

s = SerialComm()

i = 0
while i < 100:
    s.send_raw(i%2==0, i*10)
    sleep(.5)
