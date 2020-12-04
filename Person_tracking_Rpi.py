import cv2
import numpy as np

import RPi.GPIO as GPIO
from time import sleep


# font 
font = cv2.FONT_HERSHEY_SIMPLEX 
  
# org 
org = (5, 15) 
org2 = (5, 30)

# fontScale 
fontScale = 0.4
   
# Blue color in BGR 
color = (0, 0, 255) 
# Line thickness of 2 px 
thickness = 1



M11=16
M12=18
M21=33
M22=35

def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(M11,GPIO.OUT)
    GPIO.setup(M12,GPIO.OUT)
    GPIO.setup(M21,GPIO.OUT)
    GPIO.setup(M22,GPIO.OUT)
    
def forward():
    GPIO.output(M12,GPIO.HIGH)
    GPIO.output(M11,GPIO.LOW)
    GPIO.output(M22,GPIO.HIGH)
    GPIO.output(M21,GPIO.LOW)

def reverse():
    GPIO.output(M11,GPIO.HIGH)
    GPIO.output(M12,GPIO.LOW)
    GPIO.output(M21,GPIO.HIGH)
    GPIO.output(M22,GPIO.LOW)

def clockwise():
    GPIO.output(M22,GPIO.HIGH)
    GPIO.output(M21,GPIO.LOW)
    GPIO.output(M12,GPIO.LOW)
    GPIO.output(M11,GPIO.LOW)
    
def anticlockwise():
    GPIO.output(M12,GPIO.HIGH)
    GPIO.output(M11,GPIO.LOW)
    GPIO.output(M22,GPIO.LOW)
    GPIO.output(M21,GPIO.LOW)
    
    
    
def stop():
    GPIO.output(M11,GPIO.LOW)
    GPIO.output(M12,GPIO.LOW)
    GPIO.output(M21,GPIO.LOW)
    GPIO.output(M22,GPIO.LOW)
    
    
    
    
    

cap = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc(*'XVID') 
out = cv2.VideoWriter('output.avi', fourcc, 10.0, (320, 240))
cap.set(cv2.CAP_PROP_FPS,10)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,240)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,320)
setup()
while True:
    fps = cap.get(cv2.CAP_PROP_FPS)
    ret, frame = cap.read()   
    frame=cv2.flip(frame,1)
    image = cv2.putText(frame, 'FPS: '+str(fps), org, font,
                    fontScale, color, thickness, cv2.LINE_AA)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    j=True
    
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1)
        image = cv2.putText(frame,'X  Y  H  W : '+str(x)+' '+str(y)+' '+str(h)+' '+str(w)+'   '+str(frame.shape), org2, font,
                    fontScale, color, thickness, cv2.LINE_AA)
        P=x+(w/2)
        j=False

        if(P<120):
            anticlockwise()
        elif(P>200):
            clockwise()
        else:
            if(w<70):
                forward()   
            elif(w>80):
                reverse()
            else:
                stop()
                
    if(j):
        stop()
    cv2.imshow('frame', frame)
    # frame is converted to hsv 
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) 
      
    # output the frame 
    out.write(hsv)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
GPIO.cleanup()
cap.release()
cv2.destroyAllWindows()