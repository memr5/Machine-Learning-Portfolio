import numpy as np
import imutils
import cv2
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
servoPin = 14
GPIO_TRIGGER = 15
GPIO_ECHO = 18
L_Forward=19
L_Backward=13
R_Forward=5
R_Backward=6

sleeptime=1

GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO.setup(servoPin, GPIO.OUT)
GPIO.setup(L_Forward, GPIO.OUT)
GPIO.setup(L_Backward, GPIO.OUT)
GPIO.setup(R_Forward, GPIO.OUT)
GPIO.setup(R_Backward, GPIO.OUT)

pwm=GPIO.PWM(servoPin,100)
pwm.start(50)

angle1=30
angle2=100
increment = 10


def distance():
    GPIO.output(GPIO_TRIGGER, True)
 
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
        
    TimeElapsed = StopTime - StartTime
    distance = (TimeElapsed * 34300) / 2
 
    return distance


lower_blue = np.array([163,101,86])
high_blue = np.array([179,255,255])

def find_marker(frame):
    # convert the image to grayscale, blur it, and detect edges
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    frame = cv2.GaussianBlur(frame, (5, 5), 0)
    #edged = cv2.Canny(gray, 35, 125)

    mask = cv2.inRange(frame,lower_blue,high_blue)
    kernel = np.ones((5,5),np.float)/25
    mask = cv2.filter2D(mask,-1,kernel)

    kernel = np.ones((3,3),np.uint8)
    opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)

    cnts = cv2.findContours(closing.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    if len(cnts) == 0:
        return -1

    c = max(cnts, key = cv2.contourArea)

    return cv2.minAreaRect(c)


def distance_to_camera(knownWidth, focalLength, perWidth):
	# compute and return the distance from the maker to the camera
	return (knownWidth * focalLength) / perWidth
	# initialize the known distance from the camera to the object, which
	# in this case is 24 inches

angle = 0
duty= float(angle)/10 + 2.5
pwm.ChangeDutyCycle(duty)
time.sleep(3)
angle = 180
duty= float(angle)/10 + 2.5
pwm.ChangeDutyCycle(duty)
time.sleep(3)
angle = 90
duty= float(angle)/10 + 2.5
pwm.ChangeDutyCycle(duty)
time.sleep(3)

device = cv2.VideoCapture(0)

device.set(CV_CAP_PROP_FPS,5)

knownDistance = 17
knownWidth = 3
lastDistance = -1

marker = -1
while marker==-1:
    _, frame = device.read()
    marker = find_marker(frame)

focalLength = (marker[1][0] * knownDistance) / knownWidth

while(True):
    
    ret, frame = device.read()
    #frame = cv2.flip(frame,1)
    final = frame
    
    marker = find_marker(frame)
    if marker==-1:
        continue
    print("width = ",marker[1][0])
    #focalLength = (marker[1][0] * KNOWN_DISTANCE) / KNOWN_WIDTH

    fh,fw,_ = frame.shape
    cv2.rectangle(frame,(int(fw/5),0),(int(4*fw/5),fh),(0,0,255),3)
    cv2.rectangle(frame,(int(fw/3),0),(int(2*fw/3),fh),(0,255,255),3)

    if marker[1][0]*marker[1][1] > 7000:
        #print(maxarea)
        #x,y,w,h = cv2.boundingRect(contours[maxi])
        #final = cv2.rectangle(final,(x,y),(x+w,y+h),(0,255,0),2)

        #M = cv2.moments(contours[maxi])
        #cx = int(M['m10']/M['m00'])
        #cy = int(M['m01']/M['m00'])
        #print(str(cx)+","+str(cy))

        currentDistance = distance_to_camera(knownWidth, focalLength, marker[1][0])

        box = cv2.cv.BoxPoints(marker) if imutils.is_cv2() else cv2.boxPoints(marker)
        box = np.int0(box)
	    
        cv2.drawContours(frame, [box], -1, (0, 255, 0), 2)
	    
        cv2.putText(frame, "%.2fft" % (currentDistance / 12),
		(frame.shape[1] - 200, frame.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX,
		2.0, (0, 255, 0), 3)

        cv2.circle(final,(int(marker[0][0]),int(marker[0][1])),5,(0,255,0),-1)

        if lastDistance == -1:
            lastDistance = currentDistance

        distanceChange = currentDistance - lastDistance

        lastDistance = currentDistance
        print(distanceChange)

        if cx>fw/5 and cx<fw/3 and angle+1<150:
            duty= float(angle+1)/10 + 2.5
            angle += 1
            pwm.ChangeDutyCycle(int(duty))
            #time.sleep(0.02)
        elif cx>2*fw/3 and cx<4*fw/5 and angle-1>30:
            duty= float(angle-1)/10 + 2.5
            angle -= 1
            pwm.ChangeDutyCycle(int(duty))
            #time.sleep(0.02)
        elif angle+1>=150:
            angle = 90
            duty= float(angle+1)/10 + 2.5
            pwm.ChangeDutyCycle(int(duty))
            time.sleep(0.01)
            GPIO.output(L_Backward,True)
            GPIO.output(L_Forward,False)
            time.sleep(0.07)
            GPIO.output(L_Backward,False)

        elif angle-1<30:
            angle = 90
            duty= float(angle+1)/10 + 2.5
            pwm.ChangeDutyCycle(int(duty))
            time.sleep(0.01)
            GPIO.output(R_Backward,True)
            GPIO.output(R_Forward,False)
            time.sleep(0.07)
            GPIO.output(R_Backward,False)

        if cx>=3*fw/4 and cx<fw:
            GPIO.output(R_Backward,True)
            GPIO.output(R_Forward,False)
            time.sleep(0.05)
            GPIO.output(R_Backward,False)
            #time.sleep(0.05)
        elif cx>0 and cx<=fw/4:
            GPIO.output(L_Backward,True)
            GPIO.output(L_Forward,False)
            time.sleep(0.05)
            GPIO.output(L_Backward,False)
            #time.sleep(0.05)
        
        if distanceChange > 0 and currentDistance >50:
            if distanceChange < 2:
                GPIO.output(L_Forward,False)
                GPIO.output(R_Forward,False)
                time.sleep(0.01)
                GPIO.output(L_Forward,True)
                GPIO.output(R_Forward,True)
                time.sleep(0.3)
                GPIO.output(L_Forward,False)
                GPIO.output(R_Forward,False)
                
            elif distanceChange>2:
                GPIO.output(L_Forward,False)
                GPIO.output(R_Forward,False)
                time.sleep(0.01)
                GPIO.output(L_Forward,True)
                GPIO.output(R_Forward,True)
                time.sleep(0.5)
                GPIO.output(L_Forward,False)
                GPIO.output(R_Forward,False)

            if distanceChange < 0 and currentDistance<35:
                if distanceChange > -2:
                    GPIO.output(L_Backward,False)
                    GPIO.output(R_Backward,False)
                    time.sleep(0.01)
                    GPIO.output(L_Backward,True)
                    GPIO.output(R_Backward,True)
                    time.sleep(0.3)
                    GPIO.output(L_Backward,False)
                    GPIO.output(R_Backward,False)
                    
                elif distanceChange<-2:
                    GPIO.output(L_Backward,False)
                    GPIO.output(R_Backward,False)
                    time.sleep(0.01)
                    GPIO.output(L_Backward,True)
                    GPIO.output(R_Backward,True)
                    time.sleep(0.5)
                    GPIO.output(L_Backward,False)
                    GPIO.output(R_Backward,False)
                    
    """if len(contours)!=0:
        x,y,w,h = cv2.boundingRect(contours[0])
        final = cv2.rectangle(final,(x,y),(x+w,y+h),(0,255,0),2)
    """
    

    #result = cv2.blur(result,1)
    cv2.imshow('final',frame)
    #cv2.imshow('Real',frame)
    #cv2.imshow('mask',mask)
    #cv2.imshow('Opening',opening)
    #cv2.imshow('closing',closing)
    #cv2.imshow('Result',result)
    #cv2.imshow('blurResult',blurResult)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

device.release()
cv2.destroyAllWindows()