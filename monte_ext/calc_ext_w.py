import numpy as np
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from fcaz_modules.drawData import get_border_coord
import codecs





def calcW_pix_ext(ext_data, eq_data, xy_Poly, dot_size = 200):


    fig, ax = plt.subplots(figsize=(12, 12))


    plt.axis('off')


    cd = get_border_coord()
    plt.xlim(cd[0], cd[1])
    plt.ylim(cd[2], cd[3])
    center_x, center_y = np.mean(xy_Poly[:, 0]), np.mean(xy_Poly[:, 1])

    def calc_len_pix():
        fig.canvas.draw()
        reso = fig.canvas.get_width_height()

        data = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8, sep='')
        data = data.reshape((reso[0] * reso[1], 3))

        #idx_green_array1 = np.where(data[:, 1] == 128)[0]
        #green_array = data[np.where(data[idx_green_array1, 2] == 0)]

        idx_red_array1 = np.where(data[:, 0] == 255)[0]
        red_array = data[np.where(data[idx_red_array1, 1] == 0)]

        return len(red_array)


    #ax.add_patch(patches.Polygon(pols, color='#008000', zorder=0))

    test_dot = ax.scatter(center_x, center_y, marker='o', c='#ff0000', lw=0, s=dot_size, zorder=2)
    one_dot_leng = calc_len_pix()
    test_dot.set_visible(False)

    ax.scatter(ext_data[:, 0], ext_data[:, 1], c='#ff0000', marker='s', s=100, linewidths=0.0, alpha=1, zorder=1)
    zero_r = calc_len_pix()

    w = 0
    acc_points = 0
    miss_points = 0

    for i, xy in enumerate(eq_data):
        r = ax.scatter(xy[0], xy[1], marker='o', c='#ff0000', lw=0, s=dot_size, zorder=2)
        a_r = calc_len_pix()

        if np.abs(zero_r - a_r) < one_dot_leng:
            acc_points += 1
            w += 1
        else:
            #plt.savefig('/home/ivan/Documents/workspace/result/tmp/' + 'figD' +str(i+1)+ '.png', dpi=100)
            miss_points += 1
        r.set_visible(False)

    plt.close()
    return w / len(eq_data), acc_points, miss_points



