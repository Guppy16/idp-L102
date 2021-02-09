"""main_controller controller."""

from controller import Robot
import os, sys
sys.path.insert(1, os.path.join(sys.path[0], '../'))
from go_home_controller.go_home_controller import go_home, inside_home
from exit_home import exit_home

robot = Robot()
timestep = int(robot.getBasicTimeStep())

MAX_SPEED = 5
HOME = [1.0,-1.0]

# Initialise motors
l_motor = robot.getDevice("wheel1")
l_motor.setPosition(float('inf'))
l_motor.setVelocity(0.0)
r_motor = robot.getDevice("wheel2")
r_motor.setPosition(float('inf'))
r_motor.setVelocity(0.0)

# Initialise sensors
gps = robot.getDevice("gps")
gps.enable(timestep)

cps = robot.getDevice("compass")
cps.enable(timestep)

# Flags
SEARCH_BLOCK = False
RETURN_HOME = True
EXIT_HOME = False
BLOCKS = 4
ROBOT_NEARBY = False

# Main loop:
while robot.step(timestep) != -1 and BLOCKS:
    # Get sensor values
    gps_vals = gps.getValues()
    cps_vals = cps.getValues()

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
    
# Enter here exit cleanup code
