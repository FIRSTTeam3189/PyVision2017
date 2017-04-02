from serial import Serial
from BoxInfo import BoxInfo
import struct

PORT="/dev/ttyS0"
BAUDRATE=115200
TIMEOUT=3

class RoboSerial(object):
    def __init__(self):
        self._s = Serial(port=PORT, baudrate=BAUDRATE, timeout=TIMEOUT)
    def send(self, boxes, screen_width=640):
        has_boxes=True
        offset_x=0

        if boxes is None:
            has_boxes = False
        elif len(boxes) == 2:
            bi = BoxInfo(boxes)
            offset_x = int(bi.x_avg - screen_width/2)
        elif len(boxes) == 1:
            offset_x = int(reduce(lambda acc, point: acc+point[0], boxes[0], 0)/len(boxes[0]) - screen_width/2)
        else:
            has_boxes=False

        return self.send_raw(has_boxes, offset_x)

    def send_raw(self, has_box, point, prefix=0x77):
        box_flag = 0x01 if has_box else 0x00
        datar = bytearray()
        datar.extend(struct.pack("<4Bi", prefix, prefix, prefix, box_flag, int(point)))

        self._s.write(datar)
        return datar
