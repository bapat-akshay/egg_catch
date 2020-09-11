import sys
import cv2
import glob


folder = sys.argv[1]
imgArray = []

for file in range(200):
	print(file)
	img = cv2.imread(f"./{folder}/{file}.jpg")
	imgArray.append(img)

out = cv2.VideoWriter(f'egg-catch-{folder}.mp4', cv2.VideoWriter_fourcc('m','p','4','v'), 
	10, (img.shape[1], img.shape[0]))

for i in imgArray:
	out.write(i)

out.release()