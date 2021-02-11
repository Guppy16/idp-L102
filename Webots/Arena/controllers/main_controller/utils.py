import numpy as np
import json

def store_block(pos, range=0.1, fName='vision.json'):
    """Store block pos if not within range of any other block"""
    pos = np.array(pos)
    data = json.load(open(fName))
    for block in data["blocks"]:
        block_pos = np.array(block)
        if np.linalg.norm(block_pos - pos) < range:
            return False
    data["blocks"].append(pos.tolist())
    json.dump(data, open(fName, 'w+'))
    print(f"block stored at {pos}")
    return True

def pop_closest_block(my_pos, fName='vision.json'):
    """Get the position of the closest block"""

    # Load blocks
    data = json.load(open(fName))

    # Check if blocks is empty
    if data["blocks"] == []:
        print("No closest block found")
        return None
    
    # Find the closest block
    blocks = np.array(data["blocks"])
    pos = np.array(my_pos)
    # print(blocks - pos)
    blocks_dist = np.linalg.norm(blocks-pos, axis=1)
    print(blocks_dist)
    # closest_block = np.argmin(blocks_dist)
    closest_block = np.random.randint(2)


    # Remove closest block and add it to the json file
    del data["blocks"][closest_block]
    json.dump(data, open(fName, 'w+'))

    return blocks[closest_block]