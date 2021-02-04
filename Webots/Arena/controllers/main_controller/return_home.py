""" controller to return robot to starting point."""

from controller import Robot, GPS
import math
import numpy as np

robot = Robot()

ts = int(robot.getBasicTimeStep())
MAX_SPEED = 5

# Initialize gps
gps = robot.getDevice("gps")
gps.enable(ts)

# Initialize compass
cps = robot.getDevice("compass")
cps.enable(ts)

# Initialize motors
r_motor = robot.getDevice("wheel1")
l_motor = robot.getDevice("wheel2")
l_motor.setPosition(float('inf'))
l_motor.setVelocity(0.0)
r_motor.setPosition(float('inf'))
r_motor.setVelocity(0.0)

# Block drop-off coords (ignore height coordinate)
HOME = [1.0, -1.0]

# Get bearing from compass readings. Adapted from Webots documentation
def getHeadingDegrees(compassVals):
    angle = math.atan2(compassVals[0], compassVals[2])
    bearing = (angle - math.pi/2) * 180 / math.pi
    if bearing < 0:
        bearing += 360
    return bearing

def getHomeBearing(positionCoords):
    homeVector = [HOME[0] - positionCoords[0], HOME[1] - positionCoords[1]]
    unitHomeVector = homeVector / np.linalg.norm(homeVector)
    dotProduct = np.dot(unitHomeVector, HOME)
    return np.arccos(dotProduct / math.sqrt(2)) * 180 / math.pi


while robot.step(ts) != -1:
    position = [gps.getValues[0], gps.getValues[2]]
    heading = getHeadingDegrees(cps.getValues)
    homeBearing = getHomeBearing(position)
    homeVector = [HOME[0] - positionCoords[0], HOME[1] - positionCoords[1]]

    while np.linalg.norm(homeVector) > 0.02:
        if heading > homeBearing + 3:
            l_motor.setVelocity(0.95 * MAX_SPEED)
            r_motor.setVelocity(MAX_SPEED)
        elif heading < homeBearing - 3:
            l_motor.setVelocity(MAX_SPEED)
            r_motor.setVelocity(0.95 * MAX_SPEED)
        else:
            l_motor.setVelocity(MAX_SPEED)
            r_motor.setVelocity(MAX_SPEED)

    print('Arrived home, chief')            





