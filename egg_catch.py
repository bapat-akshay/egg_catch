import numpy as np
import cv2
import pickle
import matplotlib.pyplot as plt
from tqdm import tqdm
import sys
import game_env as GE


WIDTH = 10
HEIGHT = 20
OBJ_SPAWN_PERIOD = 7
NUM_EPISODES = 30_000
SHOW_EVERY = 500000
BASKET = 0
EGG = 1
GOLDEN_EGG = 2
POO = 3
OBJECT_TYPES = 4
DUMMY_OBJECT = (WIDTH, HEIGHT, 0)
NUM_ACTIONS = 5
EPISODE_DURATION = 200
FRAME_DURATION = 100

EGG_REWARD = 5
GOLDEN_EGG_REWARD = 10
EGG_DROP_PENALTY = -500
GOLDEN_EGG_DROP_PENALTY = -1000
POO_PENALTY = -500
MOVE_PENALTY = -1

epsilon = 0.9
EPSILON_DECAY = 0.9998
LEARNING_RATE = 0.2
DISCOUNT = 0.95


if len(sys.argv) > 1:
	startQT = sys.argv[1]
else:
	startQT = None


# Decide reward or penalty based on current state
def getReward(env):
	obj = env.objectList[1]

	if obj.y == HEIGHT-1:
		
		if obj.type == EGG:
			if obj.x == env.basket.x:
				return EGG_REWARD
			else:
				return EGG_DROP_PENALTY

		elif obj.type == GOLDEN_EGG:
			if obj.x == env.basket.x:
				return GOLDEN_EGG_REWARD
			else:
				return GOLDEN_EGG_DROP_PENALTY

		elif obj.type == POO:
			if obj.x == env.basket.x:
				return POO_PENALTY
			else:
				return 0

	else:
		return 0


##################
###  Main Code ###
##################

rewards = []

# Populate Q Table with random numbers if no Q Table to start with.
# The Q Table has 5 columns for the following actions:
# 		Do not move ........................(0)
#		Move one space to the left .........(1)
#		Move one space to the right ........(2)
#		Move two spaces to the left ........(3)
#		Move two spaces to the right .......(4)
#
# And several rows, corresponding to the states defined by the tuple
# ((x1, y1, t1), (x2, y2, t2))
# Here, x and y are distances in the x and y directions from the basket
# to an object, while t is the type of the object (egg/goldem egg/poo).
# 1 or 2 specifies the nearest and the next falling object.

if startQT is None:
	QT = {}

	for x1 in range(-WIDTH+1, WIDTH):
		for y1 in range(HEIGHT):
			for t1 in range(1, OBJECT_TYPES):
				for x2 in range(-WIDTH+1, WIDTH+1):
					for y2 in range(HEIGHT+1):
						for t2 in range(0, OBJECT_TYPES):
							QT[(x1, y1, t1), (x2, y2, t2)] = [np.random.uniform(-5, 0) \
							for _ in range(NUM_ACTIONS)]

else:
	with open(startQT, "rb") as file:
		QT = pickle.load(file)

for episode in tqdm(range(NUM_EPISODES)):
	env = GE.GameEnv()
	
	if episode % SHOW_EVERY == 0:
		print(f"Episode #{episode}")
	
	currReward = 0

	# Simulate current episode for a certain number of time steps
	for t in range(EPISODE_DURATION):
		episodeReward = 0
		remove = None

		# Spawn falling objects with given frequency
		if t % OBJ_SPAWN_PERIOD == 0:
			newObj = env.spawnObject()

		# If a "next falling object" exists, define the (x2, y2, t2)
		if len(env.objectList) > 2:
			nextObj = env.basket - env.objectList[2] + (env.objectList[2].type,)
		else:
			nextObj = DUMMY_OBJECT

		# Current state representation tuple
		obs = (env.basket - env.objectList[1] + (env.objectList[1].type,), nextObj)

		# Decide on whether to take a random action
		if np.random.random() > epsilon:
			action = np.argmax(QT[obs])
		else:
			action = np.random.randint(0, NUM_ACTIONS)

		# Move the basket and make the objects fall
		env.basket.move(action)

		for i in range(len(env.objectList)):

			if env.objectList[i].type > 0:

				if env.objectList[i].y < HEIGHT - 1:
					env.objectList[i].y += 1
				else:
					remove = i

		# If an object completes its fall, remove it
		if remove and env.objectList[remove].type > 0:
			env.objectList.pop(remove)
			remove = None

		# Calculate rewards
		if action > 0:
			episodeReward += MOVE_PENALTY

		objReward = getReward(env)
		episodeReward += objReward

		if len(env.objectList) > 2:
			nextObj = env.basket - env.objectList[2] + (env.objectList[2].type,)
		else:
			nextObj = DUMMY_OBJECT

		# Update Q Table based on reward
		newObs = (env.basket - env.objectList[1] + (env.objectList[1].type,), nextObj)
		maxFutureQ = np.max(QT[newObs])
		currQ = QT[obs][action]

		if objReward == 0:
			newQ = (1 - LEARNING_RATE) * currQ + LEARNING_RATE * (episodeReward + 
				DISCOUNT * maxFutureQ)
		else:
			newQ = objReward

		QT[obs][action] = newQ

		# Render the game after every SHOW_EVERY episodes
		if episode % SHOW_EVERY == 0:
			ret = env.refresh(episode, t)

			if not ret:
				break

		currReward += episodeReward

	# The rewards list keeps track of rewards across all episodes, to be plotted for analysis
	rewards.append(currReward)
	if episode % SHOW_EVERY == 0:
		print(f"Reward for episode #{episode}: {currReward}")

	# Decay epsilon. The idea is to reduce the probability of random actions as the training progresses
	epsilon *= EPSILON_DECAY

# Plot the moving average of rewards across all episodes
movingAvg = np.convolve(rewards, np.ones((SHOW_EVERY,)) / SHOW_EVERY, mode="valid")
plt.plot([i for i in range(len(movingAvg))], movingAvg)
plt.show()

# Store Q Table
with open(f"QTable.pickle", "wb") as file:
	pickle.dump(QT, file)
