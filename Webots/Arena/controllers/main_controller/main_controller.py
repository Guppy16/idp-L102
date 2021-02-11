"""main_controller controller."""

# from controller import Robot
# import os, sys
# sys.path.insert(1, os.path.join(sys.path[0], '../'))
# from go_home_controller.go_home_controller import go_home, inside_home
# from exit_home import exit_home

from robocar import Robocar
import json

robocar = Robocar()
timestep = int(robocar.getBasicTimeStep())

json.dump(
    {
        "robots": {
            "blueRobot": {
                "pos": [
                    1,
                    0,
                    1
                ]
            },
            "redRobot": {
                "pos": [
                    1,
                    0,
                    -1
                ]
            }
        },
        "blocks": []
    },
    open('vision.json', 'w+')
)

MAX_SPEED = 5
HOME = [1.0, -1.0]


# Main loop:
while robocar.step(timestep) != -1:
    #print(f"Lookup table is: {distanceSensor.getLookupTable()}")
    robocar.update_sensors()
    if not robocar.tasks.next_task():
        robocar.stop()
        break

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
