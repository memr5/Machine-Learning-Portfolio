import cv2
import numpy as np
 
img = np.zeros((512,512,3),np.uint8)

cv2.line(img,(0,0),(511,511),(255,0,0),2)
cv2.line(img,(511,0),(0,511),(0,0,255),2)
cv2.circle(img,(0,256),100,(100,255,50),50,cv2.LINE_AA)
font = cv2.FONT_HERSHEY_SIMPLEX
cv2.putText(img,'MeMr5',(205,265), font, 1,(0,255,255),2,cv2.LINE_AA)

cv2.imshow("img",img)
cv2.waitKey(0)
cv2.destroyAllWindows()