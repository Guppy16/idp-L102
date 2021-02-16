import numpy as np

class Block():
   def __init__(self, position, pickedUp=False, color=None):
      self.color = color
      self.position = position
      self.pickedUp = pickedUp

   def getColor(self):
      return self.color

   def getPosition(self):
      return self.position

   def pickedUp(self):
      return self.pickedUp
   
   def __repr__(self):
      return f"Block:\tCol: {str(self.color)}\tPos:{self.position[0]:.2f} {self.position[1]:.2f}\tpickedUp:{self.pickedUp}"
