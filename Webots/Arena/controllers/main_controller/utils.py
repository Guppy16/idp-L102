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

def get_next_block_pos(my_pos, fName='vision.json'):
    """Get the position of the next block"""
    blocks = json.load(open(fName))["blocks"]
    if blocks == []:
        print("No closest block found")
        return None
    blocks = np.array(blocks)
    pos = np.array(my_pos)
    print(blocks - pos)
    blocks_dist = np.linalg.norm(blocks-pos, axis=1)
    closest_block = np.argmin(blocks_dist)
    return blocks[closest_block]