"""main_controller controller."""

# from controller import Robot
# import os, sys
# sys.path.insert(1, os.path.join(sys.path[0], '../'))
# from go_home_controller.go_home_controller import go_home, inside_home
# from exit_home import exit_home

from robocar import Robocar
import json
from task_manager import Task, TaskManager
import numpy as np
import block
import utils

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

blocks = []



def go_to_location(location, range=0.1):
        """Sets the velocities of the motor to return home"""

        if robocar.at_location(location, range):
            return True
        pos = np.array([robocar.gps_vec[0], robocar.gps_vec[2]])
        heading = robocar.getHeadingDegrees()
        location_bearing = robocar.getLocationBearing(location - pos)

        # print("Loc Bearing is: " + str(location_bearing))
        # print("Heading is: " + str(heading))
        # print("Loc vec is: " + str(location - pos))
        # print("Pos is: " + str(pos))

        robocar.go_forward()

        if 360 - heading + location_bearing < heading - location_bearing or heading < location_bearing - 10:
            robocar.left_motor.setVelocity(robocar.MAX_SPEED)
            robocar.right_motor.setVelocity(-0.2 * robocar.MAX_SPEED)
        elif heading > location_bearing + 10:
            robocar.left_motor.setVelocity(-0.2 * robocar.MAX_SPEED)
            robocar.right_motor.setVelocity(robocar.MAX_SPEED)
        elif heading > location_bearing + 0.5:
            robocar.right_motor.setVelocity(0.8 * robocar.MAX_SPEED)
            robocar.left_motor.setVelocity(robocar.MAX_SPEED)
        elif heading < location_bearing - 0.5:
            robocar.right_motor.setVelocity(robocar.MAX_SPEED)
            robocar.left_motor.setVelocity(0.8 * robocar.MAX_SPEED)

        return False
    

def find_blocks():
        """spin until facing -15 degrees from North"""
        if robocar.original_heading is None:
            robocar.original_heading = robocar.getHeadingDegrees()

        if robocar.bot_distance < robocar.top_distance - 20.0 and not robocar.looking_at_block:
            robocar.looking_at_block = True
            r = robocar.bot_distance/500  # cm distance of block from ds_sensor
            theta = robocar.getHeadingDegrees()*np.pi/180

            # account for location of ds_sensor relative to gps sensor
            ds_x = robocar.gps_vec[0] + 0.08*np.cos(theta) - 0.1*np.sin(theta)
            ds_z = robocar.gps_vec[2] + 0.08*np.sin(theta) + 0.1*np.cos(theta)

            # global x,z pos of block
            block_x = r*np.cos(theta) + ds_x
            block_z = r*np.sin(theta) + ds_z

            print(f"x: {block_x:.2f}\ty: {block_z:.2f}")

            # Store position in file


            position = np.array([block_x, block_z])

            # Check if block is close to the other robot
            other_robot_pos = robocar.get_other_robot_pos()
            if not other_robot_pos is None:
                other_robot_pos = np.array([other_robot_pos[0], other_robot_pos[2]])
                if np.linalg.norm(other_robot_pos - position) < 0.3:
                    print("Block close to other robot")
                    return False

            #appends a block to the list with its position, and it has not been picked up yet
            currentBlock = block.Block(position, False)
            blocks.append(currentBlock)

            print(f"Blocks length is {len(blocks)}")
            for i in range(len(blocks)):
                print(f"I am block {i}")
                print(f"My position is {blocks[i].getPosition()}")

            print(f"Blocks is: {blocks}")

            utils.store_block(pos=[block_x, block_z], range=0.05)

        if robocar.bot_distance > robocar.top_distance - 20.0 and robocar.looking_at_block:
            robocar.looking_at_block = False

        # Once rotated 360
        if robocar.rotate_to_bearing(robocar.original_heading - 15):
            print("Finished rotation")
            # Reset original heading
            robocar.original_heading = None

            # Get closest block
            robocar.closest_block_pos = utils.pop_closest_block(
                my_pos=[robocar.gps_vec[0], robocar.gps_vec[2]],
            )
            return True
        return False

def get_block(block_coord=[0.03, 0.72]):
        # Get close to block
        # Look around to find block
        # Check the colour
        # Go over it
        # if self.go_to_location(block_coord, range=0.05):

        block_coord = robocar.closest_block_pos
        #if haven't been to the block, go to the block
        if not robocar.been_to_block:
            go_to_location(block_coord, 0.03)
            print("going to block!")
        
        #if at the block, 

        if robocar.at_location(block_coord, 0.04):
            robocar.been_to_block = True
            print("arrived at the block")

        if robocar.been_to_block and not robocar.gone_over_block:
            print("been to the block, haven't driven over it yet")
            print("ROTATING TO READ COLOR")
            robocar.rotate()
            # robocar.rotate_to_bearing(robocar.getHeadingDegrees() - 100)
            detectedColor="b"
            if robocar.COLOR != detectedColor:
                # forget this block, go to a different one
                pass
            else:
                robocar.match = False
        if robocar.been_to_block and not robocar.gone_over_block and robocar.match:
            print("trying to drive over block")
            robocar.go_forward()
        if robocar.been_to_block and not robocar.at_location(block_coord, 0.05):
            robocar.gone_over_block = True
        if robocar.been_to_block and robocar.gone_over_block:
            robocar.been_to_block = False
            robocar.gone_over_block = False
            robocar.match = False
            print("going home")
            # self.stack.append(self.go_home)
            return True
        return False

def find_target_block():
    """Rotate until target block found"""
    # Look around to find block and check colour
    if robocar.original_heading is None:
        robocar.looking_at_block = False
        robocar.original_heading = robocar.getHeadingDegrees()

    # Check distance
    if abs(robocar.bot_distance) < 0.07:
        robocar.looking_at_block = True
        return True
    
    # Once rotate 360, block not found
    if robocar.rotate_to_bearing(robocar.original_heading - 15):
        # Reset original heading
        robocar.original_heading = None
        robocar.looking_at_block = False
        return True
    return False

def check_block_colour():
    """Rotate until block colour detected"""
    if robocar.original_heading is None:
        robocar.match = False
        if not robocar.looking_at_block:
            return True
        robocar.original_heading = robocar.getHeadingDegrees()
    
    col = robocar.detect_block_colour()
    if not col is None:
        if col == robocar.COLOR:
            robocar.match = True
        else:
            robocar.match = False
        return True

    # Once rotate 360, block not found
    if robocar.rotate_to_bearing(robocar.original_heading - 15):
        # Reset original heading
        robocar.original_heading = None
        robocar.match = False
        return True
    return False

def drive_over_block():
    if robocar.count > 0:
        robocar.go_forward()
        robocar.count -= 1
        return False
    robocar.count = 100
    return True

def go_to_block(tm):
    # Get close to the block
    tm.push_tasks_in_reverse([
        Task(
            target=go_to_location,
            kwargs={"location":robocar.closest_block_pos, "range":0.30}
        ),
        Task(
            target=find_target_block
        ),
        Task(
            target=check_block_colour
        ),
        Task(
            target=drive_over_block
        )
    ])

    return True

    # block_coord = robocar.closest_block_pos
    

    



def add_collect_block_tasks(tm):
    """ """
    if blocksCollected >= 4:
        return True

    print("adding tasks")
    tm.push_tasks_in_reverse([
        # Task(  # Head North
        #     target=robocar.rotate_to_bearing,
        #     kwargs={"angle": 0}
        # ),
        Task(  # Find blocks
            target=find_blocks,
            # This can be got from heading?
            # kwargs={"original_bearing": 345}
        ),
        Task(  # Get blocks
            target=go_to_block,
            kwargs={"tm":tm}
        ),
        Task(
            target=add_collect_block_tasks,
            kwargs={"tm":tm}
        )
    ])

    return True

tasks = TaskManager([])

tasks.push_task(Task(
    target=add_collect_block_tasks,
    kwargs={"tm":tasks}
))

tasks.push_tasks_in_reverse([
    Task(
        target=robocar.robocar_hello
    ),
    Task(  # Set Home
        target=robocar.set_home
    ),
    # Task(  # Go to Middle
    #     target=go_to_location,
    #     kwargs={"location": robocar.MIDDLE, "range": 0.1}
    # ),
    # Task(  # Head North
    #     target=robocar.rotate_to_bearing,
    #     kwargs={"angle": 0}
    # ),
    # Task(  # Find blocks
    #     target=find_blocks,
    #     # This can be got from heading?
    #     kwargs={"original_bearing": 345}
    # ),
    # Task(  # Get blocks
    #     target=get_block,
    # ),
    # Task(  # Go HOME
    #     target=go_to_location,
    #     kwargs={"location": robocar.HOME, "range": 0.05}
    # ),
])




MAX_SPEED = 5
HOME = [1.0, -1.0]
blocksCollected=0


# Main loop:
while robocar.step(timestep) != -1:
    #print(f"Lookup table is: {distanceSensor.getLookupTable()}")
    robocar.update_sensors()

    if not tasks.next_task():
        robocar.stop()
        break
    
    # if blocksCollected<4:

    #     if not findBlock():
    #         findBlock()
        



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
