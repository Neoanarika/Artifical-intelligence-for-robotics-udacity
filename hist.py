import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time

size=[10,10]
map_ = np.random.randint(0,2,size)

measurement = [1,0,0,0,1,1,1,0,1,0] #[1,0]: to the right , [0,1]: up
motion = [[1,0],[0,0],[0,1],[-1,0],[0,-1],[-1,0],[1,0],[0,1],[0,1],[0,-1]] #(x,y)
proba_map = np.array([[1/size[0]/size[1] for j in range(size[1])] for i in range(size[0])])

fig = plt.figure()
im = plt.imshow(proba_map, cmap='gist_gray_r', vmin=0, vmax=0.2,interpolation="nearest")

def update_measure(proba_map,m):
	update = np.vectorize(lambda x: 0.6 if x == m else 0.2)
	proba_map = proba_map * update(map_)
	return 1/sum(sum(proba_map))*proba_map

def move(proba_map,m):
	new_map = np.array([[1/size[0]/size[1] for j in range(size[1])] for i in range(size[0])])
	for i in range(size[0]):
		for j in range(size[1]):
			if m[0] != 0 : new_map[i][j] = proba_map[i][(j-m[0])%size[1]]
			else: new_map[i][j] = proba_map[(i+m[1])%size[0]][j]
	return new_map
def init():
    im.set_data(proba_map)

frames = [proba_map]
for i,x in enumerate(measurement):
	proba_map = update_measure(proba_map,x)
	proba_map = move(proba_map,motion[i])
	print(proba_map)
	frames.append(proba_map)

def animate(i):
    im.set_data(frames[i])
    time.sleep(0.5)
    return im


if __name__ == "__main__":
	anim = FuncAnimation(fig, animate, init_func=init, frames=len(frames),
				       interval=50)
	plt.show()
