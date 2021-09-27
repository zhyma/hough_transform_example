import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation

def update_plot(frame_number, zarray, plot):
    plot[0].remove()
    plot[0] = ax.plot_surface(x, y, zarray[:,:,frame_number], cmap="magma")

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

N = 14
nmax=20
x = np.linspace(-4,4,N+1)
x, y = np.meshgrid(x, x)
zarray = np.zeros((N+1, N+1, nmax))

f = lambda x,y,sig : 1/np.sqrt(sig)*np.exp(-(x**2+y**2)/sig**2)

for i in range(nmax):
    zarray[:,:,i] = f(x,y,1.5+np.sin(i*2*np.pi/nmax))
z = zarray[:,:,0]
plot = ax.plot_surface(x, y, z, color='0.75', rstride=1, cstride=1)
ax.set_zlim(0,1.5)
print(len(x), len(y),len(z))
print(len(x[0]))
print(len(x[0,0]))
#animate = animation.FuncAnimation(fig, update_plot, nmax, fargs=(zarray, plot))
plt.show()