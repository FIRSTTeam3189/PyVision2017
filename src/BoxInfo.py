import cv2
import numpy as np
import numpy.linalg as la
import math

PIXEL_HEIGHT_CONST = 150.0 # In Pixels
DISTANCE_CONST = 2 # In Feet
TAPE_WIDTH = 2.0 # In Inches
CAM_FOVY = 34.3 # In Degrees
CAM_FOVX = 61 # In Degrees

class BoxInfo(object):
    def __init__(self, boxes):
        if len(boxes) != 2:
            raise ValueError('len of box doesnot equal 2')

        # Find center line between boxes
        x_sum = 0
        for box in boxes:
            for point in box:
                x_sum += point[0]

        self._x_avg = x_sum / 8
        
        p1= boxes[0][0]
        p2= boxes[1][0]

        # Find left and right box
        if p1[0]>p2[0]:
            left_box = boxes[1]
            right_box = boxes[0]
        else:
            left_box = boxes[0]
            right_box = boxes[1]

        # Find inner left and inner right edges and distance
        inner_left_points = sorted(left_box, cmp=lambda x,y: y[0]-x[0])
        inner_right_points = sorted(right_box, cmp=lambda x,y : x[0]-y[0])

        self._inner_left_x = (inner_left_points[0][0] + inner_left_points[1][0])/2
        self._inner_right_x = (inner_right_points[0][0] + inner_right_points[1][0])/2

        # Box Inner Height (bih)
        bih_one = abs(inner_left_points[0][1] - inner_left_points[1][1])
        bih_two = abs(inner_right_points[0][1] - inner_right_points[1][1])
        if  bih_one > bih_two:
            bigger_box = inner_left_points
        else:
            bigger_box = inner_right_points

        self._bigger_box_height = abs(bigger_box[0][1] - bigger_box[1][1])

        # Grab bigger box inner and outer height
        inner_bb_height = float(self._bigger_box_height)
        outer_bb_height = float(abs(bigger_box[2][1] - bigger_box[3][1]))
        if inner_bb_height > outer_bb_height:
            bigger_height = inner_bb_height
            smaller_height = outer_bb_height
        else:
            bigger_height = outer_bb_height
            smaller_height = inner_bb_height

        # Find distances, in inches
        a = (PIXEL_HEIGHT_CONST/smaller_height*DISTANCE_CONST) * 12
        b = (PIXEL_HEIGHT_CONST/bigger_height*DISTANCE_CONST) * 12
        c = TAPE_WIDTH
        cos_theta = (b**2 + c**2 - a**2)/(2*b*c)
        self._u = 0
        
        # Find U
        try:
            self._u = math.acos(cos_theta)
        except ValueError:
            self._u = -1

        print('Dist A: %.2f Dist B: %.2f Cos Theta: %.2f Theta: %.2f' \
               % (a, b, cos_theta, self._u))

        # TODO: Find X
        self._x = 0

    @property
    def inner_left_x(self):
        return self._inner_left_x

    @property
    def inner_right_x(self):
        return self._inner_right_x

    @property
    def u(self):
        return self._u
        
    @property
    def x(self):
        return self._x
    
    @property
    def x_avg(self):
        return self._x_avg

    @property
    def box_height(self):
        return self._bigger_box_height

    @property
    def inner_distance(self):
        return self._inner_right_x - self._inner_left_x
