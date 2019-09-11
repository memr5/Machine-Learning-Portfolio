import cv2
import numpy as np

"""
for i in dir(cv2):
    if i.startswith('COLOR_'):
        print(i)
"""

def nothing(pos):
    pass


img = cv2.imread('DSCN1759.JPG',-1)
height = int(img.shape[0]*15/100)
width = int(img.shape[1]*10/100)
img = cv2.resize(img,(height,width),interpolation=cv2.INTER_AREA)

newImg = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

cv2.namedWindow('mask')

cv2.createTrackbar('lh','mask',0,179,nothing)
cv2.createTrackbar('ls','mask',0,255,nothing)
cv2.createTrackbar('lv','mask',0,255,nothing)

cv2.createTrackbar('hh','mask',0,179,nothing)
cv2.createTrackbar('hs','mask',0,255,nothing)
cv2.createTrackbar('hv','mask',0,255,nothing)

while(True):

    lh = cv2.getTrackbarPos('lh','mask')
    ls = cv2.getTrackbarPos('ls','mask')
    lv = cv2.getTrackbarPos('lv','mask')

    hh = cv2.getTrackbarPos('hh','mask')
    hs = cv2.getTrackbarPos('hs','mask')
    hv = cv2.getTrackbarPos('hv','mask')

    lower_blue = np.array([lh,ls,lv])
    high_blue = np.array([hh,hs,hv])

    mask = cv2.inRange(newImg,lower_blue,high_blue)

    cv2.imshow('mask',mask)
    k = cv2.waitKey(1) & 0xFF

    if k==ord('q'):
        break

cv2.destroyAllWindows()