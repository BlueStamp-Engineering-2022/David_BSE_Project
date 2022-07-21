from picamera2 import Picamera2
from picamera.array import PiRGBArray
import RPi.GPIO as GPIO
import cv2
import numpy as np
import cv2 as cv
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

#Setting the pins of the ultrasonic sensor.
frontTrigger = 11
frontEcho = 13

#setting the motor pins that control the direction at which the motor turns.
motorPin1 = 21
motorPin2 = 26
motor2Pin1 = 24
motor2Pin2 = 22

#Setting the speed pins that are connected to a PWM pin on the Raspberry pi.
speedPin1 = 35
speedPin2 = 33

#Sets up the ultrasonic sensor
GPIO.setup(frontTrigger, GPIO.OUT)
GPIO.setup(frontEcho, GPIO.IN)

#First turns off the trigger of the ultrasonic sensor
GPIO.output(frontTrigger, False)


#This is the proportional controller for the speed of the motor when the ball is either on the right or the left side of the vehcile/robot.
#error: This is the distance (pixels) from the center of the ball to the enter of the screen/camera/robot.
#s: This is the current speed of the motor that will either be slowed dowm or sped up depending on which motor is calling this method.
#konstant: This is just a konstant to multiply the error by. (Can change to better tune the speed outcome)
#right: This will be true if the ball is to the right of the robot.
#left: This will be true if the ball is to the left of the robot.
def lrspeed (s, error, konstant, right, left):
    newSpeed = 100
    if right is True and left is False:
        newSpeed = s + (konstant * error * -1) * 0.6        #0.6 is to make the newspeed a little bit slower because without this the motor will move too fast and overshoot the ball
    elif right is False and left is True:
        newSpeed = s + (konstant * error) * 0.6
    newSpeed = newSpeed - 8;
    if newSpeed > 100:
        newSpeed = 100
    elif newSpeed < 0:
        newSpeed = 0
    return newSpeed

#This is the proportional controller for the speed of the motor when the ball is infront of the vehcile/robot.
#s: This is the current speed of the motor that will either be slowed dowm or sped up depending on which motor is calling this method.
#error: This is the difference between the current radius of the ball and the radius at which the vechile should stop so that it will not hit the ball.
#konstant: This is just a konstant to multiply the error by. (Can change to better tune the speed outcome)
def forwardspeed (s, error, konstant):
    newSpeed = konstant * error * 0.6                       #0.6 is to make the newspeed a little bit slower because without this the motor will move too fast and collide with the ball
    if newSpeed > 100:
        newSpeed = 100
    elif newSpeed < 0:
        newSpeed = 0
    return newSpeed
    


#Runs the ultrasonic sensor 
def sonar(TRIGGER, ECHO):
    start = 0
    stop = 0

    GPIO.output(TRIGGER, True)
    time.sleep(1)
    GPIO.output(TRIGGER, False)
    while GPIO.input(ECHO) == 0:
        start = time.time()
        
    while GPIO.input(ECHO)==1:
        stop = time.time()
        
        if (stop - start > 0.005):
            break
        
    elapsed = stop-start

    distance = elapsed * 17150

    distance = round(distance, 2)

    return distance



#Sets up all the motor pins and the speed pin as well.
GPIO.setup(motorPin1, GPIO.OUT)
GPIO.setup(motorPin2, GPIO.OUT)
GPIO.setup(motor2Pin1, GPIO.OUT)
GPIO.setup(motor2Pin2, GPIO.OUT)
GPIO.setup(speedPin1, GPIO.OUT)
GPIO.setup(speedPin2, GPIO.OUT)

#Turns off the motor initially
GPIO.output(motorPin1, GPIO.LOW)
GPIO.output(motorPin2, GPIO.LOW)
GPIO.output(motor2Pin1, GPIO.LOW)
GPIO.output(motor2Pin2, GPIO.LOW)


#Initally set the speed pins to highest/fastest speed (Can be set to low as well)
GPIO.output(speedPin1, GPIO.HIGH)
GPIO.output(speedPin2, GPIO.HIGH)

#This function will make the vehicle move forward.
def forward():
    GPIO.output(motorPin1, GPIO.LOW)
    GPIO.output(motorPin2, GPIO.HIGH)
    GPIO.output(motor2Pin1, GPIO.LOW)
    GPIO.output(motor2Pin2, GPIO.HIGH)
    
#This function will make the vehicle move backward.
def reverse():
    GPIO.output(motorPin1, GPIO.HIGH)
    GPIO.output(motorPin2, GPIO.LOW)
    GPIO.output(motor2Pin1, GPIO.HIGH)
    GPIO.output(motor2Pin2, GPIO.LOW)

#This function will make the vehicle turn right.
def rightTurn():
    GPIO.output(motorPin1, GPIO.LOW)
    GPIO.output(motorPin2, GPIO.HIGH)
    GPIO.output(motor2Pin1, GPIO.HIGH)
    GPIO.output(motor2Pin2, GPIO.LOW)

#This function will make the vehicle turn left.
def leftTurn():
    GPIO.output(motorPin1, GPIO.HIGH)
    GPIO.output(motorPin2, GPIO.LOW)
    GPIO.output(motor2Pin1, GPIO.LOW)
    GPIO.output(motor2Pin2, GPIO.HIGH)

  #This function will make the vehicle stop.
def stop():
    GPIO.output(motorPin1, GPIO.LOW)
    GPIO.output(motorPin2, GPIO.LOW)
    GPIO.output(motor2Pin1, GPIO.LOW)
    GPIO.output(motor2Pin2, GPIO.LOW)

#Sets the frequency of the motor speeds to 200 Hz
p = GPIO.PWM(speedPin1, 200)
p2 = GPIO.PWM(speedPin2, 200)


#cv2.startWindowThread()

#Sets up the camera
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)}))
picam2.start()

#Define the range of shades of red to detect.
lower = np.array([155,120, 80])
upper = np.array([178, 255, 255])

direction = '0'
right = False
left = False
front = False
ball = False
center = 315;
error = 0
error2 = 0
speed = 0
speedr = 0
speedl = 0
p.start(0)
p2.start(0)

while True:
   
    #captures an image to do ball tracking//detection on.
    im = picam2.capture_array()
   
    hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)               #Change out the colors to HSV
    color_mask = cv2.inRange(hsv, lower, upper)             #Remove all colors except for the color range defined (this will be in black and white)
    result = cv2.bitwise_and(im, im, mask= color_mask)      #Get the final result to show just the ball in the frame.
    
    #This function detects whether or not there is a cricle in the frame. THsi will only work for both balc and white so use the color_mask screen.
    circles = cv.HoughCircles(color_mask, cv.HOUGH_GRADIENT, 1.5, 6600, param1=50, param2=30, minRadius=0, maxRadius=0)
    if circles is not None:
        
        circles = np.uint16(np.around(circles))
        for i in circles[0,:]:
            #cv.circle(result, (i[0],i[1]),i[2],(0,255,0),2)
            #cv.circle(result,(i[0],i[1]),2,(0,0,255),3)
            if i[0] > 350:                                  #Bascially i[0] is the x-coordinate of the center of the ball so this is setting a border that will define the left, right, and front of the screen
                
                if(i[0] < 430):
                   front = True
                   right = False
                   left = False
                else:
                    right = True
                    left = False
                    front = False
                ball = True
                error = i[0] - center;
                
            elif i[0] < 250:                                #Bascially i[0] is the x-coordinate of the center of the ball so this is setting a border that will define the left, right, and front of the screen
               
                if(i[0] > 170):
                    front = True
                    right = False
                    left = False
                else:
                    right = False
                    left = True
                    front = False
                ball = True
                error = i[0] - center;
                
            else:                                           #Bascially i[0] is the x-coordinate of the center of the ball so this is setting a border that will define the left, right, and front of the screen
                
                right = False
                left = False
                front = True
                ball = True
                error2 = (i[2] -230) * -1
            

    else:
        #If ball is not detected inside the frame then the vechile will use the ultrasonic sensor to detect whether or not the vehicle is close to a wall and if it is it will reverse so it won't hit the wall.
        ball = False
        front = False
        left = False
        right = False
        
        distF = sonar(frontTrigger,frontEcho)               #gets the distance from the ultrasonic sensor to an object infront of it
       
        
        p.ChangeDutyCycle(40)
        p2.ChangeDutyCycle(40)
        if(distF < 20):
            #reverse if an object that is not a ball is 20 cm from the vehicle/robot.
            reverse()
        else:
            stop()
    if front is False and ball is True:                     #Gets the speed of the motors by calling the proportional controllers when the ball is to the left or right of the robot.
        speedr = lrspeed(0, error, 0.3, True, False)
        speedl = lrspeed(0, error, 0.3, False, True)
        p.ChangeDutyCycle(speedl)
        p2.ChangeDutyCycle(speedr)
    elif front is True and ball is True:                    #Gets the speed of the motors by calling the proportional controllers when the ball is infront of the robot/vehicle.
        speedr = forwardspeed(0, error2, 0.5)
        speedl = forwardspeed(0, error2, 0.5)
        speedr = speedr - 4
        if(speedr < 0):
            speedr = 0
        p.ChangeDutyCycle(speedr)
        p2.ChangeDutyCycle(speedl)
    
    if right is True and ball is True:
        rightTurn()
        
    elif left is True and ball is True:
        leftTurn()

    elif front is True and ball is True:
        forward()
    #cv2.imshow("Result", result)
    im = None

pwm1.stop()
pwm2.stop()
GPIO.cleanup()
