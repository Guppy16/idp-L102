from controller import Robot
import numpy as np

class Robocar(Robot):
    def __init__(self, MAX_SPEED=5, HOME=[1.0,-1.0]):
        Robot.__init__(self)
        timestep = int(self.getBasicTimeStep())
        self.MAX_SPEED = MAX_SPEED
        self.HOME = HOME

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

        self.distanceSensor = self.getDevice("ds_left")
        self.distanceSensor.enable(timestep)

        
    
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

    def findBlock(distance):
        print(f"Distance is {distance}")
        if(distance>1):
            turn_right()
        else:
            stop()