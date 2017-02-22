#encoding=utf-8
import cv2
import numpy as np
import numpy.linalg as la
import math

PIXEL_HEIGHT_CONST = 150.0 # In Pixels
DISTANCE_CONST = 24 # In Inches
TAPE_WIDTH = 2.0 # In Inches
CAM_FOVY = 34.3 # In Degrees
CAM_FOVX = 61.0 # In Degrees
CAM_RES_X = 640.0
L_PT = 3.125 # In Inches
L_P = 11.0 # In Inches
PHI = math.atan(L_P/L_PT) # In Radians
H = math.sqrt(L_P**2 + L_PT**2)

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
        left_points = sorted(left_box, cmp=lambda x,y: y[0]-x[0])
        right_points = sorted(right_box, cmp=lambda x,y : x[0]-y[0])

        self._inner_left_x = (left_points[0][0] + left_points[1][0])/2
        self._inner_right_x = (right_points[0][0] + right_points[1][0])/2

        if  self._x_avg < (CAM_RES_X/2.0):
            bigger_box = left_points
            bigger_inner_x = self._inner_left_x
            lambda_mult = 1
        else:
            bigger_box = right_points
            bigger_inner_x = self._inner_right_x
            lambda_mult = 1

        self._bigger_box_height = abs(bigger_box[0][1] - bigger_box[1][1])

        # Grab bigger box inner and outer height
        inner_bb_height = float(self._bigger_box_height)
        outer_bb_height = float(abs(bigger_box[2][1] - bigger_box[3][1]))

        # Find distances, in inches
        a = PIXEL_HEIGHT_CONST/inner_bb_height*DISTANCE_CONST
        b = PIXEL_HEIGHT_CONST/outer_bb_height*DISTANCE_CONST
        c = TAPE_WIDTH
        cos_theta = (b**2 + c**2 - a**2)/(2*b*c)
        theta = 0
        
        # Find U
        try:
            theta = math.acos(cos_theta)
        except ValueError:
            self._u = 0

        omega = math.pi - PHI - theta
        d2 = math.sqrt(H**2 + a**2 - 2*H*a*math.cos(omega))
        lambda_angle = lambda_mult*math.asin(math.sin(omega)*H/d2)
        tau = math.radians(CAM_FOVX/CAM_RES_X*(self._x_avg - (CAM_RES_X/2.0)))

        self._u =  lambda_angle + tau

        print("d1: %.2f d2: %.2f d3: %.2f θ: %.2f Ω: %.2f λ: %.2f τ: %.2f u: %.2f" \
              % (a, d2, b, math.degrees(theta), math.degrees(omega), math.degrees(lambda_angle), math.degrees(tau), math.degrees(self._u)))

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
