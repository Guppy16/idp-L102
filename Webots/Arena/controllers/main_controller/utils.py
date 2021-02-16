import numpy as np
import json

def store_block(pos, range=0.1, fName='vision.json'):
    """Store block pos if not within range of any other block"""
    pos = np.array(pos)             # Conert pos to np array
    data = json.load(open(fName))   # Load json file of all block pos

    # Check if block is close to any other block
    for block in data["blocks"]:
        block_pos = np.array(block)
        if np.linalg.norm(block_pos - pos) < range:
            return False

    data["blocks"].append(pos.tolist()) # Add block to list
    json.dump(data, open(fName, 'w+'))  # Store block lists in json
    print(f"Block stored at {pos}")
    return True

def pop_closest_block(my_pos, fName='vision.json'):
    """Get the position of the closest block"""

    # Load blocks
    data = json.load(open(fName))

    # Check if blocks is empty
    if data["blocks"] == []:
        print("Empty list of blocks")
        return None
    
    # Find the closest block
    blocks = np.array(data["blocks"])
    pos = np.array(my_pos)
    # print(blocks - pos)
    blocks_dist = np.linalg.norm(blocks-pos, axis=1)
    closest_block = np.argmin(blocks_dist)

    # Remove closest block and add it to the json file
    del data["blocks"][closest_block]
    json.dump(data, open(fName, 'w+'))

    return blocks[closest_block]


# Functions related to list of Block
def next_block(blocks, pos=[0,0]):
    """Given a list of blocks, return block of col=None, pickedUp=False that is closest to pos"""
    pos = np.array(pos)
    next_block = blocks[0]
    closest_dist = 100
    for block in blocks:
        if block.color is None and not block.pickedUp and np.linalg.norm(block.position - pos):
            closest_dist = np.linalg.norm(block.position - pos)
            next_block = block
    if closest_dist == 100:
        print("--- No closest block found")
        return None
    return next_block

def ds_sensor_to_m(val):
    """Cover ds_sensor distance to cm using lookup tables"""
    return val / 500

def is_within_range(a,b, range=0.1):
    """Returns true if np.abs(a-b)<range. Assuming numpy array"""
    try:
        # print(np.linalg.norm(a - b))
        return np.linalg.norm(a - b) < range
    except Exception as e:
        print(e)
        return False
    print("*** utils.is_witin_range !!!Something went wrong.")
    return False
        