from controller import Robot
        
class Robocar(Robot):
    def __init__(self):
        Robot.__init__(self)
        timestep = int(self.getBasicTimeStep())

        #Init motors
        self.left_motor = self.getDevice("wheel1")

        left_motor.setPosition(float('inf'))
        left_motor.setVelocity(0.0)

        self.right_motor = self.getDevice("wheel2")

        right_motor.setPosition(float('inf'))
        right_motor.setVelocity(0.0)

        #Init sensors

        self.gps = self.getDevice("gps")
        gps.enable(timestep)

        self.cps = self.getDevice("compass")
        cps.enable(timestep)

        self.distanceSensor = self.getDevice("ds_left")
        distanceSensor.enable(timestep)

        
    
    def robocar_hello(self):
        print("I am a robocar!")

    def go_forward(self):
        self.left_motor.setVelocity(MAX_SPEED)
        self.right_motor.setVelocity(MAX_SPEED)

    def go_backward(self):
        self.left_motor.setVelocity(-MAX_SPEED)
        self.right_motor.setVelocity(-MAX_SPEED)

    def turn_left(self):
        self.left_motor.setVelocity(-MAX_SPEED)
        self.right_motor.setVelocity(MAX_SPEED)

    def turn_right(self):
        self.left_motor.setVelocity(MAX_SPEED)
        self.right_motor.setVelocity(-MAX_SPEED)


    def stop(self):
        self.left_motor.setVelocity(0)
        self.right_motor.setVelocity(0)

    def findBlock(distance):
        print(f"Distance is {distance}")
        if(distance>1):
            turn_right()
        else:
            stop()