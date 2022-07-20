# A Robot that uses Computer Vision to Track a Ball
This robot will track a ball and it will follow the ball using a Raspberry Pi.

| **Engineer** | **School** | **Area of Interest** | **Grade** |
|:--:|:--:|:--:|:--:|
| David | Monta Vista Highschool | Mechanical Engineering | Incoming Senior

![Headstone Image](https://lh3.googleusercontent.com/pw/AM-JKLVbcVsXtbVDlJuw0to8qprEm4nzvpmechAxXFTnBjrnaQnZk5eflwQXT3I46UE1jroaWahA_ZodNRUtbbHt7iFZwZqHAU7C8B2Qf57jLTXL7Mm-1x0gQ9uiL_iphZOY8YwViqiN2oftpD9LLPRMid0=s1934-no?authuser=0)
  
# Third Milestone: Ball Tracking Robot
For my third and final milestone, I finally put all the components together, the chassis and the tracking system to create a ball tracking robot. So during the process of putting it together I had to replace the arduino that was originally on the raspberry pi. The pins on the raspberry pi are similar to the pins on the arduino because both of them have pwm pins and regular digital pins. So to replace the arduino with the raspberry pi, I had to move the speed pin on the motor driver to the pwm pins on the raspberry pi and also move the rest of the pins that are connected to the motor driver to the digital pins on the raspberry pi. After replacing the arduino with the raspberry pi, I also have to change the arduino code to python code. In the code I had a proportional controller that would control the speed of the motor so that when the ball is far away from the vehicle, the speed of the motor would be fast and as it gets closer to the vehicle. And for the left and right proportional controller, the speed of one of the motors would be quick if the ball is really far to the either the left or right side of the vehicle, and as it gets closer to the center of the vehicle, the speed of the motors would slow down. I would use the coordinates of the center of the ball that is given by the tracking ball code to do the calculations for the proportional controllers.

Here is the code for the vehicle and a detailed explanation of the code: (link)

While putting all the components together, I encountered many issues, but the main issue is with the batteries. The batteries that I was originally using ran out really quick and recently I also burned a battery pack because of how I left the batteries running for a long amount of time and it was drawing so much current that it started to really heat up and cause the battery pack to start smoking. Other than that I enjoyed completing the project and seeing it work in the end.


[![David C Milestone 3](https://res.cloudinary.com/marcomontalbano/image/upload/v1658351180/video_to_markdown/images/youtube--6Doy682EGRU-c05b58ac6eb4c4700831b2b3070cd403.jpg)](https://www.youtube.com/watch?v=6Doy682EGRU "David C Milestone 3"){:target="_blank" rel="noopener"}

# Second Milestone: Tracking a Ball

For my second milestone, I used a raspberry pi and a pi camera to track a red ball, and it also tells you where the ball is relative to the camera such as if it is to the camera’s right or left or in front of it. For this to work I used computer vision using OpenCV to track the ball. In the code for tracking the ball I first set up the camera so that it will be on until I stop the program. Next I set the range for the shade of red so that when the camera turns on it will only look for the color within that range. To get the upper and lower range I used a HSV filter which is Hue, Saturation, and Value. This will be used to set the darkest shade of red and the lightest shade of red to narrow down the image to just the color of the ball in the frame. After just detecting the ball, I isolate the particular color that is in the frame, which is the red ball. This is also known as color masking. After isolating the red color, I used a method called cv.HoughCircle(). This method basically detects circles in an image, then it will draw a green circle around that ball and a red dot in the center of the ball. This way I can get the coordinates of where the red dot is, and then figure out if it is to the right of the camera or the left of the camera. While completing the second milestone, I encountered some difficulties and problems. One of the problems was that the cable connecting the raspberry pi to the monitor was broken so I had to get another cable. Another problem I ran into was that in the beginning I was using a green ball instead of a red ball, and using a green ball is harder to isolate as there is also a lot of green in the background.

[![David C Milestone 2](https://res.cloudinary.com/marcomontalbano/image/upload/v1658266488/video_to_markdown/images/youtube--RTmboxN7S_E-c05b58ac6eb4c4700831b2b3070cd403.jpg)](https://www.youtube.com/watch?v=RTmboxN7S_E "David C Milestone 2"){:target="_blank" rel="noopener"}
# First Milestone: Chassis
  

For my first milestone I built the chassis for my main project. Using an arduino, sensor shield, and motor driver to control the speed at which the vehicle moves and the direction. On the robot I have two motors to move the wheels and these motors are connected to a motor driver which is then connected to and powered by a sensor shield that is attached to the arduino. On the motor driver there are 6 wires connecting the motor driver to the sensor shield. Two of the wires control the speed at which the motor will run and 4 will control which direction the motor will turn. The two wires that control the speed of the motors will be connected to a pwm pin so that it can be controlled using analogWrite. This means that when controlling the speed there are more options instead of just having the motors be off or max speed. The rest of the pins do not have to be connected to a pwm pin as it controls the direction at which the vehicle moves. While completing the first milestone, one major problem I ran into is that when I turn the robot on while it is connected to my computer, my computer will automatically shut down, this is because when I turn the robot on, it is putting 5 volts into my computer.


[![David C Milestone 1](https://res.cloudinary.com/marcomontalbano/image/upload/v1656107664/video_to_markdown/images/youtube--TsNfXT9q5ho-c05b58ac6eb4c4700831b2b3070cd403.jpg)](https://www.youtube.com/watch?v=TsNfXT9q5ho "David C Milestone 1")

# Starter Project: Useless Machine
  

For my starter project, I created the Useless Machine. What the useless machine does is when you flip the switch, the robot will flip the switch back. The Useless Machine uses a motor, a PCB (Printed Circuit Board), and battery to power the machine. The motor is the one that moves the arm so that it will flip the switch back. On the PCB there is the switch, two resistors, 2 screw terminals which can connect two or more conductors, but in this case it is connecting both the battery and the motor. The PCB also includes a LED which changes to green when the switch is flipped by a person and it turns red when the machine flips the switch. And lastly it also has a snap switch which basically stops the circuit. When the switch is flipped it will cause the motor to move which will move the arm to flip the switch again. While building this starter project some difficult aspect is soldering, since I have never soldered before and it was also difficult holding the components in place while also soldering. But something I enjoyed while building this project was putting everything together after finishing the circuit. 


[![David C Starter Project](https://res.cloudinary.com/marcomontalbano/image/upload/v1655500037/video_to_markdown/images/youtube--eJ2ibpvaais-c05b58ac6eb4c4700831b2b3070cd403.jpg)](https://www.youtube.com/watch?v=eJ2ibpvaais "David C Starter Project")
