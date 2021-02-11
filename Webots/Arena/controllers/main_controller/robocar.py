from controller import Robot
import json
import numpy as np
import block
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

       
        # self.required_bearing = 0

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
        print("rotating")
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
