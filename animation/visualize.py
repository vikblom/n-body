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

ax.set_xlim(-1,1)
ax.set_ylim(-1,1)
ax.set_zlim(-1,1)

fig.set_facecolor('black')
ax.patch.set_facecolor('black')

points = ax.scatter([],[],[], s=1.0, c='w')

mass = np.fromstring(stdin.readline(), sep=" ")
points.set_sizes(mass)

def get_lines():
    while stdin.readline(): #Skip time for now
        x = np.fromstring(stdin.readline(), sep=" ")
        y = np.fromstring(stdin.readline(), sep=" ")
        z = np.fromstring(stdin.readline(), sep=" ")
        yield x,y,z

def update(data):
    points._offsets3d = data
    return points,

anim = FuncAnimation(fig, update,
                     frames=get_lines,
                     interval=30,
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
