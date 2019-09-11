import cv2
import numpy as np
from imutils.object_detection import non_max_suppression

#device = cv2.VideoCapture(0)
device = cv2.VideoCapture('HumanVideo.mp4')
_, frame1 = device.read()
_, frame2 = device.read()
frame1 = cv2.flip(frame1,1)

height = int(frame1.shape[0]*40/100)
width = int(frame1.shape[1]*50/100)
frame1 = cv2.resize(frame1,(width,height),interpolation=cv2.INTER_AREA)

while True:
    
    frame2 = cv2.flip(frame2,1)
    height = int(frame2.shape[0]*40/100)
    width = int(frame2.shape[1]*50/100)
    frame2 = cv2.resize(frame2,(width,height),interpolation=cv2.INTER_AREA)

    diff = cv2.absdiff(frame1,frame2)
    gray = cv2.cvtColor(diff,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(5,5),0)
    _, thresh = cv2.threshold(blur,20,255,cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh,(5,5),iterations=3)

    kernel = np.ones((3,3),np.uint8)
    #opening = cv2.morphologyEx(dilated, cv2.MORPH_OPEN, kernel)
    #closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)

    contours,hierarchy = cv2.findContours(dilated,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    """ new_contours = []
    for contour in contours:
        x,y,w,h = cv2.boundingRect(contour)
        new_contours.append([x,y,x+w,y+h])
    
    #contours = np.array([[x, y, x + w, y + h] for x,y,w,h in cv2.boundingRect(contours)])
	
    if len(new_contours)!=0:
        new_contours = non_max_suppression(new_contours,probs=None,overlapThresh=0.65)
 """

    if hierarchy is not None:
        hierarchy = hierarchy[0]

        for contour,hi in zip(contours,hierarchy):
            #if cv2.contourArea(contour) > 3000:
            #x,y,w,h = cv2.boundingRect(contour)
            #print(hi)
            if hi[3]==-1 and cv2.contourArea(contour) > 1000:
                x,y,w,h = cv2.boundingRect(contour)
                cv2.rectangle(frame1,(x,y),(x+w,y+h),(0,255,0),3)

    cv2.imshow('frame',frame1)
    #cv2.imshow('closing',closing)
    cv2.imshow('dilated',dilated)
    
    frame1 = frame2
    _, frame2 = device.read()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

device.release()
cv2.destroyAllWindows()