from controller import Robot
import json
import numpy as np
import block
import utils
from task_manager import Task, TaskManager


class Robocar(Robot):
    def __init__(self, MAX_SPEED=10, HOME=[1.0, -1.0], MIDDLE=[0.0, 0.0], COLOR='b', NAME="blueRobot", OTHER_NAME="redRobot"):
        """Initialise Robots, sensors and motors"""
        Robot.__init__(self)
        timestep = int(self.getBasicTimeStep())
        self.MAX_SPEED = MAX_SPEED
        self.HOME = np.array(HOME)
        self.MIDDLE = MIDDLE
        self.NAME = self.getName()
        self.COLOR = 'b' if self.NAME == 'blueRobot' else 'r'
        self.timestep = 32
        self.frontClear = 0

        self.OTHER_NAME = "redRobot" if self.COLOR == 'b' else 'blueRobot'
        # self.closest_block_pos = None
        self.target_block = None
        self.original_heading = None
        # self.stack = [self.go_home, self.go_middle, self.set_home, self.robocar_hello]


        # Init FLAGS!!!
        self.looking_at_block = False
        self.been_to_block = False
        self.gone_over_block = False
        self.match = False
        self.count = 100

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
        print(f"{self.NAME} Set HOME: {self.HOME}")
        return True

    def robocar_hello(self):
        print("I am a robocar!")
        print(f"My details:{self.NAME}\t{self.COLOR}\nOther Robot:{self.OTHER_NAME}")
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

    def turn_and_drive(self, dir='CW'):
        """Move forwards and turn"""
        if dir == 'CW':
            self.right_motor.setVelocity(0.5*self.MAX_SPEED)
            self.left_motor.setVelocity(0.9*self.MAX_SPEED)
        else:
            self.right_motor.setVelocity(0.9*self.MAX_SPEED)
            self.left_motor.setVelocity(0.5*self.MAX_SPEED)   

    def stop(self):
        self.left_motor.setVelocity(0)
        self.right_motor.setVelocity(0)

    def drive(self, f, count, *args, **kwargs):
        """Execute a driving function for count timesteps"""
        self.stop()
        for _ in range(count):
            self.step(self.timestep)
            self.update_sensors()
            f(*args, **kwargs)


    def rotate(self, dir='CW'):
        """Set rotation of motors to rotate CW or CCW"""
        if dir == 'CW':
            self.right_motor.setVelocity(-0.5*self.MAX_SPEED)
            self.left_motor.setVelocity(0.5*self.MAX_SPEED)
        else:
            self.right_motor.setVelocity(0.5*self.MAX_SPEED)
            self.left_motor.setVelocity(-0.5*self.MAX_SPEED)

    def get_relative_pos(self, loc=[0,0]):
        """Return 2D x-z position of robot"""
        return np.array([self.gps_vec[0], self.gps_vec[2]] - np.array(loc))

    def getHeadingDegrees(self):
        """Return angle of robot head wrt global north"""
        angle = np.arctan2(self.cps_vec[0], self.cps_vec[2])
        bearing = (angle - np.pi/2) * 180 / np.pi
        bearing %= 360
        return bearing

    def rotate_to_bearing(self, angle, tol=5, dir='CW'):
        """Rotate until bearing = angle (degrees)"""
        angle %= 360 # Ensure that the angle is 0 - 360
        self.rotate(dir)
        return abs(self.getHeadingDegrees() - angle) < tol

    def getLocationBearing(self, loc_vec):
        """Return angle between location and global north
        loc_vec: 2D np array [x-coord, z-coord]
        """
        angle = np.arctan2(loc_vec[1], loc_vec[0]) * 180 / np.pi
        angle %= 360
        return angle

    def rotate_to_location(self, location, tol=5):
        """Given a location, rotate to that bearing"""
        location_bearing = self.getLocationBearing(-self.get_relative_pos(location))
        my_bearing = self.getHeadingDegrees()


        if my_bearing < location_bearing or 360 - my_bearing + location_bearing < my_bearing - location_bearing:
            self.rotate(dir='CW')
        else:
            self.rotate(dir='CCW')

        return abs(location_bearing - my_bearing) < tol or 360 - abs(location_bearing - my_bearing) < tol


    def get_ds_sensor_object_pos(self):
        """Get 2D position of object form bottom distance sensor"""
        r = utils.ds_sensor_to_m(self.bot_distance)
        theta = self.getHeadingDegrees()*np.pi/180

        # global x,z pos of block
        block_x = r*np.cos(theta)
        block_z = r*np.sin(theta)

        # account for location of ds_sensor relative to gps sensor
        block_x += self.gps_vec[0] + 0.08*np.cos(theta) - 0.1*np.sin(theta)
        block_z += self.gps_vec[2] + 0.08*np.sin(theta) + 0.1*np.cos(theta)

        position = np.array([block_x, block_z])
        print(f"Found object at\tx: {block_x:.2f}\tz: {block_z:.2f}")
        return position

    # def turn_to(self,location, range=0.1):
    #     """Rotate until pointing in the right direction"""
    #     print("----- Turning to location")

    #     self.update_sensors()
    #     pos = np.array([self.gps_vec[0], self.gps_vec[2]])
    #     heading = self.getHeadingDegrees()
    #     location_bearing = self.getLocationBearing(location - pos)
    #     # print(f"location is {location}")
    #     # print(f"pos is {pos}")
    #     # print(f"heading is {heading}")
    #     # print(f"location bearing is is {location_bearing}")

    #     if heading > location_bearing - 10 and heading < location_bearing + 10:
    #         self.stop()
    #         print("Done turning.")
    #         return

    #     elif heading < location_bearing:
    #         self.turn_right()
    #         print("Turning right")
    #         self.step(self.timestep)
    #         self.stop()
    #         self.turn_to(location)

    #     elif heading > location_bearing:
    #         self.turn_left()
    #         print("Turning left")
    #         self.step(self.timestep)
    #         self.stop()
    #         self.turn_to(location)

    def turn_left_time(self,time, range=0.1):
        #turns a number of degrees
        """Advance enough time steps to turn left"""
        self.turn_left()
        self.step(time)
        self.stop()

    def rotate_cw_by(self, angle):
        """rotates through the angle, if the angle is negative then it is anticlockwise"""
        heading = self.getHeadingDegrees()
        dir = "CW" if angle > 0 else "CCW"
        while abs(self.getHeadingDegrees() - heading) < abs(angle) or abs(self.getHeadingDegrees() - heading + np.sign(angle)*360) < abs(angle):
            self.drive(self.rotate, count=10, dir=dir) 
        self.stop()

    def at_location(self, location, range=0.1):
        """Returns true if robot pos is within range of location"""
        if location is None:
            return False
        
        location = np.array(location)
        pos = np.array([self.gps_vec[0], self.gps_vec[2]])
        # print(pos)
        pos -= location
        # print(f"Distance from location: {np.linalg.norm(pos)}")
        return np.linalg.norm(pos) < range

    def found_wall(self, wall_threshold=20.0):
        """Check if ds sensors are looking at a wall"""
        return self.bot_distance > self.top_distance- wall_threshold


    def found_object(self, wall_threshold=20.0):
        """Check if ds_sensors have found an object"""
        return self.bot_distance < self.top_distance - wall_threshold

    def detect_block_colour(self, fName='vision.json'):
        """Return the colour displayed in the camera
        returns: 'b', 'r', or None
        """
        # NOTE: Max value of colour is 256?
        # NOTE: may need to compare values??
        print(f"Detecting block color. Block color reading is {self.colour_sensor}")
        if self.colour_sensor[0] > 70:
            print('+++RED')
            return 'r'
        if self.colour_sensor[2] > 70:
            print('+++BLUE')
            return 'b'

        # Otherwise check the json file for irregular colours
        data = json.load(open(fName))
        if any([np.linalg.norm(np.array(self.colour_sensor) - np.array(col)) < 10 for col in data["colours"]["red"]]):
            print('+++RED')
            return 'r'
        if any([np.linalg.norm(np.array(self.colour_sensor) - np.array(col)) < 10 for col in data["colours"]["blue"]]):
            print('+++BLUE')
            return 'b'
        
        print(f"+++UNIDENTIFIED BLOCK with colour: {self.colour_sensor}")
        return None

    def update_my_pos(self, fName='vision.json'):

        # Write position of robot in a file
        data = json.load(open(fName))

        # Update my pos
        if not self.NAME in data:
            data[self.NAME] = {}
        data[self.NAME]["pos"] = self.gps_vec
        json.dump(data, open(fName, 'w+'))

    def get_other_robot_pos(self, fName='vision.json'):
        """Return x-z position of other robot"""
        # Write position of robot in a file
        data = json.load(open(fName))

        # Get position of other robot
        if not self.OTHER_NAME in data['robots']:
            print("Other robot pos not found")
            return None
        other_robot_pos = data['robots'][self.OTHER_NAME]["pos"]
        # print(f"Other robot pos: {other_robot_pos}")
        return np.array([other_robot_pos[0], other_robot_pos[2]])

    # def detect_other_robot(self, range=0.2, fName='vision.json'):
    #     """Find co-ordinates of other robot and check if that's within 30 cm"""


    #     # Check if within range
    #     return np.linalg.norm(other_robot_pos - self.gps_vec) < range
