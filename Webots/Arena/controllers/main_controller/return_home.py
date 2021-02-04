""" controller to return robot to starting point."""

from controller import Robot, GPS

robot = Robot()

ts = int(robot.getBasicTimeStep())
MAX_SPEED = 5

# Initialize gps
gps = robot.getDevice("gps")
gps.enable(ts)

# Initialize motors
r_motor = robot.getDevice("wheel1")
l_motor = robot.getDevice("wheel2")
l_motor.setPosition(float('inf'))
l_motor.setVelocity(0.0)
r_motor.setPosition(float('inf'))
r_motor.setVelocity(0.0)

