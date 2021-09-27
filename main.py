from __future__ import print_function

import numpy as np
from math import sin, cos, pi
import os

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation

xXY = []
yXY = []
xShape = []
yShape = []
xHo = []
yHo = []
zHo = []

## Search for all shape X that pass x, y
x_p = 2
y_p = 3

n_sample = int(360/15+1)
layers = 5

def funcCircle(rIn = 1):
    ## sample every 1 degree
    theta = np.arange(0, 361, 1)
    #r = r*np.ones(len(theta))
    r = np.zeros(len(theta))
    for i in range(len(theta)):
        if i < 180:
            r[i] = rIn + rIn*i/120.0
        elif i > 360:
            r[i] = rIn + rIn*(i-360)/120.0
        else:
            r[i] = rIn + rIn*(360-i)/120.0
    return [r, theta]

def findShape(x, y, theta, inR):
    ## find origin
    ## x, y is the point that this shape passes
    ## theta is the angle
    ## inR is the

    theta_rad = theta/360.0*(2*pi)

    x_o = x - inR[theta] * cos(theta_rad)
    y_o = y - inR[theta] * sin(theta_rad)

    outShape_x = np.zeros(len(inR))
    outShape_y = np.zeros(len(inR))
    for i in range(361):
        i_rad = i/360.0*(2*pi)
        outShape_x[i] = x_o + inR[i] * cos(i_rad)
        outShape_y[i] = y_o + inR[i] * sin(i_rad)
    return [x_o, y_o], [outShape_x, outShape_y]

# initialization function: plot the background of each frame
#def init():
#    pointCenter.set_data([], [])
#    pointCurrent.set_data([], [])
#    lineCentOut.set_data([], [])
#    for i in range(len(lineXY)):
#        lineXY[i].set_data([], [])
#
#    #line2.set_xdata([])
#    #line2.set_ydata([])
#    #line2.set_3d_properties([])
#    return lineXY#line1, line2, pointCenter

# animation function.  This is called sequentially
def animate(i):
    ## For 2D image (Euclid space)
    start = int(i/n_sample)*n_sample
    xline = np.array(xXY[start:i+1])
    yline = np.array(yXY[start:i+1])
    lineCentOut.set_data(xline, yline)

    pointCenter.set_data(xXY[start:i+1], yXY[start:i+1])
    pointCurrent.set_data(xXY[i],yXY[i])

    #change the blit param to False if you want to keep previous shape.
    if i > 0:
        lineXY[i-1].set_alpha(0.1)
    lineXY[i].set_data(xShape[i], yShape[i])
    lineXY[i].set_alpha(0.5)

    h = int(i/n_sample)
    z = np.ones(len(xline))*h
    lineHough[h].set_xdata(xline)
    lineHough[h].set_ydata(yline)
    lineHough[h].set_3d_properties(z)

    x = np.array(xline)
    y = np.array(yline)
    x, y = np.meshgrid(x,y)

    #ax2.plot_surface(x, y, zarray[:, :, frame_number], cmap="magma")

    return pointCenter, lineCentOut, lineHough, lineXY[i]

if __name__=='__main__':
    fig = plt.figure(figsize=plt.figaspect(.5))

    fig.suptitle('Generalized Hough Transform')
    ax1 = fig.add_subplot(1, 2, 1)
    ax1.grid(True)
    ax1.set_ylabel('Original space')
    ax1.set_xlim(-15,20)
    ax1.set_ylim(-15,20)
    pointPass = ax1.plot(x_p, y_p, 'r+', markersize=7)
    ## line up those center points with share the same r
    lineCentOut, = ax1.plot([], [], lw=1, alpha=1)
    # ## cooresponding shape outline of the center
    # print(n_sample)
    lineXY = [ax1.plot([], [], lw=1, alpha=0.5, color='g')[0] for i in range(n_sample*(layers+1))]

    ## the given point (all shapes pass through this point)
    pointCurrent = ax1.plot([], [], 'b+',markersize=7)[0]
    pointCenter = ax1.plot([], [], 'bo', markersize=0.5)[0]

    ax2 = fig.add_subplot(1, 2, 2, projection='3d')
    ax2.set_xlim(-10,10)
    ax2.set_ylim(-10,10)
    ax2.set_zlim(0,10)
    lineHough = [ax2.plot([], [], [], lw=1, alpha=0.8)[0] for i in range(layers)]
    X = np.array([])
    Y = np.array([])
    X, Y = np.meshgrid(X, Y)
    Z = X + Y
    surface = ax2.plot_surface(X, Y, Z, lw=0, antialiased=True)

    xXY = []
    yXY = []
    samples = [int(t*360/(n_sample-1)) for t in range(n_sample-1)]
    samples.append(360)
    for i in range(1, layers):
        ## generate r-theta relationship basing on given function
        [outline, theta] = funcCircle(i)
        for j in range(n_sample):
            origin, outShape = findShape(x_p, y_p, samples[j], outline)
            print(j)
            xXY.append(origin[0])
            yXY.append(origin[1])
            xShape.append(outShape[0])
            yShape.append(outShape[1])

    ## call the animator.  blit=True means only re-draw the parts that have changed.
    anim = animation.FuncAnimation(fig, animate, #init_func=init,
                               frames=n_sample*(layers-1), interval=200, blit=False, repeat=False)

    gif = False
    if gif == True:
        anim.save('hough.gif', dpi=80, writer='imagemagick')

    ## save the animation as an mp4.  This requires ffmpeg or mencoder to be
    ## installed.  The extra_args ensure that the x264 codec is used, so that
    ## the video can be embedded in html5.  You may need to adjust this for
    ## your system: for more information, see
    ## http://matplotlib.sourceforge.net/api/animation_api.html
    #anim.save('basic_animation.mp4', fps=30, extra_args=['-vcodec', 'libx264'])

    plt.show()
