import numpy as np
from math import sin, cos, pi, tan, sqrt
import os

import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D
# import matplotlib.animation as animation


degree = np.arange(0, 361, 1)
theta = [d/360.0*2*pi for d in degree]
r = []
for d in degree:
    # t stands for theta
    t = (d%60)/360*2*pi
    x = sqrt(3)/(tan(t)+sqrt(3))
    y = tan(t)*x
    r.append(sqrt(x**2+y**2))


ax1 = plt.subplot(111, projection='polar')
ax1.plot(theta, r)
plt.show()