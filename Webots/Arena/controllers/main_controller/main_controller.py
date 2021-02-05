"""main_controller controller."""

from controller import Robot

robot = Robot()
timestep = int(robot.getBasicTimeStep())

global MAX_SPEED = 5, HOME = [1.0,1.0]

# Initialise motors
l_motor = robot.getDevice("wheel1")
l_motor.setPosition(float('inf'))
l_motor.setVelocity(0.0)
r_motor = robot.getDevice("wheel2")
r_motor.setPosition(float('inf'))
r_motor.setVelocity(0.0)

# Initialise sensors
gps = robot.getDevice("gps")
gps.enable(ts)

cps = robot.getDevice("compass")
cps.enable(ts)

# Flags
SEARCH_BLOCK = True
RETURN_HOME = False
BLOCKS = 4
ROBOT_NEARBY = False

# Main loop:
while robot.step(timestep) != -1 and BLOCKS:
    if SEARCH_BLOCK:
        r_motor.setVelocity(MAX_SPEED)
        l_motor.setVelocity(MAX_SPEED)
    if RETURN_HOME:
        pass
        
    pass

# Enter here exit cleanup code.
