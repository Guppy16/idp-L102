""" controller to return robot to starting point."""

# from controller import Robot, GPS
import numpy as np

# robot = Robot()

# ts = int(robot.getBasicTimeStep())
# MAX_SPEED = 5

# Initialize gps
# gps = robot.getDevice("gps")
# gps.enable(ts)

# Initialize compass
# cps = robot.getDevice("compass")
# cps.enable(ts)

# Initialize motors
# r_motor = robot.getDevice("wheel2")
# l_motor = robot.getDevice("wheel1")
# l_motor.setPosition(float('inf'))
# l_motor.setVelocity(0.0)
# r_motor.setPosition(float('inf'))
# r_motor.setVelocity(0.0)

MAX_SPEED = 5

# Block drop-off coords (ignore height coordinate)
HOME = np.array([1.0, 1.0])
# In competition HOME = START_POSITION

# Get bearing from compass readings. Adapted from Webots documentation
def getHeadingDegrees(compassVals):
    """Return angle of robot head wrt global north"""
    angle = np.arctan2(compassVals[0], compassVals[2])
    bearing = 180 + (angle - np.pi/2) * 180 / np.pi 
    bearing %= 360
    return bearing

def getHomeBearing(homeVec):
    """Return angle between home and global north"""
    unitHomeVector = homeVec / np.linalg.norm(homeVec)
    dotProduct = np.dot(unitHomeVector, [0, 1]) # Dot unit North vector with vector home
    dotProduct = np.clip(dotProduct, -1.0, 1.0)
    return np.arccos(dotProduct) * 180 / np.pi

def reached_home(gps_vals):
    """Returns true if robot pos is within home box"""
    pos = np.array([gps_vals[0],-gps_vals[2]])
    homeVec = HOME - pos
    return np.linalg.norm(homeVec) < 0.05
    print("Arrived home chief")

def go_home(gps_vals, cps_vals, l_motor, r_motor):
    """Sets the velocities of the motor to return home"""
    pos = np.array([gps_vals[0],-gps_vals[2]])
    homeVec = HOME - pos
    heading = getHeadingDegrees(cps_vals)
    homeBearing = getHomeBearing(homeVec)
    
    """print("Bearing home is: " + str(homeBearing))
    print("Heading is: " + str(heading))
    print("Home vector is: " + str(homeVector))
    print("Position is: " + str(position))"""

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





