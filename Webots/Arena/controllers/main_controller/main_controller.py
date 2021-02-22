"""main_controller controller."""

from robocar import Robocar
import numpy as np
np.set_printoptions(formatter={'float': lambda x: "{0:0.2f}".format(x)})
from block import Block
import utils

robocar = Robocar()
robocar.robocar_hello()

timestep = int(robocar.getBasicTimeStep())
rotationstep=3

def find_blocks(blocks, other_robot_threshold=0.3):
    """Rotate and Check if what we're seeing is a wall or a block"""

    # Keep track of the original heading
    if robocar.original_heading is None:
        robocar.original_heading = robocar.getHeadingDegrees()

    # Check if ds sensor sees a wall
    if robocar.found_wall() and (robocar.looking_at_block or robocar.looking_at_object):
        # print("LOOKING AT WALL")
        robocar.looking_at_block = False
        robocar.looking_at_object = False
        return False

    # Check if ds sensor reads a difference
    if not robocar.looking_at_object and robocar.found_object():
        robocar.looking_at_object = True
        return False

    # Check if ds sensor sees an object and a block
    if robocar.looking_at_object and robocar.found_object():
        robocar.looking_at_block = True
        # print("LOOKING AT BLOCK")

        block_pos = robocar.get_ds_sensor_object_pos()

        # Check if block is close to the other robot
        if utils.is_within_range(robocar.get_other_robot_pos(), block_pos, range=other_robot_threshold):
            print("--- Object close to other robot. Ignoring it")
        elif utils.is_within_range(block_pos, robocar.HOME, range=0.5):
            print("--- Object close to HOME. ignoring it")
        elif any([utils.is_within_range(block_pos, b.position, range=0.15) for b in blocks]):
            print("--- Object is close to another block. Ignoring it")
        else:
            print("--- Found a block. Adding it to the list...")
            # Add block to list of blocks
            # Appends a block to the list with its position, and it has not been picked up yet
            blocks.append(Block(block_pos, False))

            # Add block pos to a file
            # utils.store_block(pos=[block_pos[0], block_pos[1]], range=0.05)

    # Once rotated 360 degrees (tolerance of 15)
    if robocar.rotate_to_bearing(robocar.original_heading - 15):
        print("---Finished scanning blocks")
        
        # Reset original heading
        robocar.original_heading = None
        robocar.stop()
        robocar.step(timestep)
        robocar.update_sensors()

        # Select next block if it is different from the one just attempted
        block = utils.next_block(blocks, pos=[robocar.gps_vec[0], robocar.gps_vec[2]])
        robocar.target_block = None if robocar.target_block == block else block
        
        return True

    # Return false to advance the timestep
    return False

def rotate_to_target_block():
    """Rotate until target block found"""
    # print("---Locating Target block")
    # Set original heading
    if robocar.original_heading is None:
        robocar.looking_at_block = False
        robocar.original_heading = robocar.getHeadingDegrees()

    # Check if ds sensors have found a block within 35 cm
    # print(utils.ds_sensor_to_m(robocar.bot_distance))
    if robocar.found_object() and abs(utils.ds_sensor_to_m(robocar.bot_distance)) < 0.35:
        print("Found target block")
        robocar.looking_at_block = True
        robocar.original_heading = None # Reset original heading
        return True
    
    # IF block hasn't been found after rotating 360, then ignore this block
    if robocar.rotate_to_bearing(robocar.original_heading + 20, dir='CCW'):
        # Reset original heading
        print("Did not find target block")
        robocar.original_heading = None
        robocar.looking_at_block = False
        return True
    return False

def check_block_colour():
    """Assuming the colour sensor is looking at a block. Set robocar.match if color matches"""

    col = robocar.detect_block_colour()
    # If colour is green, then reverse a bit and check the colour again
    if col == 'g': 
        robocar.drive(robocar.go_backward, 10)      # Reverse a bit
        col = robocar.detect_block_colour()
    col = None if col == 'g' else col
    robocar.target_block.color = robocar.colour_sensor if col is None else col
    return True

def drive_around_block():
    """Somehow drive around the object"""

    robocar.drive(robocar.go_backward, 10)      # Reverse a bit

    # Determine which way to go around the block using cross product
    heading = robocar.getHeadingDegrees()    
    if np.cross(robocar.get_relative_pos(), robocar.bearing_to_vec(heading)) > 0:
        robocar.rotate_cw_by(45)
    else:
        robocar.rotate_cw_by(-45)

    heading = robocar.getHeadingDegrees()
    point_x = robocar.gps_vec[0] + 0.3*np.cos(heading*np.pi/180)
    point_z = robocar.gps_vec[2] + 0.3*np.sin(heading*np.pi/180)
    print("Yeah bro, just taking a quick detour to (" + str(point_x) + ", " + str(point_z) + ")")
    print("Current coords are (" + str(robocar.gps_vec[0]) + ", " + str(robocar.gps_vec[2]) + ")")

    go([point_x, point_z], 0.08)

    return True
    


# Function to check if front is clear
def check_front_clear(collisiondistance=1.0):
    for _ in range(20):
        robocar.turn_left()
        robocar.step(rotationstep)
        robocar.stop()
        robocar.step(rotationstep)
        robocar.update_sensors()
        if robocar.bot_distance < collisiondistance and robocar.found_object():
            print("------FRONT NOT CLEAR?")
            return False
        else:
            pass

    robocar.frontClear=50
    return True


def go(location, range=0.2):

    # Exit if location is close by
    if robocar.at_location(location, range):
        return True

    # Turn to the right heading
    while not robocar.rotate_to_location(location, tol=10):
        robocar.update_sensors()
        robocar.step(timestep)

    # Update the sensors
    robocar.update_sensors()

    # Check if the front is clear
    if robocar.frontClear < 1:
        robocar.stop()
        if not check_front_clear():
            drive_around_block()

    if robocar.frontClear<1:
        print("ABORT FRONT NOT CLEAR ABORT")

    # Otherwise, advance the timestep and keep on going
    elif robocar.frontClear > 0:
        # Turn to the right heading
        while not robocar.rotate_to_location(location, tol=10):
            robocar.update_sensors()
            robocar.step(timestep)

        robocar.go_forward()
        robocar.frontClear -= 1
        robocar.step(timestep)
        go(location, range)

blocksCollected=0

# Set home
robocar.step(timestep)
robocar.update_sensors()
robocar.set_home()

blocks = []

# Main loop:
def main_loop(time=300):
    global blocks, blocksCollected

    if robocar.getTime() > time:
        # print("--- returning home")
        go(robocar.HOME)
        # robocar.return_home()
        return

    robocar.update_sensors()
    go(robocar.get_next_loc())

    # Look around for blocks
    robocar.looking_at_block = False
    while not find_blocks(blocks):
        robocar.update_sensors()
        robocar.step(timestep)

    # If a target block hasn't been identified, move around
    if robocar.target_block is None:
        print("Resetting the list of blocks")
        go(robocar.get_next_loc())
        blocks = []
        # blocks = [] # Try resetting list of blocks
        return

    # Otherwise, go to closest block
    print(f"--- Target block located at {robocar.target_block.position}")
    robocar.frontClear = 50
    go(robocar.target_block.position, range=0.3)

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
        robocar.drive(robocar.turn_and_drive, 40)   # Drive over block
        go(robocar.HOME)                            # Drive back home
        robocar.drive(robocar.go_forward, 15)       # Drive a few cm forwards
        robocar.drive(robocar.go_backward, 40)      # Reverse out of home

        robocar.target_block.position = robocar.HOME    # Set new position of block
        blocksCollected += 1                        # Increment the number of blocks collected

    else: # Drive around block if it's not the correct colour
        print("Block is not the right colour. Driving around it")
        drive_around_block()


    # for b in blocks:
    #     print(b)

    robocar.stop()
    print("--- Finished a loop")

# Drive around blue robot if less 120 secs
while robocar.step(timestep) != -1:
    # Drive back home if more than 2 mins passed
    if blocksCollected >= 4 or robocar.getTime() > 150:
        go(robocar.HOME)
        robocar.stop()
        break
    if robocar.NAME != "redRobot":
        continue
    main_loop(time=120)

# Drive around red robot if less 240 secs
while robocar.step(timestep) != -1:
    # Drive back home if more than 2 mins passed
    if blocksCollected >= 4 or robocar.getTime() > 280:
        go(robocar.HOME)
        robocar.stop()
        break
    if robocar.NAME != "blueRobot":
        continue
    main_loop(time=270)
