#!/usr/bin/env python3


from sys import argv, stdin
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import rcParams
from matplotlib.animation import FuncAnimation, writers

#a = np.fromstring(stdin.readline(), sep=" ")

rcParams['toolbar'] = 'None'

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

#fig.set_facecolor('black')

ax.set_xlim(-5,5)
ax.set_ylim(-5,5)
ax.set_zlim(-5,5)

points = ax.scatter([],[],[], s=1.0, c='b')

N = 100

mass = np.random.gamma(2.0, 1.0, N)

x = np.random.normal(0, .1, N)
y = np.random.normal(0, .1, N)
z = np.random.normal(0, .1, N)
vx = np.random.normal(0, .1, N)
vy = np.random.normal(0, .1, N)
vz = np.random.normal(0, .1, N)

points.set_sizes(mass)

def update(data):
    global x, y, z
    x += vx
    y += vy
    z += vz
    points._offsets3d = (x,y,z)
    return points,


anim = FuncAnimation(fig, update,
                     frames=500,
                     interval=25,
                     repeat=False,
                     blit=False)

plt.axis('off')
plt.tight_layout()



if 1 < len(argv):
    print("Saving to:", argv[1], end=" ")
    anim.save(argv[1], writer='imagemagick', fps=30,
              savefig_kwargs={'facecolor':'black'})
    print("Done!")
else:
    plt.show()
