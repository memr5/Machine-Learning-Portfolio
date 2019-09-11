import cv2
import numpy as np

rect = True
drawing = False
ix,iy = -1,-1

def draw(event,x,y,flags,params):
    global rect,drawing,ix,iy,img

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix,iy = x,y
    
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            #img = np.zeros((512,512,3),np.uint8)
            color = (np.random.randint(0,256),np.random.randint(0,256),np.random.randint(0,256))
            if rect == True:
                cv2.rectangle(img,(ix,iy),(x,y),color,-1,cv2.LINE_AA)
            else:
                radius = int(np.sqrt(np.square(ix-x) + np.square(iy-y)))
                cv2.circle(img,(ix,iy),radius,color,-1,cv2.LINE_AA)

    elif event == cv2.EVENT_LBUTTONUP:
        #img = np.zeros((512,512,3),np.uint8)
        drawing = False
        color = (np.random.randint(0,256),np.random.randint(0,256),np.random.randint(0,256))
        if rect == True:
            cv2.rectangle(img,(ix,iy),(x,y),color,-1,cv2.LINE_AA)
        else:
            radius = int(np.sqrt(np.square(ix-x) + np.square(iy-y)))
            cv2.circle(img,(ix,iy),radius,color,-1,cv2.LINE_AA)
            

img = np.zeros((512,512,3),np.uint8)
cv2.namedWindow('img')
cv2.setMouseCallback('img',draw)

while(True):
    cv2.imshow("img",img)
    k = cv2.waitKey(1) & 0xFF 
    if k == ord('q'):
        break
    elif k == ord('m'):
        rect = not rect
    elif k == ord('c'):
        img = np.zeros((512,512,3),np.uint8)

cv2.destroyAllWindows()