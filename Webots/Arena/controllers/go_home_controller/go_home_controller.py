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
r_motor = robot.getDevice("wheel2")
l_motor = robot.getDevice("wheel1")
l_motor.setPosition(float('inf'))
l_motor.setVelocity(0.0)
r_motor.setPosition(float('inf'))
r_motor.setVelocity(0.0)

# Block drop-off coords (ignore height coordinate)
HOME = [1.0, 1.0]

# Get bearing from compass readings. Adapted from Webots documentation
def getHeadingDegrees(compassVals):
    angle = math.atan2(compassVals[0], compassVals[2])
    bearing = 180 + (angle - math.pi/2) * 180 / math.pi 
    if bearing < 0:
        bearing += 360
    if bearing > 360:
        bearing -= 360
    return bearing

def getHomeBearing(positionCoords):
    homeVector = [HOME[0] - positionCoords[0], HOME[1] - positionCoords[1]]
    unitHomeVector = homeVector / np.linalg.norm(homeVector)
    dotProduct = np.dot(unitHomeVector, [0, 1]) # Dot unit North vector with vector home
    return np.arccos(dotProduct) * 180 / math.pi


while robot.step(ts) != -1:
    position = [gps.getValues()[0], - gps.getValues()[2]]
    heading = getHeadingDegrees(cps.getValues())
    homeBearing = getHomeBearing(position)
    homeVector = [HOME[0] - position[0], HOME[1] - position[1]]
    """print("Bearing home is: " + str(homeBearing))
    print("Heading is: " + str(heading))
    print("Home vector is: " + str(homeVector))
    print("Position is: " + str(position))"""

    if np.linalg.norm(homeVector) > 0.05:
        r_motor.setVelocity(MAX_SPEED)
        l_motor.setVelocity(MAX_SPEED)
        if 360 - heading + homeBearing < heading - homeBearing or heading < homeBearing - 10:
            l_motor.setVelocity(MAX_SPEED)
            r_motor.setVelocity(-0.2 * MAX_SPEED)
        elif heading > homeBearing + 10:
            l_motor.setVelocity(-0.2 * MAX_SPEED)
            r_motor.setVelocity(MAX_SPEED)
        elif heading > homeBearing + 0.5:
            r_motor.setVelocity(0.8 * MAX_SPEED)
            l_motor.setVelocity(MAX_SPEED)
        elif heading < homeBearing - 0.5:
            r_motor.setVelocity(MAX_SPEED)
            l_motor.setVelocity(0.8 * MAX_SPEED)
    else:
        r_motor.setVelocity(0)
        l_motor.setVelocity(0)
        print('Arrived home, chief')            





