from math import *
import random
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time

landmarks  = [[20.0, 20.0], [80.0, 80.0], [20.0, 80.0], [80.0, 20.0]]
world_size = 100.0


class robot:
    def __init__(self):
        self.x = random.random() * world_size
        self.y = random.random() * world_size
        self.orientation = random.random() * 2.0 * pi
        self.forward_noise = 0.0;
        self.turn_noise    = 0.0;
        self.sense_noise   = 0.0;
    
    def set(self, new_x, new_y, new_orientation):
        if new_x < 0 or new_x >= world_size:
            raise ValueError("X coordinate out of bound")
        if new_y < 0 or new_y >= world_size:
            raise ValueError('Y coordinate out of bound')
        if new_orientation < 0 or new_orientation >= 2 * pi:
            raise ValueError('Orientation must be in [0..2pi]')
        self.x = float(new_x)
        self.y = float(new_y)
        self.orientation = float(new_orientation)
        return self
    
    
    def set_noise(self, new_f_noise, new_t_noise, new_s_noise):
        # makes it possible to change the noise parameters
        # this is often useful in particle filters
        self.forward_noise = float(new_f_noise);
        self.turn_noise    = float(new_t_noise);
        self.sense_noise   = float(new_s_noise);
        return self
    
    
    def sense(self):
        Z = []
        for i in range(len(landmarks)):
            dist = sqrt((self.x - landmarks[i][0]) ** 2 + (self.y - landmarks[i][1]) ** 2)
            dist += random.gauss(0.0, self.sense_noise)
            Z.append(dist)
        return Z
    
    
    def move(self, turn, forward):
        if forward < 0: raise ValueError('Robot cant move backwards')       
        
        # turn, and add randomness to the turning command
        orientation = self.orientation + float(turn) + random.gauss(0.0, self.turn_noise)
        orientation %= 2 * pi
        
        # move, and add randomness to the motion command
        dist = float(forward) + random.gauss(0.0, self.forward_noise)
        x = self.x + (cos(orientation) * dist)
        y = self.y + (sin(orientation) * dist)
        x %= world_size    # cyclic truncate
        y %= world_size
        
        return self
    
    def Gaussian(self, mu, sigma, x):
        
        # calculates the probability of x for 1-dim Gaussian with mean mu and var. sigma
        return exp(- ((mu - x) ** 2) / (sigma ** 2) / 2.0) / sqrt(2.0 * pi * (sigma ** 2))
    
    
    def measurement_prob(self, measurement):
        
        # calculates how likely a measurement should be
        
        prob = 1.0;
        for i in range(len(landmarks)):
            dist = sqrt((self.x - landmarks[i][0]) ** 2 + (self.y - landmarks[i][1]) ** 2)
            prob *= self.Gaussian(dist, self.sense_noise, measurement[i])
        return prob
    
    
    
    def __repr__(self):
        return '[x=%.6s y=%.6s orient=%.6s]' % (str(self.x), str(self.y), str(self.orientation))



def eval(r, p):
    sum = 0.0;
    for i in range(len(p)): # calculate mean error
        dx = (p[i].x - r.x + (world_size/2.0)) % world_size - (world_size/2.0)
        dy = (p[i].y - r.y + (world_size/2.0)) % world_size - (world_size/2.0)
        err = sqrt(dx * dx + dy * dy)
        sum += err
    return sum / float(len(p))

def x_y_split(p):
    x = [i.x for i in p]
    y = [i.y for i in p]
    return [x,y]

def animate(i):
    hist = plt.hist2d(*x_y_split(frames[i]))
    time.sleep(0.2)
    return hist

N_particles = 1000
myrobot = robot()
p = [robot() for i in range(N_particles)]
frames = [p]

fig = plt.figure()
hist = plt.hist2d(*x_y_split(p))

def init():
    hist = plt.hist2d(*x_y_split(p))
    return hist

if __name__ == "__main__":
    for i in range(10):
        myrobot = myrobot.move(0.1, 5.0)
        Z = myrobot.sense()
        p = [bot.set_noise(0.05, 0.05, 5.0).move(0.1,5) for bot in p]
        weights = [part.measurement_prob(Z) for part in p]
        p_re,beta = [],0
        for i in range(N_particles):
            beta += 2*max(weights)*random.random()
            index = 0
            while weights[index] < beta:
                beta = beta - weights[index]
                index = index+1
            p_re.append(p[index])
        p = p_re
        frames.append(p)
    anim = FuncAnimation(fig, animate, init_func=init, frames=len(frames),
                                   interval=50)
    plt.show()
