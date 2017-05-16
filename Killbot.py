#!/usr/bin/env python
# Simple two DC motor robot class usage example.
# Author: Tony DiCola
# License: MIT License https://opensource.org/licenses/MIT
import time
import subprocess
import os

# Import the Robot.py file (must be in the same directory as this file!).
import Robot
import cwiid

# Set the trim offset for each motor (left and right).  This is a value that
# will offset the speed of movement of each motor in order to make them both
# move at the same desired speed.  Because there's no feedback the robot doesn't
# know how fast each motor is spinning and the robot can pull to a side if one
# motor spins faster than the other motor.  To determine the trim values move the
# robot forward slowly (around 100 speed) and watch if it veers to the left or
# right.  If it veers left then the _right_ motor is spinning faster so try
# setting RIGHT_TRIM to a small negative value, like -5, to slow down the right
# motor.  Likewise if it veers right then adjust the _left_ motor trim to a small
# negative value.  Increase or decrease the trim value until the bot moves
# straight forward/backward.
LEFT_TRIM   = 0
RIGHT_TRIM  = 0


# Create an instance of the robot with the specified trim values.
# Not shown are other optional parameters:
#  - addr: The I2C address of the motor HAT, default is 0x60.
#  - left_id: The ID of the left motor, default is 1.
#  - right_id: The ID of the right motor, default is 2.
robot = Robot.Robot(left_trim=LEFT_TRIM, right_trim=RIGHT_TRIM)

# Now move the robot around!
# Each call below takes two parameters:
#  - speed: The speed of the movement, a value from 0-255.  The higher the value
#           the faster the movement.  You need to start with a value around 100
#           to get enough torque to move the robot.
#  - time (seconds):  Amount of time to perform the movement.  After moving for
#                     this amount of seconds the robot will stop.  This parameter
#                     is optional and if not specified the robot will start moving
#                     forever.
#robot.forward(150, 1.0)   # Move forward at speed 150 for 1 second.
#robot.left(200, 0.5)      # Spin left at speed 200 for 0.5 seconds.

# That's it!  Note that on exit the robot will automatically stop moving.

# Connect to Wii Remote

print("Press 1 + 2 to start")
wm = cwiid.Wiimote()
print("Connected")

# Enable accelerometer
wm.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_ACC

os.chdir('/home/pi/tensorflow')

# Ask user how to begin
subprocess.call(['flite', '-t', "I am here to assist you. What would you like to see?"], shell=False)

# Print state - buttons that are being pushed on remote

while True:
    # print(wm.state['acc'])
    # time.sleep(0.3)
        
    if (wm.state['buttons'] & cwiid.BTN_UP):
        robot.forward(200)
        print ("button 'UP' pressed")

    elif (wm.state['buttons'] & cwiid.BTN_DOWN):
        robot.backward(200)
        print ("button 'DOWN' pressed")

    elif (wm.state['buttons'] & cwiid.BTN_LEFT):
        robot.left(200)
        print ("button 'LEFT' pressed")

    elif (wm.state['buttons'] & cwiid.BTN_RIGHT):
        robot.right(200)
        print ("button 'RIGHT' pressed")

    elif (wm.state['buttons'] & cwiid.BTN_A):
        print ("button 'A' pressed")
        subprocess.call(['flite', '-t', "Acquiring image"], shell=False)
        subprocess.call(['raspistill', '-hf', '-vf', '-o', "image.jpg"], shell=False)
        subprocess.call(['flite', '-t', "Analyzing"], shell=False)
        output1 =  subprocess.check_output(['./tensorflow/contrib/pi_examples/label_image/gen/bin/label_image', '--image=image.jpg'], shell=False)
        subprocess.call(['flite', '-t', "I see a " + output1], shell=False)

    else:
        robot.stop()
