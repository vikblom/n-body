#!/usr/bin/env python3
from sys import argv, stdin
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Line3DCollection
from matplotlib import rcParams
from matplotlib.animation import FuncAnimation, writers


TAIL_LEN = 10

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

n=20
x = np.random.uniform(0, 1, n)
y  = np.random.uniform(0, 1, n)
z = np.arange(0,n)/n

points_ = np.array([x, y, z]).T.reshape(-1, 1, 3)
segments = np.concatenate([points_[:-1], points_[1:]], axis=1)

tails = Line3DCollection(segments, colors='w', linewidth=0.25)
ax.add_collection(tails)

x_tail = []
y_tail = []
z_tail = []


def get_lines():
    while stdin.readline(): #Skip time for now
        x = np.fromstring(stdin.readline(), sep=" ")
        y = np.fromstring(stdin.readline(), sep=" ")
        z = np.fromstring(stdin.readline(), sep=" ")
        yield x,y,z


angle=0

def update(data):
    points._offsets3d = data
    x, y, z = data
    x_tail.append(np.r_[x, np.nan])
    y_tail.append(np.r_[y, np.nan])
    z_tail.append(np.r_[z, np.nan])

    if len(x_tail) > TAIL_LEN:
        x_tail.pop(0)
        y_tail.pop(0)
        z_tail.pop(0)

    segments = np.stack((np.array(x_tail).T,
                         np.array(y_tail).T,
                         np.array(z_tail).T), axis=-1)
    tails.set_segments(segments)


    # global angle
    # angle += 1.0
    # ax.view_init(30, angle)

    return points, tails


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
