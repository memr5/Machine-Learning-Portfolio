import cv2
import numpy as np


device = cv2.VideoCapture(0)

while(True):

    ret, frame = device.read()
    frame = cv2.flip(frame,1)

    lap = cv2.Laplacian(frame,cv2.CV_64F)
    sobelx = cv2.Sobel(frame,cv2.CV_64F,1,0,ksize=1)
    sobely = cv2.Sobel(frame,cv2.CV_64F,0,1,ksize=-1)
    edges = cv2.Canny(frame,20,50)

    cv2.imshow('frame',frame)
    cv2.imshow('lap',lap)
    cv2.imshow('sobelx',sobelx)
    cv2.imshow('sobely',sobely)
    cv2.imshow('edges',edges)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

device.release()
cv2.destroyAllWindows()