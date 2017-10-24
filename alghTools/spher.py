import matplotlib
import numpy as np

from alghTools.tools import read_csv

matplotlib.use('Qt4Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import math



def create_3d_map(data, title):
    ax = Axes3D(plt.figure())
    x, y, z = data[:, 0], data[:, 1], data[:, 2]



    #xi = np.linspace(x.min(), x.max(), 50)
    #yi = np.linspace(y.min(), y.max(), 50)
    #zi = griddata((x, y), z, (xi[None, :], yi[:, None]), method='nearest')  # create a uniform spaced grid
    #xig, yig = np.meshgrid(xi, yi)
    #surf = ax.plot_wireframe(X=xig, Y=yig, Z=zi, rstride=1, cstride=1, linewidth=1)  # 3d plot
    #surf = ax.contourf(xig, yig, zi, zdir='z', cmap=cm.coolwarm)
    ax.scatter(x, y, z, marker='.')
    #surf = ax.scatter(xig, yig, zi, marker='.', linewidth=0)
    #surf = ax.contourf(xig, yig, zi, zdir='z', cmap=cm.Spectral)
    #surf = ax.contourf(xig, yig, zi, zdir='z', cmap=cm.cool)
    #surf = ax.plot_surface(X=xig, Y=yig, Z=zi, rstride=1, cstride=1, linewidth=1, cmap=cm.coolwarm)  # 3d plot



    plt.grid(True)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.title(title)
    #plt.savefig('/Users/Ivan/Documents/workspace/result/sk/kvz_' + title + '.png', dpi=400)
    print('done')

    plt.show()

def create_2d_map(data):
    x = data[:, 0]
    y = data[:, 1]
    plt.scatter(x, y, marker='.', linewidths=0.0)
    plt.show()

def toDesc(data):
    """
    x = r * sin(y) * cos(x)
    y = r * sin(y) * sin(x)
    z = r * cos(y)
    """
    r = 6371
    desc_data = np.empty((0, 3))
    for i in data:
        x, y = math.radians(i[0]), math.radians(i[1])
        #x, y = i[0]*math.pi/180, i[1]*math.pi/180

        xyz = []
        xyz.append(r * math.sin(y) * math.cos(x))
        xyz.append(r * math.sin(y) * math.sin(x))
        xyz.append(r * math.cos(y))



        xyz = np.array(xyz).reshape((1, 3))
        desc_data = np.append(desc_data, xyz, axis=0)
    return desc_data


data = read_csv('//Users/Ivan/Documents/workspace/resources/csv/GEO/kvz/kvz_dps.csv').T
#data = read_csv('//Users/Ivan/Documents/workspace/resources/csv/samer.csv').T

desc_data = toDesc(data)
#create_2d_map(desc_data)
#create_2d_map(data)
create_3d_map(desc_data, 'samer')