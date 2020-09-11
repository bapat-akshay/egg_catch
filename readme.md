# Egg-Catch Using Reinforcement Learning

This code uses Q-learning to teach the computer to play the "egg-catch" game.

## Game Rules

1. Objects fall from the sky randomly. These objects can be of three types:
	* Eggs - Good :-)
	* Golden Eggs - Great :-D
	* Poo - Bad :-(
1. Player controls a basket on the ground.
1. There is a reward for catching eggs, and a bigger reward for catching golden eggs.
1. There is a penalty for catching poo or dropping eggs, and an even larger penalty for dropping golden eggs.
1. The objective is to maximize the reward.

## How to Run

* Run the command `python egg_catch.py` if you do not have a Q Table to start with.
* If a Q Table already exists, run `python egg_catch.py <Q-Table-file-name>`.
* The code runs a number of training episodes, and outputs a Q Table that is saved in the directory, as well as a graph showing the moving average of rewards across all training episodes.
* You can change the learning parameters such as number of episodes, learning rate, epsilon, etc. in the python files.
* After every certain number of episodes, a full episode is rendered and you can see the computer trying to catch eggs to maximize the reward. This certain number is defined using the constant "SHOW_EVERY" in egg_catch.py.
* With the current parameters, the code runs 30,000 episodes. Every 5000th episode is shown on the screen and saved in the folder "output_images/".
* A video can be generated from the output images using the "generate_video.py" file. Simply run `python generate_video.py <output-images-subfolder>`. This subfolder can be something like 0, or 5000.

## Output Videos

The first video is the untrained computer playing the game. As you can see, it performs random actions and has a very bad success rate.

![Alt Text](https://github.com/bapat-akshay/egg_catch/blob/master/egg-catch-0.gif)

In the second video, the computer has trained over 25,000 game episodes and does not miss eggs at all.

![Alt Text](https://github.com/bapat-akshay/egg_catch/blob/master/egg-catch-25000.gif)
