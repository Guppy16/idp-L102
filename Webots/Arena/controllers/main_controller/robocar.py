from controller import Robot
import numpy as np

class Robocar(Robot):
    def __init__(self, MAX_SPEED=5, HOME=[1.0,-1.0], MIDDLE=[0.0,0.0], COLOR='b'):
        """Initialise Robots, sensors and motors"""
        Robot.__init__(self)
        timestep = int(self.getBasicTimeStep())
        self.MAX_SPEED = MAX_SPEED
        self.HOME = np.array(HOME)
        self.MIDDLE = MIDDLE
        self.COLOR = COLOR
        self.stack = [self.go_home, self.get_block, self.find_blocks, self.go_middle, self.set_home, self.robocar_hello]

        #init FLAGS!!!
        self.looking_at_block = False
        self.been_to_block = False
        self.gone_over_block = False
        self.match = False

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

    #GO HOME FUNCTIONS

    def getHeadingDegrees(self, cpsVals):
        """Return angle of robot head wrt global north"""
        angle = np.arctan2(cpsVals[0], cpsVals[2])
        bearing = (angle - np.pi/2) * 180 / np.pi 
        bearing %= 360
        return bearing

    def getLocationBearing(self, loc_vec):
        """Return angle between home and global north
        loc_vec: 2D np array [x-coord, z-coord]
        """
        angle = np.arctan2(loc_vec[1], loc_vec[0]) * 180 / np.pi
        angle %= 360
        return angle

    def at_location(self, location, range=0.1):
        """Returns true if robot pos is within range of location"""
        pos = np.array([self.gps_vec[0],self.gps_vec[2]])
        pos -= location
        return np.linalg.norm(pos) < range

    def go_to_location(self, location, range=0.1):
        """Sets the velocities of the motor to return home"""

        if self.at_location(location, range):
            return True
        pos = np.array([self.gps_vec[0],self.gps_vec[2]])
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

    def find_blocks(self):
        """spin until found all blocks"""
        if self.bot_distance < self.top_distance - 20.0 and not self.looking_at_block:
            self.looking_at_block = True
            r = self.bot_distance/500
            theta = self.getHeadingDegrees(self.cps_vec)*np.pi/180
            ds_x = self.gps_vec[0] + 0.08*np.cos(theta) - 0.1*np.sin(theta) #account for 
            ds_z = self.gps_vec[2] + 0.08*np.sin(theta) + 0.1*np.cos(theta)
            block_x = r*np.cos(theta) + ds_x
            block_z = r*np.sin(theta) + ds_z
            print(block_x)
            print(block_z)
        if self.bot_distance > self.top_distance - 20.0 and self.looking_at_block:
            self.looking_at_block = False
        self.rotate()

    def get_block(self, block_coord=[0.03, 0.72]):
        if not self.been_to_block:
            self.go_to_location(block_coord, 0.03)
        if self.at_location(block_coord, 0.03):
            self.been_to_block = True
        if self.been_to_block and not self.gone_over_block:
            if self.COLOR != self.detect_block_colour():
                #forget this block, go to a different one
                pass
            else:
                self.match = True
        if self.been_to_block and not self.gone_over_block and self.match:
            self.go_forward()
        if self.been_to_block and not self.at_location(block_coord, 0.05):
            self.gone_over_block = True
        if self.been_to_block and self.gone_over_block:
            self.been_to_block = False
            self.gone_over_block = False
            self.match = False
            self.stack.append(self.go_home)
            return True 

    def go_home(self):
        """Go home"""
        return self.go_to_location(self.HOME, range=0.1)
        ## Add self.get_out_of_home_ to stack IF not all blocks recovered

    def go_middle(self):
        """Go middle"""
        return self.go_to_location(self.MIDDLE, range=0.05)
        # ADD self.find blocks to stack


    def pop_task(self):
        """Pops the task from the list of tasks and executes the next task"""
        if self.stack == []:
            return False
        task = self.stack.pop()
        # Execute task and push back to stack if not completed
        if not task():
            self.stack.append(task)
        return True

         