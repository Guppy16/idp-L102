"""red_controller controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot, Motor, Keyboard
import sys

# create the Robot instance.
robot = Robot()

# get the time step of the current world.
timestep = int(robot.getBasicTimeStep())
MAX_SPEED = 5

keyboard = Keyboard()
keyboard.enable(timestep)

right_motor = robot.getDevice("wheel1")
left_motor = robot.getDevice("wheel2")

# You should insert a getDevice-like function in order to get the
# instance of a device of the robot. Something like:
#  motor = robot.getDevice('motorname')
#  ds = robot.getDevice('dsname')
#  ds.enable(timestep)

# Main loop:
# - perform simulation steps until Webots is stopping the controller

#INIT DEVICES
left_motor.setPosition(float('inf'))
left_motor.setVelocity(0.0)

right_motor.setPosition(float('inf'))
right_motor.setVelocity(0.0)

def go_forward():
    left_motor.setVelocity(MAX_SPEED)
    right_motor.setVelocity(MAX_SPEED)

def go_backward():
    left_motor.setVelocity(-MAX_SPEED)
    right_motor.setVelocity(-MAX_SPEED)

def turn_left():
    left_motor.setVelocity(MAX_SPEED)
    right_motor.setVelocity(-MAX_SPEED)

def turn_right():
    left_motor.setVelocity(-MAX_SPEED)
    right_motor.setVelocity(MAX_SPEED)

def stop():
    left_motor.setVelocity(0)
    right_motor.setVelocity(0)

while robot.step(timestep) != -1:
    # Read the sensors:
    # Enter here functions to read sensor data, like:
    #  val = ds.getValue()
    key=keyboard.getKey()

    if key==ord("W"):
        go_forward()
    elif key==ord("S"):
        go_backward()
    elif key==ord("A"):
        turn_left()
    elif key==ord("D"):
        turn_right()
    else:
        stop()

    # Process sensor data here.

    # Enter here functions to send actuator commands, like:
    #  motor.setPosition(10.0)






# Enter here exit cleanup code.
