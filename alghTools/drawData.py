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

import math
from PIL import Image


def visual_data(clusterA, dataX, title='', display_plot=False, direc=None, eqs=None, baseM=False, labels=[''], diff_data=False, ext=False,
                poly_field=False, real_ext_size=False):
    #fig, ax = plt.subplots()
    #fig = plt.figure()
    plt.clf()
    figManager = plt.get_current_fig_manager()
    figManager.window.showMaximized()
    ax = plt.gca()

    if baseM:
        #xplt = np.arange(baseM[0], baseM[1] + 1, 2)
        #yplt = np.arange(baseM[2], baseM[3] + 1, 1)
        m_r = baseM
        m = Basemap(llcrnrlat=m_r[2], urcrnrlat=m_r[3],
                    llcrnrlon=m_r[0], urcrnrlon=m_r[1],
                    resolution='l')
        m.drawcountries(zorder=1, linewidth=1)
        #m.drawcoastlines(zorder=1, linewidth=0.25)
        parallels = np.arange(0., 90, 1)
        m.drawparallels(parallels, labels=[1, 1, 0, 0], zorder=1, linewidth=0.5, alpha=0.8)
        meridians = np.arange(0., 360, 1)
        m.drawmeridians(meridians, labels=[0, 0, 0, 1], zorder=1, linewidth=0.5, alpha=0.8)
    else:
        xplt = np.arange(min(dataX[:, 0]), max(dataX[:, 0]) + 1, 2)
        yplt = np.arange(min(dataX[:, 1]), max(dataX[:, 1]) + 1, 1)

    #plt.xticks(xplt, [str(x) + u'\N{DEGREE SIGN}' for x in xplt])
    #plt.yticks(yplt, [str(y) + u'\N{DEGREE SIGN}' for y in yplt])

    if poly_field is not False:
        ax.add_patch(patches.Polygon(poly_field, edgecolor='b', facecolor='none', alpha=0.9, lw=1.5, zorder=1))

    plt.scatter(dataX[:, 0], dataX[:, 1], c='k', marker='.', s=40, linewidths=0, alpha=0.6, label='AltaiSayan M2.8+', zorder=1)

    if ext is not False:
        # #64ffff cyan
        if real_ext_size:
            delta = (np.sqrt(2)*0.05/2)
            for xy in ext:

                ax.add_artist(RegularPolygon(xy=(xy[0], xy[1]), numVertices=4, radius=delta, orientation=math.pi/4, lw=0,
                                             color='r', label='e2xt'))
        else:
            plt.scatter(ext[:, 0], ext[:, 1], c='r', marker='s', s=120, linewidths=0.0, alpha=1, label='e2xt')
        #

    if diff_data is not False:
        plt.scatter(clusterA[:, 0], clusterA[:, 1], c='g', marker='.', s=160, linewidths=0.1, label='DPS unique', zorder=2)
        plt.scatter(diff_data[0][:, 0], diff_data[0][:, 1], c='c', marker='.', s=160, linewidths=0.1, label='DPS 1', zorder=3)
        plt.scatter(diff_data[1][:, 0], diff_data[1][:, 1], c='m', marker='.', s=160, linewidths=0.1, label='DPS 2', zorder=3)
    else:
        plt.scatter(clusterA[:, 0], clusterA[:, 1], c='g', marker='.', s=160, linewidths=0.1, label='DPS clust', zorder=2)

    if eqs is not None:
        col_array = ['b', '#d8d800', 'm']
        for col, eq in enumerate(eqs):
            #plt.scatter(eq[:, 0], eq[:, 1], edgecolors=col_array[col], marker='*', s=50, linewidths=0.5, facecolor="none")
            for x, y, r in zip(eq[:, 0], eq[:, 1], [0.24 for i in range(len(eq))]):
                if col == 0:
                    squareA = ax.add_artist(
                        RegularPolygon((x, y), 4, r, alpha=0.8, linewidth=2, zorder=4, facecolor='none',
                                       edgecolor=col_array[col], label=labels[col]))


                else:
                    circleA = ax.add_artist(Circle(xy=(x, y),
                                                   radius=r, alpha=0.8, linewidth=2, zorder=4, facecolor='none',
                                                   edgecolor=col_array[col], label=labels[col]))

            """if col == 0:
                plt.scatter(eq[:, 0], eq[:, 1], c=col_array[col], marker='s', s=50, linewidths=0.3, label=labels[col],
                            zorder=4)
            else:
                plt.scatter(eq[:, 0], eq[:, 1], c=col_array[col], marker='o', s=50, linewidths=0.5, label=labels[col],
                            zorder=4)
"""

    plt.grid(True)
    plt.title(title)
    #plt.legend(loc=8, bbox_to_anchor=(0.5, -0.19), ncol=4) #altai
    plt.legend(loc=8, bbox_to_anchor=(0.5, -0.10), ncol=4)  # baikal
    if direc is None:
        plt.savefig('/Users/Ivan/Documents/workspace/result/' + title + '.png', dpi=500)
    else:
        plt.savefig(direc + title + '.png', dpi=500)

    if display_plot == True:
        plt.show()
    plt.close()


def visual_dps_iter(clusters, fdata, xdata, title, disp=False, direc=None):
    fig = plt.figure()

    plt.scatter(fdata[:, 0], fdata[:, 1], c='k', marker='.', s=10, linewidths=0)
    plt.scatter(clusters[:, 0], clusters[:, 1], c='r', marker='.', s=19, linewidths=0)
    if xdata is not None:
        plt.scatter(xdata[:, 0], xdata[:, 1], c='g', marker='.', s=8, linewidths=0)

    # eq = read_csv('/Users/Ivan/Documents/workspace/resourses/csv/geop/kvz/kvz_nEQ.csv').T
    # plt.scatter(eq[:, 0], eq[:, 1], c='b', marker='^', s=17, linewidths=0.1)
    plt.grid(True)
    plt.title(title)
    if direc is None:
        plt.savefig('/Users/Ivan/Documents/workspace/result/' + title + '.png', dpi=500)
    else:
        plt.savefig(direc + '.png', dpi=500)
    if disp == True:
        plt.show()
    plt.close(fig)


def visual_ext(X, A_DPS, Z, title, path=None):
    fig, ax = plt.subplots()
    plt.gca().set_aspect('equal')

    try:
        plt.scatter(X[:, 0], X[:, 1], c='k', marker='.', s=10, linewidths=0, label='X')
    except:
        pass

    plt.scatter(Z[:, 0], Z[:, 1], c='r', marker='s', s=14, linewidths=0.0, label='e2xt')
    plt.scatter(A_DPS[:, 0], A_DPS[:, 1], c='g', marker='.', s=15, linewidths=0.1, label='DPS')

    plt.legend()
    plt.grid(True)
    plt.title(title)

    if path is None:
        plt.savefig('/Users/Ivan/Documents/workspace/result/'+title+'.png', dpi=500)
    else:
        plt.savefig(path+title+'.png', dpi=500)
    plt.close()

def visual_dataPoly(dps, B, eq, xyPoly, title, direct):
    poly = mlpPolygon(xyPoly, fc='none', ec='b', alpha=0.6, linewidth=2)
    plt.gca().set_aspect('equal', adjustable='box')
    if B is not None:
        plt.scatter(B[:, 0], B[:, 1], c='k', marker='.', s=9, alpha=0.3, linewidths=0)
    plt.scatter(dps[:, 0], dps[:, 1], c='g', marker='.', s=15, linewidths=0)
    plt.scatter(eq[:, 0], eq[:, 1], c='r',  marker='o', s=30, linewidths=0.5)

    plt.gca().add_patch(poly)
    plt.grid(True)
    plt.title(title)

    if direct is None:
        plt.savefig('/Users/Ivan/Documents/workspace/result/MonteCarlo_'+title+'.png',  dpi=500)
    else:
        plt.savefig(direct+'MonteCarlo_'+title+'.png', dpi=500)

    plt.close()

def visual_MontePlot(data_real, data_rand, title, versions, directory):
    plt.clf()
    figManager = plt.get_current_fig_manager()
    figManager.window.showMaximized()
    ax = plt.gca()

    #plt.yticks(np.arange(0, 120, 10))
    #plt.xticks(np.arange(0, 100, 10))

    colors = ['r', 'b']
    for c, r in enumerate(data_real):
        ax.plot([i*100 for i in r], c=colors[c], linestyle='--', zorder=1, markersize=20, label=versions[c])

    for c, r in enumerate(data_rand):
        ax.plot([i*100 for i in r], c=colors[c], linestyle='-', zorder=2, markersize=15)

    plt.xlabel('iteration')
    plt.ylabel('%')
    plt.grid(True)
    plt.legend()
    #plt.title(title)

    plt.savefig(directory + 'MCplot.png', dpi=400)


def check_pix_ext(A, cd, pols, real_size=False):
    fig = plt.figure()

    figManager = plt.get_current_fig_manager()
    figManager.window.showMaximized()
    ax = plt.gca()


    plt.xlim(cd[0], cd[1])
    plt.ylim(cd[2], cd[3])

    ax.add_patch(patches.Polygon(pols, color='#008000'))

    if real_size:
        delta = (np.sqrt(2) * 0.05 / 2)
        for xy in A:
            ax.add_artist(RegularPolygon(xy=(xy[0], xy[1]), numVertices=4, radius=delta, orientation=math.pi / 4, lw=0,
                                         color='r', label='e2xt'))
    else:
        plt.scatter(A[:, 0], A[:, 1], c='#ff0000', marker='s', s=120, linewidths=0.0, alpha=1, zorder=2)

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

