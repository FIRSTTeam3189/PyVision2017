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
    
    im2, cnts, hiersrchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(frame, cnts, -1, (0, 255, 0), 3)
    
    largest = None
    for cnt in cnts:
        hull = cv2.convexHull(cnt)
        if largest is None or cv2.contourArea(largest) < cv2.contourArea(hull):
            second_largest = largest;
            largest = hull
            
    if largest is not None:
        rect = cv2.minAreaRect(largest)
        second_rect = rect
        if second_largest is not None:
            second_rect = cv2.minAreaRect(second_largest)
        box=cv2.boxPoints(rect)
        second_box = cv2.boxPoints(second_rect)
        box = numpy.int0(box)
        second_box = numpy.int0(second_box)
        cv2.drawContours(frame,[box],-1,(255,0,0),3)
        cv2.drawContours(frame,[second_box],-1,(255,0,0),3)
        cv2.drawContours(frame,[largest],-1,(0,255,0),3)
        cv2.drawContours(frame,[second_largest],-1,(0,255,0),3)
            
    overlay = cv2.bitwise_and(frame, frame, mask=mask)
    cv2.imshow("original Pic", frame)
    cv2.imshow("hello peoples!", mask)
    cv2.imshow("the overlay", overlay)
    if cv2.waitKey(1) & 0xff == ord("q"):
        break
    
grabber.release()
cv2.destroyAllWindows()
    
