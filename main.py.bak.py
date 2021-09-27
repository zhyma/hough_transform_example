from __future__ import print_function

import numpy as np
from math import sin, cos, pi
import os

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation

xEu = []
yEu = []
xHo = []
yHo = []
zHo = []

## Search for all shape X that pass x, y
x_p = 2
y_p = 3

def funcCircle(r = 10):
    theta = np.arange(0, 360, 5)
    r = r*np.ones(len(theta))
    return [r, theta]
    #x = np.zeros(len(theta))
    #y = np.zeros(len(theta))
    #for i in range(len(theta)):
    #    x[i] = r * cos(theta[i]/(2*pi))
    #    y[i] = r * sin(theta[i]/(2*pi))
    #return x, y

def findShape(x, y, theta, inShape):
    ## find origin
    x_o = x - inShape[int(theta/5)] * cos(theta/(2*pi))
    y_o = y - inShape[int(theta/5)] * sin(theta/(2*pi))

    outShape_x = np.zeros(len(inShape))
    outShape_y = np.zeros(len(inShape))
    for i in range(len(inShape)):
        outShape_x = x_o + inShape[int(theta/5)] * cos(theta/(2*pi))
        outShape_y = y_o + inShape[int(theta/5)] * sin(theta/(2*pi))
    return [x_o, y_o], [outShape_x, outShape_y]

# initialization function: plot the background of each frame
def init():
    #point1.set_data(x_p, y_p)
    line1.set_data([], [])
    #point1.set_data([])
    line2.set_xdata([])
    line2.set_ydata([])
    line2.set_3d_properties([])
    return line1, line2

# animation function.  This is called sequentially
def animate(i):
    ## For 2D image (Euclid space)
    xline = np.array(xEu[0:i])
    yline = np.array(yEu[0:i])
    line1.set_data(xline,yline)
    line2.set_xdata(xline)
    line2.set_ydata(yline)
    line2.set_3d_properties(np.ones(len(xline)))

    #point1.set_data(0,0)
    return line1, line2

if __name__=='__main__':
    fig = plt.figure(figsize=plt.figaspect(.5))

    fig.suptitle('A tale of 2 subplots')
    ax1 = fig.add_subplot(1, 2, 1)
    ax1.grid(True)
    ax1.set_ylabel('Original space')
    ax1.set_xlim(-5,5)
    ax1.set_ylim(-5,5)
    line1, = ax1.plot([], [], lw=2, alpha=1)
    point1 = ax1.scatter(x_p, y_p, s=5)

    ax2 = fig.add_subplot(1, 2, 2, projection='3d')
    ax2.set_xlim(-10,10)
    ax2.set_ylim(-10,10)
    ax2.set_zlim(0,10)
    line2, = ax2.plot([], [], [], lw=2)

    ## generate r-theta relationship basing on given function
    [r, theta] = funcCircle(r = 1)
    print(len(theta))
    xEu = []
    yEu = []
    for i in range(len(theta)):
        origin, outShape = findShape(x_p, y_p, theta[i], r)
        xEu.append(origin[0])
        yEu.append(origin[1])

    ## call the animator.  blit=True means only re-draw the parts that have changed.
    anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=10, interval=200, blit=True)

    ## save the animation as an mp4.  This requires ffmpeg or mencoder to be
    ## installed.  The extra_args ensure that the x264 codec is used, so that
    ## the video can be embedded in html5.  You may need to adjust this for
    ## your system: for more information, see
    ## http://matplotlib.sourceforge.net/api/animation_api.html
    #anim.save('basic_animation.mp4', fps=30, extra_args=['-vcodec', 'libx264'])

    plt.show()
