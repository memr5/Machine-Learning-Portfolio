import cv2
import numpy as np

device = cv2.VideoCapture('http://192.168.1.136:4812/video')
#device = cv2.VideoCapture(0)
face = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye = cv2.CascadeClassifier('haarcascade_eye.xml')
face.load('haarcascade_frontalface_default.xml')
eye.load('haarcascade_eye.xml')

while True:

    ret,frame = device.read()

    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face.detectMultiScale(frame_gray,1.3,5)

    for (x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),3)
        face_roi_gray = frame_gray[y:y+h,x:x+w]
        face_roi = frame[y:y+h,x:x+w]
        eyes = eye.detectMultiScale(face_roi)
        for (xe,ye,we,he) in eyes:
            cv2.rectangle(face_roi,(xe,ye),(xe+we,ye+he),(0,255,255),2)

    cv2.imshow('frame',frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


device.release()
cv2.destroyAllWindows()