import cv2
import numpy as np

img = cv2.imread('DSCN1759.JPG',-1)
height = int(img.shape[0]*15/100)
width = int(img.shape[1]*10/100)
img = cv2.resize(img,(height,width),interpolation=cv2.INTER_AREA)

newImg = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

lower_blue = np.array([51,50,50])
high_blue = np.array([112,255,255])

mask = cv2.inRange(newImg,lower_blue,high_blue)
result = cv2.bitwise_and(img,img,mask=mask)

cv2.imshow('img',img)
cv2.imshow('result',result)
cv2.waitKey(0)
cv2.destroyAllWindows()