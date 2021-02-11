import utils

fName="controller_tests/vision_test.json"

def test_store_block():
    utils.store_block(pos=[1,0], fName=fName)
    utils.store_block(pos=[1.05,0], fName=fName)
    utils.store_block(pos=[1.05,0.4], fName=fName)

test_store_block()

def test_get_next_block_pos():
    print(utils.get_next_block_pos(my_pos=[1.0,0.0,0.0],fName=fName))

test_get_next_block_pos()