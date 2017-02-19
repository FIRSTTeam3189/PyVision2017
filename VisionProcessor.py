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

    # Draw info of boxes
    if len(boxes) == 2:
        box_one_x = boxes[0][0][0] + boxes[0][1][0] + boxes[0][2][0] + boxes[0][3][0]
        box_two_x = boxes[1][0][0] + boxes[1][1][0] + boxes[1][2][0] + boxes[1][3][0]
        if box_one_x > box_two_x:
            right_box = boxes[0]
            left_box  = boxes[1]
        else:
            right_box = boxes[1]
            left_box = boxes[0]

        # Find out inner distance
        inner_left = sorted(left_box, cmp=lambda x, y: y[0] - x[0])[0:2]
        inner_right = sorted(right_box, cmp=lambda x, y: x[0] - y[0])[0:2]
        
        # Average x's
        inner_left_x = (inner_left[0][0] + inner_left[1][0]) / 2
        inner_right_x = (inner_right[0][0] + inner_right[1][0]) / 2
        
        cv2.line(frame, (inner_left_x, 0), (inner_left_x, height), (255, 0, 0), 3)
        cv2.line(frame, (inner_right_x, 0), (inner_right_x, height), (0, 0, 255), 3)

        # Box Inner Height (bih)
        bih_one = abs(inner_left[0][1] - inner_left[1][1])
        bih_two = abs(inner_right[0][1] - inner_right[1][1])
        if  bih_one > bih_two:
            bigger_box = inner_left
        else:
            bigger_box = inner_right

        box_height = abs(bigger_box[0][1] - bigger_box[1][1])
        cv2.line(frame, (bigger_box[0][0], bigger_box[0][1]), (bigger_box[1][0], bigger_box[1][1]), (64, 255, 64), 3)

        print("Inner Distance: %d Bigger Height: %d" % (inner_right_x - inner_left_x, box_height))
        """
        SEND TO SMART DASHBOARD
        s = bigHeight/115;
        u = arcsin((s * InnerDistance)/144);
        x = 264 * cos(u);
        """
    return frame    
