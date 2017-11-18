#!/usr/bin/env python3

from sys import argv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.animation import FuncAnimation, writers

rcParams['toolbar'] = 'None'

fig, ax = plt.subplots()

fig.set_facecolor('black')

ax.set_xlim(-5,5)
ax.set_ylim(-5,5)

points = ax.scatter([],[], s=1.0, c='w')

dt = 10 / 1000
N = 100

mass = np.random.gamma(2.0, 1.0, N)

x = np.random.normal(0, .1, N)
y = np.random.normal(0, .1, N)
vx = np.random.normal(0, dt*1, N)
vy = np.random.normal(0, dt*1, N)

points.set_sizes(mass)

def update(data):
    global x, y
    x += vx
    y += vy
    points.set_offsets(np.c_[x,y])
    return points,


anim = FuncAnimation(fig, update,
                     frames=500,
                     interval=dt,
                     repeat=False,
                     blit=True)

plt.axis('off')
plt.tight_layout()



if 1 < len(argv):
    print("Saving to:", argv[1], end=" ")
    anim.save(argv[1], writer='imagemagick', fps=30,
              savefig_kwargs={'facecolor':'black'})
    print("Done!")
else:
    plt.show()
