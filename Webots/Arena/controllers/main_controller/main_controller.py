"""main_controller controller."""

from controller import Robot
import os, sys
sys.path.insert(1, os.path.join(sys.path[0], '../'))
from go_home_controller.go_home_controller import go_home, inside_home
from exit_home import exit_home

from robocar import Robocar

robocar = Robocar()
timestep = int(robocar.getBasicTimeStep())

#INITIALIZE

# robot = Robot()
# timestep = int(robot.getBasicTimeStep())

MAX_SPEED = 5
HOME = [1.0,-1.0]


# Flags
SEARCH_BLOCK = False
RETURN_HOME = True
EXIT_HOME = False
blocks = 0
ROBOT_NEARBY = False


# Main loop:
while robocar.step(timestep) != -1:
    # Get sensor values
    # gps_vals = gps.getValues()
    # cps_vals = cps.getValues()
    # distance = distanceSensor.getValue()
    #print(f"GPS values are: {gps_vals}")
    #print(f"CPS values are: {cps}")
    #print(f"Lookup table is: {distanceSensor.getLookupTable()}")
    robocar.go_forward()

'''
    if blocks<4:
        robot.findBlock(distance)
        goToBlock()
        pickUpBlock()
        returnHome()
        depositBlock()
        blocks+=1
    else:
        pass

'''




'''
    if SEARCH_BLOCK:
        r_motor.setVelocity(MAX_SPEED)
        l_motor.setVelocity(MAX_SPEED)
    if RETURN_HOME:
        go_home(gps_vals, cps_vals, l_motor, r_motor, HOME)
        RETURN_HOME = not inside_home(gps_vals, HOME, 0.1)
        EXIT_HOME = not RETURN_HOME
    if EXIT_HOME:
        EXIT_HOME = exit_home(gps_vals, cps_vals, l_motor, r_motor, HOME)
        SEARCH_BLOCK = not EXIT_HOME
'''
    
# Enter here exit cleanup code
