import numpy as np


WIDTH = 10
HEIGHT = 20
BASKET = 0
EGG = 1
GOLDEN_EGG = 2
POO = 3

colors = {BASKET: (255, 175, 0),
			EGG: (255, 255, 255),
			GOLDEN_EGG: (0, 215, 255),
			POO: (20, 40, 70)}


# Class for eggs and poo
class FallingObject:
	def __init__(self, objType=None):
		self.x = np.random.randint(0, WIDTH)
		self.y = 0
		self.type = objType

		if self.type is not None:
			self.color = colors[self.type]


	def __sub__(self, obj):
		return (self.x - obj.x, abs(self.y - obj.y))


class Basket:
	def __init__(self):
		self.x = 0
		self.y = HEIGHT - 1
		self.color = colors[BASKET]
		self.type = 0


	def __eq__(self, obj):
		return (self.x == obj.x and self.y == obj.y)


	def __sub__(self, obj):
		return (self.x - obj.x, abs(self.y - obj.y))


	def move(self, action):

		if action == 1 and self.x > 0:
			self.x -= 1
		elif action == 2 and self.x < WIDTH-1:
			self.x += 1
		elif action == 3 and self.x > 1:
			self.x -= 2
		elif action == 4 and self.x < WIDTH-2:
			self.x += 2