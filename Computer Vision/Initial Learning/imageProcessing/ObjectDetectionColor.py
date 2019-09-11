import cv2
import numpy as np


device = cv2.VideoCapture(0)

knownDistance = 17
knownWidth = -1
lastDistance = -1

while(True):
    
    ret, frame = device.read()
    #frame = cv2.flip(frame,1)

    newFrame = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    lower_blue = np.array([163,101,86])
    high_blue = np.array([179,255,255])

    mask = cv2.inRange(newFrame,lower_blue,high_blue)
    kernel = np.ones((5,5),np.float)/25
    mask = cv2.filter2D(mask,-1,kernel)

    kernel = np.ones((3,3),np.uint8)
    opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
    result = cv2.bitwise_and(frame,frame,mask=closing)

    contours, hierarchy = cv2.findContours(closing,1,2)
    final = frame
    i = 0
    maxi = 0
    maxarea = -1
    for l in contours:
        #print(l)
        area = cv2.contourArea(l)
        if maxarea==-1:
            maxarea = area
        elif maxarea < area:
            maxarea = area
            maxi = i
        i += 1
    if maxarea!=-1 and maxarea > 7000:
        #print(maxarea)
        x,y,w,h = cv2.boundingRect(contours[maxi])
        final = cv2.rectangle(final,(x,y),(x+w,y+h),(0,255,0),2)
        M = cv2.moments(contours[maxi])
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        #print(str(cx)+","+str(cy))
        cv2.circle(final,(cx,cy),5,(0,255,0),-1)

        if knownWidth == -1:
            knownWidth = w
            flag = 1
        
        focalLength = (x * knownDistance) / knownWidth

        currentDistance = (knownWidth*focalLength) / x

        if lastDistance == -1:
            lastDistance = currentDistance

        distanceChange = currentDistance - lastDistance
        lastDistance = currentDistance
        print(distanceChange)

    """if len(contours)!=0:
        x,y,w,h = cv2.boundingRect(contours[0])
        final = cv2.rectangle(final,(x,y),(x+w,y+h),(0,255,0),2)
    """
    

    #result = cv2.blur(result,1)
    cv2.imshow('final',final)
    #cv2.imshow('Real',frame)
    #cv2.imshow('mask',mask)
    #cv2.imshow('Opening',opening)
    cv2.imshow('closing',closing)
    #cv2.imshow('Result',result)
    #cv2.imshow('blurResult',blurResult)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

device.release()
cv2.destroyAllWindows()