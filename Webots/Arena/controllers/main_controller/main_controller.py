"""main_controller controller."""

# from controller import Robot
# import os, sys
# sys.path.insert(1, os.path.join(sys.path[0], '../'))
# from go_home_controller.go_home_controller import go_home, inside_home
# from exit_home import exit_home

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
    #print(f"Lookup table is: {distanceSensor.getLookupTable()}")
    # Update sensors
    robocar.update_sensors()

    # Go to middle
    if not robocar.at_location(range = 0.5, [0.0, 0.0]):
        robocar.go_to_location([0.0, 0.0])
    else:
        robocar.find_blocks()

    # Go home
    if not robocar.go_to_location(HOME):
        robocar.stop()

'''
    if blocks<4:
        robot.findBlock(distance)
        goToBlock()
        pickUpBlock()
        robocar.go_home()
        depositBlock()
        blocks+=1
    else:
        pass

'''