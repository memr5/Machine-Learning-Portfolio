import cv2 

img = cv2.imread('pro-pic.jpg',-1)

cv2.namedWindow('MeMr5',cv2.WINDOW_NORMAL)
cv2.imshow('MeMr5',img)
cv2.waitKey(0)
cv2.destroyAllWindows()