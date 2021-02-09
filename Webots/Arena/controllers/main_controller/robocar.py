from controller import Robot
import numpy as np

class Robocar(Robot):
    def __init__(self, MAX_SPEED=5, HOME=[1.0,-1.0]):
        """Initialise Robots, sensors and motors"""
        Robot.__init__(self)
        timestep = int(self.getBasicTimeStep())
        self.MAX_SPEED = MAX_SPEED
        self.HOME = np.array(HOME)

        #Init motors
        self.left_motor = self.getDevice("wheel1")
        self.left_motor.setPosition(float('inf'))
        self.left_motor.setVelocity(0.0)

        self.right_motor = self.getDevice("wheel2")

        self.right_motor.setPosition(float('inf'))
        self.right_motor.setVelocity(0.0)

        #Init sensors
        self.gps = self.getDevice("gps")
        self.gps.enable(timestep)

        self.cps = self.getDevice("compass")
        self.cps.enable(timestep)

        self.ds_low = self.getDevice("ds_low")
        self.ds_low.enable(timestep)

        self.ds_high = self.getDevice("ds_high")
        self.ds_high.enable(timestep)

        self.camera = self.getDevice('camera')
        self.camera.enable(timestep)


    def update_sensors(self):
        """Update sensor values"""
        self.gps_vec = self.gps.getValues()
        self.cps_vec = self.cps.getValues()
        self.distance = self.distanceSensor.getValue()
        self.img = self.camera.getImageArray()[0][0]

    def robocar_hello(self):
        print("I am a robocar!")

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
        self.right_motor.setVelocity(-0.2)
        self.left_motor.setVelocity(0.2)

    #GO HOME FUNCTIONS

    def getHeadingDegrees(self, cpsVals):
        """Return angle of robot head wrt global north"""
        angle = np.arctan2(cpsVals[0], cpsVals[2])
        bearing = (angle - np.pi/2) * 180 / np.pi 
        bearing %= 360
        return bearing

    def getLocationBearing(self, loc_vec):
        """Return angle between home and global north"""
        # Check for divide by zero
        if np.linalg.norm(loc_vec) < 0.00001:
            return 0
        loc_vec /= np.linalg.norm(loc_vec)
        dotProduct = np.dot(loc_vec, [1, 0]) # Dot unit North vector with vector home
        dotProduct = np.clip(dotProduct, -1.0, 1.0)
        return 360 - np.arccos(dotProduct) * 180 / np.pi

    def at_location(self, range=0.1, location):
        """Returns true if robot pos is within range of location"""
        pos = np.array([self.gps_vec[0],self.gps_vec[2]])
        pos -= location
        return np.linalg.norm(pos) < range
        print("Arrived home chief")

    def go_to_location(self, location, range=0.1):
        """Sets the velocities of the motor to return home"""

        if self.at_location(range, location):
            return True

        pos = np.array([self.gps_vec[0],self.gps_vec[2]])
        loc_vec = location - pos
        heading = self.getHeadingDegrees(self.cps_vec)
        location_bearing = self.getLocationBearing(loc_vec)

        # print("Bearing home is: " + str(homeBearing))
        # print("Heading is: " + str(heading))
        # print("Home vector is: " + str(homeVec))
        # print("Position is: " + str(pos))

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

    def find_blocks(self, robo_heading):
        """spin until distance sensors have significant discrepancy"""
        if 


        
         

    def detect_block_colour(self):
        """Return the colour displayed in the camera
        returns: 'b', 'r', or None
        """
        # NOTE: Max value of colour is 32
        if 
        return 