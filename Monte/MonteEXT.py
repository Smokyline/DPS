import numpy as np
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches




def calcW_pix_ext(ext_data, eq_data, coord_field, pols):
    fig = plt.figure()
    #ax = fig.add_subplot(111, aspect='equal')

    figManager = plt.get_current_fig_manager()
    figManager.window.showMaximized()
    ax = plt.gca()

    plt.axis('off')

    plt.xlim(coord_field[0], coord_field[1])
    plt.ylim(coord_field[2], coord_field[3])
    center_x, center_y = np.mean(coord_field[:2]), np.mean(coord_field[2:])

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

    test_dot = ax.scatter(center_x, center_y, marker='o', c='#ff0000', lw=0, s=70, zorder=2)
    one_dot_leng = calc_len_pix()
    test_dot.set_visible(False)

    ax.scatter(ext_data[:, 0], ext_data[:, 1], c='#ff0000', marker='s', s=100, linewidths=0.0, alpha=1, zorder=1)
    zero_r = calc_len_pix()

    w = 0
    acc_points = 0
    miss_points = 0

    for i, xy in enumerate(eq_data):
        r = ax.scatter(xy[0], xy[1], marker='o', c='#ff0000', lw=0, s=70, zorder=2)
        a_r = calc_len_pix()

        if np.abs(zero_r - a_r) < one_dot_leng:
            acc_points += 1
            w += 1
        else:
            #plt.savefig('/Users/Ivan/Documents/workspace/result/tmp/' + 'figD' +str(i+1)+ '.png', dpi=100)
            miss_points += 1
        r.set_visible(False)

    plt.close()
    return w / len(eq_data), acc_points, miss_points



