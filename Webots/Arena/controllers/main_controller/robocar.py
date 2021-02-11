from controller import Robot
import json
import numpy as np
from utils import store_block, pop_closest_block
from task_manager import Task, TaskManager


class Robocar(Robot):
    def __init__(self, MAX_SPEED=5, HOME=[1.0, -1.0], MIDDLE=[0.0, 0.0], COLOR='b', NAME="blueRobot", OTHER_NAME="redRobot"):
        """Initialise Robots, sensors and motors"""
        Robot.__init__(self)
        timestep = int(self.getBasicTimeStep())
        self.MAX_SPEED = MAX_SPEED
        self.HOME = np.array(HOME)
        self.MIDDLE = MIDDLE
        self.COLOR = COLOR
        self.NAME = NAME
        self.OTHER_NAME = OTHER_NAME
        self.closest_block_pos = None
        # self.stack = [self.go_home, self.go_middle, self.set_home, self.robocar_hello]

        self.tasks = TaskManager([
            Task(
                target=self.robocar_hello
            ),
            Task(  # Set Home
                target=self.set_home
            ),
            # Task(  # Go to Middle
            #     target=self.go_to_location,
            #     kwargs={"location": self.MIDDLE, "range": 0.1}
            # ),
            Task(  # Head North
                target=self.rotate_to_bearing,
                kwargs={"angle": 0}
            ),
            Task(  # Find blocks
                target=self.find_blocks,
                # This can be got from heading?
                kwargs={"original_bearing": 345}
            ),
            Task(  # Attempt block pick up
                target=self.get_block,
            ),
            Task(  # Go HOME
                target=self.go_to_location,
                kwargs={"location": self.HOME, "range": 0.05}
            ),
        ])

        # init FLAGS!!!
        self.looking_at_block = False
        self.been_to_block = False
        self.gone_over_block = False
        self.match = False

        # Init motors
        self.left_motor = self.getDevice("wheel1")
        self.left_motor.setPosition(float('inf'))
        self.left_motor.setVelocity(0.0)

        self.right_motor = self.getDevice("wheel2")

        self.right_motor.setPosition(float('inf'))
        self.right_motor.setVelocity(0.0)

        # Init sensors
        self.gps = self.getDevice("gps")
        self.gps.enable(timestep)

        self.cps = self.getDevice("compass")
        self.cps.enable(timestep)

        self.ds_bottom = self.getDevice("ds_bottom")
        self.ds_bottom.enable(timestep)

        self.ds_top = self.getDevice("ds_top")
        self.ds_top.enable(timestep)

        self.camera = self.getDevice('camera')
        self.camera.enable(timestep)

    def update_sensors(self):
        """Update sensor values"""
        self.gps_vec = self.gps.getValues()
        self.cps_vec = self.cps.getValues()
        self.bot_distance = self.ds_bottom.getValue()
        self.top_distance = self.ds_top.getValue()
        self.colour_sensor = self.camera.getImageArray()[0][0]

    def set_home(self):
        self.HOME = np.array([self.gps_vec[0], self.gps_vec[2]])
        print(f"Set HOME: {self.HOME}")
        return True

    def robocar_hello(self):
        print("I am a robocar!")
        return True

    def go_forward(self):
        self.left_motor.setVelocity(self.MAX_SPEED)
        self.right_motor.setVelocity(self.MAX_SPEED)

    def go_backward(self):
        self.left_motor.setVelocity(-self.MAX_SPEED)
        self.right_motor.setVelocity(-self.MAX_SPEED)

    def turn_left(self):
        self.left_motor.setVelocity(-self.MAX_SPEED)
        self.right_motor.setVelocity(self.MAX_SPEED)

    def turn_right(self):
        self.left_motor.setVelocity(self.MAX_SPEED)
        self.right_motor.setVelocity(-self.MAX_SPEED)

    def stop(self):
        self.left_motor.setVelocity(0)
        self.right_motor.setVelocity(0)

    def rotate(self):
        self.right_motor.setVelocity(-1)
        self.left_motor.setVelocity(1)

    def getHeadingDegrees(self, cpsVals):
        """Return angle of robot head wrt global north"""
        angle = np.arctan2(cpsVals[0], cpsVals[2])
        bearing = (angle - np.pi/2) * 180 / np.pi
        bearing %= 360
        return bearing

    def rotate_to_bearing(self, angle, tol=5):
        """Rotate until bearing = angle (degrees)"""
        self.rotate()
        return abs(self.getHeadingDegrees(self.cps_vec) - angle) < tol

    def getLocationBearing(self, loc_vec):
        """Return angle between home and global north
        loc_vec: 2D np array [x-coord, z-coord]
        """
        angle = np.arctan2(loc_vec[1], loc_vec[0]) * 180 / np.pi
        angle %= 360
        return angle

    def at_location(self, location, range=0.1):
        """Returns true if robot pos is within range of location"""
        pos = np.array([self.gps_vec[0], self.gps_vec[2]])
        pos -= location
        # print(f"Distance from location: {np.linalg.norm(pos)}")
        return np.linalg.norm(pos) < range

    def go_to_location(self, location, range=0.1):
        """Sets the velocities of the motor to return home"""

        if self.at_location(location, range):
            return True
        pos = np.array([self.gps_vec[0], self.gps_vec[2]])
        heading = self.getHeadingDegrees(self.cps_vec)
        location_bearing = self.getLocationBearing(location - pos)

        # print("Loc Bearing is: " + str(location_bearing))
        # print("Heading is: " + str(heading))
        # print("Loc vec is: " + str(location - pos))
        # print("Pos is: " + str(pos))

        self.go_forward()

        if 360 - heading + location_bearing < heading - location_bearing or heading < location_bearing - 10:
            self.left_motor.setVelocity(self.MAX_SPEED)
            self.right_motor.setVelocity(-0.2 * self.MAX_SPEED)
        elif heading > location_bearing + 10:
            self.left_motor.setVelocity(-0.2 * self.MAX_SPEED)
            self.right_motor.setVelocity(self.MAX_SPEED)
        elif heading > location_bearing + 0.5:
            self.right_motor.setVelocity(0.8 * self.MAX_SPEED)
            self.left_motor.setVelocity(self.MAX_SPEED)
        elif heading < location_bearing - 0.5:
            self.right_motor.setVelocity(self.MAX_SPEED)
            self.left_motor.setVelocity(0.8 * self.MAX_SPEED)

        return False

    def find_blocks(self, original_bearing=345):
        """spin until facing -15 degrees from North"""

        if self.bot_distance < self.top_distance - 20.0 and not self.looking_at_block:
            self.looking_at_block = True
            r = self.bot_distance/500  # cm distance of block from ds_sensor
            theta = self.getHeadingDegrees(self.cps_vec)*np.pi/180

            # account for location of ds_sensor relative to gps sensor
            ds_x = self.gps_vec[0] + 0.08*np.cos(theta) - 0.1*np.sin(theta)
            ds_z = self.gps_vec[2] + 0.08*np.sin(theta) + 0.1*np.cos(theta)

            # global x,z pos of block
            block_x = r*np.cos(theta) + ds_x
            block_z = r*np.sin(theta) + ds_z

            print(f"x: {block_x:.2f}\ty: {block_z:.2f}")

            # Store position in file
            store_block(pos=[block_x, block_z], range=0.05)

        if self.bot_distance > self.top_distance - 20.0 and self.looking_at_block:
            self.looking_at_block = False

        # Once rotated 360
        if self.rotate_to_bearing(original_bearing):
            # Get closest block
            self.closest_block_pos = pop_closest_block(
                my_pos=[self.gps_vec[0], self.gps_vec[2]],
            )
            return True
        return False
    
    def get_block_task(self, block_coord):
        block_coord = self.closest_block_pos
        # Append these as tasks

        # Get close to block
        self.go_to_location(block_coord, range=0.1)
        # Rotate CW until block found
        if np.linalg.norm(self.ds_bottom / 500) < 12:
            self.rotate_to_bearing(self.getHeadingDegrees() - 20)
        # Once found block

        # Check the colour
        # IF not correct color, mark it as red
        # Go over it

    def get_block(self, block_coord=[0.03, 0.72]):

        # if self.go_to_location(block_coord, range=0.05):
        block_coord = self.closest_block_pos
        if not self.been_to_block:
            self.go_to_location(block_coord, 0.03)
            print("going to block!")
        if self.at_location(block_coord, 0.04):
            self.been_to_block = True
            print("arrived at the block")

        if self.been_to_block and not self.gone_over_block:
            print("been to the block, haven't driven over it yet")
            if self.COLOR != self.detect_block_colour():
                # forget this block, go to a different one
                pass
            else:
                self.match = True
        if self.been_to_block and not self.gone_over_block and self.match:
            print("trying to drive over block")
            self.go_forward()
        if self.been_to_block and not self.at_location(block_coord, 0.05):
            self.gone_over_block = True
        if self.been_to_block and self.gone_over_block:
            self.been_to_block = False
            self.gone_over_block = False
            self.match = False
            print("going home")
            # self.stack.append(self.go_home)
            return True
        return False

    def detect_block_colour(self):
        """Return the colour displayed in the camera
        returns: 'b', 'r', or None
        """
        # NOTE: Max value of colour is 256?
        # NOTE: may need to compare values??
        if self.colour_sensor[0] > 70:
            print('red')
            return 'r'
        if self.colour_sensor[2] > 70:
            print('blue')
            return 'b'
        return None

    def detect_other_robot(self, range=0.2, fName='vision.json'):
        """Find co-ordinates of other robot and check if that's within 30 cm"""
        # Write position of robot in a file
        data = json.load(open(fName))

        # Update my pos
        if not self.NAME in data:
            data[self.NAME] = {}
        data[self.NAME]["pos"] = self.gps_vec
        json.dump(data, open(fName, 'w+'))

        # Get position of other robot
        if not self.OTHER_NAME in data:
            return None
        other_robot_pos = np.array(data[self.OTHER_NAME]["pos"])

        # Check if within range
        return np.linalg.norm(other_robot_pos - self.gps_vec) < range
