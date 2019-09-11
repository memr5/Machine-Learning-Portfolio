import cv2
import numpy as np
from imutils.object_detection import non_max_suppression
import imutils

device = cv2.VideoCapture('http://192.168.1.136:4812/video')
#device = cv2.VideoCapture('HumanVideo.mp4')
#device = cv2.VideoCapture(0)

""" human_cascade = cv2.CascadeClassifier('haarcascade_fullbody.xml')
human_cascade.load('haarcascade_fullbody.xml') """

human_hog = cv2.HOGDescriptor()
human_hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

while True:

    ret,frame = device.read()
    frame = cv2.flip(frame,1)
    """ height = int(frame.shape[0]*40/100)
    width = int(frame.shape[1]*50/100)
    frame = cv2.resize(frame,(width,height),interpolation=cv2.INTER_AREA)
 """
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #frame_gray = cv2.GaussianBlur(frame_gray,(5,5),0)

    #humans = human_cascade.detectMultiScale(frame_gray,1.1,3)
    (rects, weights) = human_hog.detectMultiScale(frame_gray, winStride=(4, 4),padding=(8, 8), scale=1.05)

    rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
    pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)

    maxarea = -1
    maxi = 0
    i = 0
    for (x1,y1,x2,y2) in pick:
        w, h = x2-x1,y2-y1
        if maxarea == -1:
            maxarea = w*h
        elif maxarea < w*h:
            maxarea = w*h
            maxi = i
        i += 1


    if len(pick)!=0:
        (x1,y1,x2,y2) = pick[maxi]
        cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)

    cv2.imshow("frame", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

device.release()
cv2.destroyAllWindows()