from alghTools.tools import read_csv
from shapely.geometry import Polygon, Point
import numpy as np
import os
import numpy as np
import math


import matplotlib

matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Circle
from matplotlib.patches import RegularPolygon
import matplotlib.patches as patches

from PIL import Image
# from skimage.color import rgb2gray
from  scipy.misc import imsave




def calc_acc_pixpoly(B, eq_data, delta):
    """расчет точности алгоритма по пикселям"""
    fig = plt.figure()

    #figManager = plt.get_current_fig_manager()
    #figManager.window.showMaximized()
    ax = plt.gca()

    plt.axis('off')

    coord_field = [84, 101, 45, 53]
    plt.xlim(coord_field[0], coord_field[1])
    plt.ylim(coord_field[2], coord_field[3])
    center_x, center_y = np.mean(coord_field[:2]), np.mean(coord_field[2:])

    def calc_len_pix():
        fig.canvas.draw()
        reso = fig.canvas.get_width_height()

        data = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8, sep='')
        data = data.reshape((reso[0] * reso[1], 3))

        idx_red_array1 = np.where(data[:, 0] == 255)[0]
        red_array = data[np.where(data[idx_red_array1, 1] == 0)]

        return len(red_array)

    test_dot_size = 13  #70 standart
    test_dot = ax.scatter(center_x, center_y, marker='o', c='#ff0000', lw=0, s=test_dot_size, zorder=2)
    #test_dot = ax.scatter(center_x, center_y, marker='o', c='g', lw=0, s=13, zorder=2)
    #test_dot = ax.scatter(eq_coord[:, 0], eq_coord[:, 1], marker='o', c='g', lw=0, s=13, zorder=2)

    one_dot_leng = calc_len_pix()
    test_dot.set_visible(False)

    #for x, y, r in zip(B[:, 0], B[:, 1], [delta for i in range(len(B))]):
    #    ax.add_artist(RegularPolygon(xy=(x, y), numVertices=4, radius=0.14, orientation=math.pi / 4, lw=0,
    #                                 facecolor='#ff0000', edgecolor='#ff0000', zorder=1))

    ax.add_patch(patches.Polygon(pols_coords, edgecolor='#ff0000', facecolor='#ff0000', alpha=1, lw=0, zorder=1))

    #plt.savefig('/home/ivan/Documents/workspace/result/tmp/' + 'field.png', dpi=100)
    #plt.savefig('/home/ivan/Documents/workspace/result/tm/' + 'field.png', dpi=100)

    zero_r = calc_len_pix()
    w = 0
    acc_points = 0
    miss_points = 0

    for i, xy in enumerate(eq_data):
        r = ax.scatter(xy[0], xy[1], marker='o', c='#ff0000', lw=0, s=test_dot_size, zorder=2)
        a_r = calc_len_pix()
        if np.abs(zero_r - a_r) < one_dot_leng:
            acc_points += 1
            w += 1
        else:
            #plt.savefig('/home/ivan/Documents/workspace/result/tmp/' + str(i) + 'field.png', dpi=100)

            miss_points += 1
        r.set_visible(False)

    plt.close()
    return w / len(eq_data), acc_points, miss_points



workspace_path = os.path.expanduser('~' + os.getenv("USER") + '/Documents/workspace/')
eq_coord = read_csv(workspace_path+'resources/csv/GEO/altaiSay/altaiSay_3,5.csv').T
ext_coord = read_csv(workspace_path+'resources/csv/GEO/altaiSay/ext_dze.csv').T
pols_coords = [[84, 47], [84, 53], [101, 53], [101, 48.5], [91.5, 48.5], [91.5, 45.5], [89, 45.5], [89, 47]]

acc = calc_acc_pixpoly(ext_coord, eq_coord, 0.14)
print(acc)


