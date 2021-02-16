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
from block import Block
import utils

robocar = Robocar()
robocar.robocar_hello()

timestep = int(robocar.getBasicTimeStep())

movementstep=32
rotationstep=3
collisiondistance=1


def find_blocks(other_robot_threshold=0.3):
    """Rotate and Check if what we're seeing is a wall or a block"""

    # Keep track of the original heading
    if robocar.original_heading is None:
        print(f"---Setting original heading: {robocar.getHeadingDegrees():.2f}")
        robocar.original_heading = robocar.getHeadingDegrees()

    # Check if ds sensor sees a wall
    if robocar.found_wall() and robocar.looking_at_block:
        robocar.looking_at_block = False

    # Check if ds sensor sees a block
    if not robocar.looking_at_block and robocar.found_object():
        robocar.looking_at_block = True

        block_pos = robocar.get_ds_sensor_object_pos()

        # Check if block is close to the other robot
        if utils.is_within_range(robocar.get_other_robot_pos(), block_pos, range=other_robot_threshold):
            print("--- Object close to other robot. Ignoring it")
        elif utils.is_within_range(block_pos, robocar.HOME, range=0.2):
            print("--- Object close to HOME. ignoring it")
        elif any([utils.is_within_range(block_pos, b.position, range=0.1) for b in blocks]):
            print("--- Object is close to another block. Ignoring it")
        else:
            print("--- Found a block. Adding it to the list...")
            # Add block to list of blocks
            # Appends a block to the list with its position, and it has not been picked up yet
            
            # ADD some algo to check if we have already "attempted" to pick up this block
            # So that we don't try to pick it up again!
            blocks.append(Block(block_pos, False))

            # Add block pos to a file
            utils.store_block(pos=[block_pos[0], block_pos[1]], range=0.05)

    # Once rotated 360
    if robocar.rotate_to_bearing(robocar.original_heading - 15):
        print("---Finished rotation")
        # Reset original heading
        robocar.original_heading = None
        robocar.stop()

        # Print list of blocks
        for b in blocks:
            print(b)

        # Get closest block
        # robocar.closest_block_pos = utils.pop_closest_block(
        #     my_pos=[robocar.gps_vec[0], robocar.gps_vec[2]],
        # )
        robocar.target_block = utils.next_block(blocks, pos=[robocar.gps_vec[0], robocar.gps_vec[2]])
        print("---Finished scanning blocks")
        return True

    # Return false to advance the timestep
    return False

def rotate_to_target_block():
    """Rotate until target block found"""
    # Set original heading
    if robocar.original_heading is None:
        robocar.looking_at_block = False
        robocar.original_heading = robocar.getHeadingDegrees()

    # Check if ds sensors have found a block within 25 cm
    # print(utils.ds_sensor_to_m(robocar.bot_distance))
    if robocar.found_object() and abs(utils.ds_sensor_to_m(robocar.bot_distance)) < 0.25:
        print("Found target block")
        robocar.looking_at_block = True
        return True
    
    # IF block hasn't been found after rotating 360, then ignore this block
    if robocar.rotate_to_bearing(robocar.original_heading + 10, dir='CCW'):
        # Reset original heading
        print("Did not find target block")
        robocar.original_heading = None
        robocar.looking_at_block = False
        return True
    return False

def check_block_colour():
    """Assuming the colour sensor is looking at a block. Set robocar.match if color matches"""

    col = robocar.detect_block_colour()
    if not col is None:
        # Update colour of block in objects list
        robocar.target_block.color = col
        # if col == robocar.COLOR:
        #     robocar.match = True
        # else:
        #     robocar.match = False
    return True

def drive_around_block():
    """Somehow drive around the object"""
    return True
    # Try rotating CCW and then turn_and_drive
    robocar.drive(robocar.rotate, count=20, dir='CCW')
    robocar.drive(robocar.turn_and_drive, 100)

    return True

## START redundant functions

def drive_over_block():
    """Turn and drive over block"""
    for _ in range(100):
        robocar.update_sensors()
        robocar.turn_and_drive()
        robocar.step(timestep)

def deposit_block_at_home():
    """Reverse from home until count = 0"""
    for _ in range(100):
        robocar.update_sensors()
        robocar.go_backward()
        robocar.step(timestep)
    
## -- END of redundant functions

# idk if this actually works?
def check_front_clear():
    for _ in range(10):
        robocar.turn_left()
        robocar.step(rotationstep)
        robocar.stop()
        robocar.step(rotationstep)
        robocar.update_sensors()
        if robocar.bot_distance < collisiondistance or robocar.top_distance < collisiondistance:
            return False
        else:
            pass

    robocar.frontClear=50
    return True


def go(location, range=0.2):

    # Check if location is close by
    if robocar.at_location(location, range):
        return True

    # Turn to the right heading
    robocar.turn_to(location)

    # Update the sensors
    robocar.update_sensors()

    # Check if the front is clear
    if robocar.frontClear < 1:
        robocar.stop()
        check_front_clear()

    if robocar.frontClear<1:
        print("ABORT FRONT NOT CLEAR ABORT")

    # Otherwise, advance the timestep and keep on going
    elif robocar.frontClear > 0:
        robocar.turn_to(location)
        robocar.go_forward()
        robocar.frontClear -= 1
        robocar.step(movementstep)
        go(location, range)

HOME = [1.0, -1.0]
MIDDLE = [0.0, 0.0]
blocksCollected=0

blocks = []

robocar.step(timestep)
robocar.update_sensors()
robocar.set_home()

# Main loop:
while robocar.step(timestep) != -1:
    #print(f"Lookup table is: {distanceSensor.getLookupTable()}")

    print(robocar.getTime())

    # Check if the time is 4:30
    # Go home

    robocar.update_sensors()

    # Look around for blocks
    robocar.looking_at_block = False
    while not find_blocks():
        robocar.update_sensors()
        robocar.step(timestep)

    # If a target block hasn't been identified, move around
    # TO BE IMPLEMENTED
    if robocar.target_block is None:
        go(MIDDLE)
        continue

    # Otherwise, go to closest block
    print(f"Next block at {robocar.target_block.position}")
    go(robocar.target_block.position, range=0.35)

    # Look around to find target block
    while not rotate_to_target_block():
        robocar.update_sensors()
        robocar.step(timestep)

    # Check colour of block
    if robocar.looking_at_block:
        check_block_colour()

    # Pick up block if correct colour
    # robocar.count = 100
    if robocar.target_block.color == robocar.COLOR:
        print("---Found block with matching colour")
        robocar.drive(robocar.turn_and_drive, 30)   # Drive over block
        go(robocar.HOME)                            # Drive back home
        robocar.drive(robocar.go_forward, 15)       # Drive a few cm forwards
        robocar.drive(robocar.go_backward, 40)      # Reverse out of home

        robocar.target_block.position = robocar.HOME    # Set new position of block

    else: # Drive around block if it's not the correct colour
        print("Block is not the right colour. Driving around it")
        while not drive_around_block():
            robocar.update_sensors()
            robocar.step(timestep)


    for b in blocks:
        print(b)


    # go(MIDDLE)

    print("gone to the middle!")

    robocar.stop()
    print("Finishing up robot")


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
