import numpy as np

class Block():
    def __init__(self, position, pickedUp, color="unknown"):
        self.color = color
        self.position = position
        self.pickedUp = False
    
    def getColor(self):
       return self.color
    
    def getPosition(self):
       return self.position

    def pickedUp(self):
       return self.pickedUp

    def getColor(self):
       return self.color