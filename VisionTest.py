'''
Created on Jan 15, 2017

@author: Nate Mansfield
'''

import cv2
import numpy
def pa(x):
    pass
grabber = cv2.VideoCapture(0)

cv2.namedWindow("controls")
cv2.createTrackbar("H Low", 'controls', 0, 255, pa)
cv2.createTrackbar('S Low', 'controls', 0, 255, pa)
cv2.createTrackbar('V Low', 'controls', 0, 255, pa)
cv2.createTrackbar('H High', 'controls', 0, 255, pa)
cv2.createTrackbar('S High', "controls", 0, 255, pa)
cv2.createTrackbar('V High', 'controls', 0, 255, pa)
cv2.setTrackbarPos('H High', 'controls', 255)
cv2.setTrackbarPos('S High', 'controls', 255)
cv2.setTrackbarPos('V High', 'controls', 255)
while True:
    retrieve, frame = grabber.read()
    frame = cv2.GaussianBlur(frame, (5, 5), 0)    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    h_low = cv2.getTrackbarPos('H Low', 'controls')
    s_low = cv2.getTrackbarPos('S Low', 'controls')
    v_low = cv2.getTrackbarPos('V Low', 'controls')
    h_high = cv2.getTrackbarPos('H High', 'controls')
    s_high = cv2.getTrackbarPos('S High', 'controls')
    v_high = cv2.getTrackbarPos('V High', 'controls')
     
    low = numpy.array([h_low, s_low, v_low])
    high = numpy.array([h_high, s_high, v_high])
    mask = cv2.inRange(hsv, low, high)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, numpy.ones((5, 5), numpy.uint8))
    
    im2, cnts, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(frame, cnts, -1, (0, 255, 0), 3)
    
    largest = None
    convex_hulls = [cv2.convexHull(cnt) for cnt in cnts]
    sorted_hulls = sorted(convex_hulls, cmp=lambda x, y : int(cv2.contourArea(y) - cv2.contourArea(x)))
    biggest_two = []
    if len(sorted_hulls) > 1:
        biggest_two = sorted_hulls[:2]
    elif len(sorted_hulls) == 1:
        biggest_two = sorted_hulls[:1]

    for i in xrange(len(biggest_two)):
        rect = cv2.minAreaRect(biggest_two[i])
        box = cv2.boxPoints(rect)
        box = numpy.int0(box)
        print('box %d is %s' %(i, str(box)))
        cv2.drawContours(frame, [box], -1, (255, 0, 0), 3)
            
    overlay = cv2.bitwise_and(frame, frame, mask=mask)
    cv2.imshow("original Pic", frame)
    cv2.imshow("hello peoples!", mask)
    cv2.imshow("the overlay", overlay)
    if cv2.waitKey(1) & 0xff == ord("q"):
        break
    
grabber.release()
cv2.destroyAllWindows()
    
