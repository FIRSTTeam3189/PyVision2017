import cv2
import math
import numpy as np
from BoxInfo import BoxInfo

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
        arc_length = cv2.arcLength(biggest_two[i], True)
        approx = cv2.approxPolyDP(biggest_two[i], arc_length*.08, True)
        if len(approx) == 4:
            box = [x[0] for x in approx]
            boxes.append(box)
        #rect = cv2.minAreaRect(biggest_two[i])
        #box = cv2.boxPoints(rect)
        #box = np.int0(box)
        #boxes.append(box)

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

        s = box_height /115
        u = math.asin((s * (inner_right_x - inner_left_x)) / (s*144)) 
        x = (s*264) * math.cos(u)

        cv2.line(frame, (int(x), 0), (int(x), height), (255,255,255), 3)
        
        print("Inner Distance: %d Bigger Height: %d" % (inner_right_x - inner_left_x, box_height))
        """
        SEND TO SMART DASHBOARD
        s = bigHeight/115;
        u = arcsin((s * InnerDistance)/144);
        x = 264 * cos(u);
        """
    return frame

def draw_box_info(frame, boxes):
    # Draw centerline of image first
    height, width = frame.shape[0:2]
    frame_middle_top = (width/2, 0)
    frame_middle_bottom = (width/2, height)

    cv2.line(frame, frame_middle_top, frame_middle_bottom, (255, 255, 255), 2)
    
    if len(boxes) > 0:
        # Draw average x line of boxes
        x_avg = 0
        for box in boxes:
            x_avg += reduce(lambda acc, x: acc + x[0], box, 0)

        x_avg = x_avg / len(boxes) * 4
        avg_top = (x_avg, 0)
        avg_bottom = (x_avg, height)

        cv2.line(frame, avg_top, avg_bottom, (0, 128, 255), 3)

        # Draw boxes
        contour_boxes = []
        for box in boxes:
            contour_boxes.append(np.array([[x] for x in box]))
        cv2.drawContours(frame, contour_boxes, -1, (0, 255, 255), 1)
    if len(boxes) == 2:
        info = BoxInfo(boxes)

        # Draw inner lines now
        inner_left_p1 = (info.inner_left_x, 0)
        inner_left_p2 = (info.inner_left_x, height)
        inner_right_p1 = (info.inner_right_x, 0)
        inner_right_p2 = (info.inner_right_x, height)
        cv2.line(frame, inner_left_p1, inner_left_p2, (255, 0, 0), 3)
        cv2.line(frame, inner_right_p1, inner_right_p2, (255, 0, 0), 3)

        # Draw calculated peg line
        peg_line_p1 = (int(info.x), 0)
        peg_line_p2 = (int(info.x), height)
        cv2.line(frame, peg_line_p1, peg_line_p2, (0, 255, 0), 3)

        # Draw info about box on screen
        font = cv2.FONT_HERSHEY_PLAIN
        cv2.putText(frame, 'U: %.4f' % math.degrees(info.u), (10, 20), font, 1.5, (255, 0, 255), 3, cv2.LINE_AA)
        cv2.putText(frame, 'Box Height: %d' % info.box_height, (10, 50), font, 1.5, (255, 0, 255), 3, cv2.LINE_AA)
        cv2.putText(frame, 'Inner Distance: %d' % info.inner_distance, (10, 90), font, 1.5, (255, 0, 255), 3, cv2.LINE_AA)

    return frame
