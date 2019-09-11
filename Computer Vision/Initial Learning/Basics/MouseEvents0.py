import cv2
import numpy as np


def drawCircle(event,x,y,flags,params):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        color = (np.random.randint(0,256),np.random.randint(0,256),np.random.randint(0,256))
        cv2.circle(img,(x,y),20,color,2,cv2.LINE_AA)


img = np.zeros((512,512,3),np.uint8)
cv2.namedWindow('img')
cv2.setMouseCallback('img',drawCircle)

while(True):
    cv2.imshow("img",img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()