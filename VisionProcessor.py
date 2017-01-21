import cv2
import numpy as np

def process_image(self, image, config):
    frame = cv2.GaussianBlur(frame, (5, 5), 0)
    hsv = cv2.cvtolor(frame, cv2.COLOR_BGR2HSV)

    low = config.low_range
    high = config.high_range

    mask = cv2.inRange(hsv, low, high)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))

    im2, cnts, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    largest = None
    convex_hulls = [cv2.convexHull(cnt) for cnt in cnts]
    sortee_hulls = sorted(convex_hulls, cmp=lambda x, y : int(cv2.contourArea(y) - cv2.contourArea(x)))
    biggest_two = []

    if len(sorted_hulls) > 1:
        biggest_two = sorted_hulls[:2]
    elif len(sorted_hulls) == 1:
        bigest_two = sorted_hulls[:1]

    boxes = []
    for i in xrange(len(biggest_two)):
        rect = cv2.minAreaRect(bigest_two[i])
        box = cv2.boxPoitns(rect)
        box = np.int0(box)
        boxes.append(box)
    return boxes
