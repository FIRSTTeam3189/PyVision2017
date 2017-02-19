import cv2
import numpy as np

def process_image(frame, config):
    frame = cv2.GaussianBlur(frame, (5, 5), 0)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    low = config.low_range
    high = config.high_range

    mask = cv2.inRange(hsv, low, high)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))

    im2, cnts, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    largest = None
    convex_hulls = [cv2.convexHull(cnt) for cnt in cnts]
    sorted_hulls = sorted(convex_hulls, cmp=lambda x, y : int(cv2.contourArea(y) - cv2.contourArea(x)))
    biggest_two = []

    if len(sorted_hulls) > 1:
        biggest_two = sorted_hulls[:2]
    elif len(sorted_hulls) == 1:
        biggest_two = sorted_hulls[:1]

    boxes = []
    for i in xrange(len(biggest_two)):
        rect = cv2.minAreaRect(biggest_two[i])
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        boxes.append(box)

    if config.show_image:
        cv2.imshow('Processed', mask)
        
    return boxes

def draw_center_line(frame, boxes):
    height, width, _ = frame.shape

    # Draw frame center first
    x_center_bottom = (width/2, 0)
    x_center_top = (width/2, height)
    cv2.line(frame, x_center_bottom, x_center_top, (255, 0, 255), 3)

    if len(boxes) > 0:
        x_sum = reduce(lambda tot, box: tot + box[0][0] + box[1][0] + box[2][0] + box[3][0], boxes, 0)
        
        avg = int(x_sum/(len(boxes)*4))
        avg_bottom = (avg, 0)
        avg_top = (avg, height)
        cv2.line(frame, avg_bottom, avg_top, (0, 255, 0), 3)

    return frame    
