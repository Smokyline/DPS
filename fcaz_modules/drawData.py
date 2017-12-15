import os
import numpy as np
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import Polygon as mlpPolygon
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Circle
from matplotlib.patches import RegularPolygon
from matplotlib.patches import RegularPolygon
import matplotlib.patches as patches
import matplotlib.image as mpimg
from scipy.misc import imread
import matplotlib.cbook as cbook

from itertools import cycle
cycol = cycle('bgrcmk')


import math
#from PIL import Image


def get_border_coord():
    # coord = [40, 52, 37, 45] #kvz
    # coord = [84, 102, 45, 56] #altai
    #coord = [75, 105, 45, 55]  # altai
    #coord = [95, 125, 46, 61] # baikal
    coord = [154, 168, 48, 57] #kmch
    #coord = [-84, -64, -46, 6]

    return coord



def visual_FCAZ(X, A_DPS, EXT, eqs, eqs_labels, title, path=None):
    fig = plt.figure(figsize=(16, 12))
    ax = fig.add_subplot(111)

    cd = get_border_coord()
    m = Basemap(llcrnrlat=cd[2], urcrnrlat=cd[3],
                llcrnrlon=cd[0], urcrnrlon=cd[1],
                resolution='l')
    m.drawcountries(zorder=1, linewidth=1)
    m.arcgisimage(service='World_Shaded_Relief', xpixels=1500, verbose=True, zorder=0)

    parallels = np.arange(-90., 90, 2)
    m.drawparallels(parallels, labels=[1, 1, 0, 0], zorder=1, linewidth=0.5, alpha=0.8)
    meridians = np.arange(0., 360, 2)
    m.drawmeridians(meridians, labels=[0, 0, 0, 1], zorder=1, linewidth=0.5, alpha=0.8)


    ax.scatter(X[:, 0], X[:, 1], c='k', marker='.', s=45, linewidths=0.0, label='X')

    if EXT is not None:
        ax.scatter(EXT[:, 0], EXT[:, 1], c='#fd41cd', marker='s', s=140, linewidths=0.0, label='e2xt')
    ax.scatter(A_DPS[:, 0], A_DPS[:, 1], c='g', marker='.', s=75, linewidths=0.1, label='DPS')

    if eqs is not None:
        clr = ['c', 'b', 'y', 'r', '#533126', '#c0c0c0']

        c_rad = [0.14, 0.17, 0.20, 0.24, 0.28, 0.33]

        for col, eq in enumerate(eqs):
            for x, y, r in zip(eq[:, 0], eq[:, 1], [c_rad[col] for i in range(len(eq))]):

                circleA = ax.add_artist(Circle(xy=(x, y),
                                                   radius=r, alpha=1, linewidth=4, zorder=4,
                                                   edgecolor=clr[col], facecolor='none', label=eqs_labels[col]))
                ax.scatter(x, y, marker='x', color='k', alpha=0.75)

            plt.scatter([], [], c=clr[col], marker='o', s=50, linewidths=0.5, label=eqs_labels[col],
                            zorder=4)

    plt.grid(True)
    plt.title(title)
    plt.legend(loc=8, bbox_to_anchor=(0.5, -0.15), ncol=4)
    plt.savefig(path+title+'.png', dpi=500)
    plt.close()



def visual_SFCAZ(X, DPS_set, EXT, eqs, eqs_labels, title, path=None):
    fig = plt.figure(figsize=(16, 12))
    ax = fig.add_subplot(111)

    cd = get_border_coord()
    m = Basemap(llcrnrlat=cd[2], urcrnrlat=cd[3],
                llcrnrlon=cd[0], urcrnrlon=cd[1],
                resolution='l')
    m.drawcountries(zorder=1, linewidth=1)
    m.arcgisimage(service='World_Shaded_Relief', xpixels=1500, verbose=True, zorder=0)

    parallels = np.arange(-90., 90, 2)
    m.drawparallels(parallels, labels=[1, 1, 0, 0], zorder=1, linewidth=0.5, alpha=0.8)
    meridians = np.arange(0., 360, 2)
    m.drawmeridians(meridians, labels=[0, 0, 0, 1], zorder=1, linewidth=0.5, alpha=0.8)

    ax.scatter(X[:, 0], X[:, 1], c='k', marker='x', s=25, linewidths=0.0, label='X', alpha=0.75)
    ax.scatter(EXT[:, 0], EXT[:, 1], c='#fd41cd', marker='s', s=140, linewidths=0.0, label='e2xt')
    for j, color in enumerate(['g', '#c5e72b', 'w']):
        ax.scatter(DPS_set[j][:, 0], DPS_set[j][:, 1], c=color, marker='.', s=90, linewidths=0.1, label='DPS')

    if eqs is not None:
        clr = ['c', 'b', 'y', 'r', '#533126', '#c0c0c0']

        c_rad = [0.14, 0.17, 0.20, 0.24, 0.28, 0.33]
        #TODO цвета

        for col, eq in enumerate(eqs):
            for x, y, r in zip(eq[:, 0], eq[:, 1], [c_rad[col] for i in range(len(eq))]):
                circleA = ax.add_artist(Circle(xy=(x, y),
                                                   radius=r, alpha=1, linewidth=4, zorder=4,
                                                   edgecolor=clr[col], facecolor='none', label=eqs_labels[col]))
                ax.scatter(x, y, marker='x', color='k', alpha=0.75)

            plt.scatter([], [], c=clr[col], marker='o', s=50, linewidths=0.5, label=eqs_labels[col],
                            zorder=4)
    """
    import pandas as pd
    nodes_X = np.array(
        pd.read_csv('/home/ivan/Documents/workspace/resources/csv/GEO/kmch/kmch_nodes.csv', delimiter=';', header=0,
                    decimal=','))
    nodes_B = np.array(
        pd.read_csv('/home/ivan/Documents/workspace/resources/csv/GEO/kmch/kmch_nodes_B.csv', delimiter=';', header=0,
                    decimal=','))
    for x, y, r in zip(nodes_B[:, 0], nodes_B[:, 1], [0.67 for i in range(len(nodes_B))]):
            m.tissot(x, y, r, 50, alpha=0.9, linewidth=5, zorder=4, linestyle='dashed',
                     facecolor='none', edgecolor="#800080")

    ax.scatter(nodes_X[:, 0], nodes_X[:, 1], marker='o', color='y', alpha=0.75, s=150)
    """

    plt.grid(True)
    plt.title(title)
    plt.legend(loc=8, bbox_to_anchor=(0.5, -0.15), ncol=4)
    plt.savefig(path+title+'.png', dpi=500)
    plt.close()


def visual_dpsB_iter(clusters, fdata, xdata, title, disp=False, direc=None):
    fig = plt.figure(figsize=(16, 12))
    ax = fig.add_subplot(111)

    plt.scatter(fdata[:, 0], fdata[:, 1], c='k', marker='.', s=10, linewidths=0)
    plt.scatter(clusters[:, 0], clusters[:, 1], c='r', marker='.', s=19, linewidths=0)
    if xdata is not None:
        plt.scatter(xdata[:, 0], xdata[:, 1], c='g', marker='.', s=8, linewidths=0)

    # eq = read_csv('/Users/Ivan/Documents/workspace/resourses/csv/GEO/kvz/kvz_nEQ.csv').T
    # plt.scatter(eq[:, 0], eq[:, 1], c='b', marker='^', s=17, linewidths=0.1)
    plt.grid(True)
    plt.title(title)
    if direc is None:
        plt.savefig(os.path.expanduser('~' + os.getenv("USER") + '/Documents/workspace/')+
                    'result/test/' + title + '.png', dpi=400)

    else:
        plt.savefig(direc + '.png', dpi=500)
    if disp == True:
        plt.show()
    plt.close(fig)


def visual_MC_dataPoly(dps, B, ext, eq, xyPoly, title, direct):
    poly = mlpPolygon(xyPoly, fc='none', ec='b', alpha=0.6, linewidth=2)
    fig = plt.figure(figsize=(16, 12))
    ax = fig.add_subplot(111)
    cd = get_border_coord()
    plt.xlim(cd[0], cd[1])
    plt.ylim(cd[2], cd[3])


    if B is not None:
        plt.scatter(B[:, 0], B[:, 1], c='k', marker='.', s=9, alpha=0.3, linewidths=0)

    plt.scatter(ext[:, 0], ext[:, 1], c='#fd41cd', marker='s', s=110, linewidths=0.0, label='e2xt')

    plt.scatter(dps[:, 0], dps[:, 1], c='g', marker='.', s=15, linewidths=0)
    plt.scatter(eq[:, 0], eq[:, 1], c='r',  marker='o', s=350, linewidths=0.5)# eq square

    plt.gca().add_patch(poly)
    plt.grid(True)
    plt.title(title)

    if direct is None:
        plt.savefig(os.path.expanduser('~' + os.getenv("USER") + '/Documents/workspace/')+
                    'result/test/' + title + '.png', dpi=400)

    else:
        plt.savefig(direct+'MonteCarlo_'+title+'.png', dpi=500)

    plt.close()


def check_pix_ext(A, pols, real_size=False):
    fig = plt.figure(figsize=(16, 12))
    ax = fig.add_subplot(111)


    cd = get_border_coord()
    plt.xlim(cd[0], cd[1])
    plt.ylim(cd[2], cd[3])

    ax.add_patch(patches.Polygon(pols, color='#008000'))

    if real_size:
        delta = (np.sqrt(2) * 0.05 / 2)
        for xy in A:
            ax.add_artist(RegularPolygon(xy=(xy[0], xy[1]), numVertices=4, radius=delta, orientation=math.pi / 4, lw=0,
                                         color='r', label='e2xt'))
    else:
        plt.scatter(A[:, 0], A[:, 1], c='#ff0000', marker='s', s=110, linewidths=0.0, alpha=1, zorder=2)

    fig.canvas.draw()

    reso = fig.canvas.get_width_height()
    data = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8, sep='')
    data = data.reshape((reso[0] * reso[1], 3))

    idx_green_array1 = np.where(data[:, 1] == 128)[0]
    green_array = data[np.where(data[idx_green_array1, 2] == 0)]

    idx_red_array1 = np.where(data[:, 0] == 255)[0]
    red_array = data[np.where(data[idx_red_array1, 1] == 0)]

    r = len(red_array)
    f = len(green_array) + r
    plt.close()
    return round(r * 100 / f, 1)

