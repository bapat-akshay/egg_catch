import numpy as np
import cv2
from PIL import Image
import egg_catch_objects as eco


FRAME_DURATION = 100
WIDTH = 10
HEIGHT = 20
OBJECT_TYPES = 4


# The game environment class. This handles the falling objects and the basket
class GameEnv:
	def __init__(self):
		self.game = np.zeros((HEIGHT, WIDTH, 3), np.uint8)
		self.basket = eco.Basket()
		self.objectList = [self.basket]


	# Spawns a falling object from the top of the game window
	def spawnObject(self):
		obj = np.random.randint(1, OBJECT_TYPES)
		newObj = eco.FallingObject(obj)
		self.objectList.append(newObj)
		
		return newObj


	# Display the game window
	def refresh(self, episode, imgCount):
		self.game = np.zeros((HEIGHT, WIDTH, 3), np.uint8)
		ret = True
		
		for obj in self.objectList:
			self.game[obj.y, obj.x] = obj.color

		img = Image.fromarray(self.game, "RGB")
		img = img.resize((300,600))
		cv2.imwrite(f"output_images/{episode}/{imgCount}.jpg", np.array(img))
		cv2.imshow("Egg Catch", np.array(img))

		if (cv2.waitKey(FRAME_DURATION) & 0xFF == ord("q")):
			ret = False

		return ret