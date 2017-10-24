import pandas as pd
import numpy as np
import os
import time

import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse


def read_csv(path, col=['x', 'y']):
    array = []
    frame = pd.read_csv(path, header=0, sep=';', decimal=",")
    for i, title in enumerate(col):
        cell = frame[title].values

        try:
            cell = cell[~np.isnan(cell)]
        except Exception as ex:
            print(ex)
            for j, c in enumerate(cell):
                try:
                    np.float(c.replace(',', '.'))
                except:
                    print('Error in row:%s "%s"' % (j, c))

        array.append(cell)
    return np.array(array)




def draw_ellipce(ellipses, data, elength):
    #fig = plt.figure(0)
    #ax = fig.add_subplot(111, aspect='equal')
    plt.clf()
    figManager = plt.get_current_fig_manager()
    figManager.window.showMaximized()
    ax = plt.gca()

    ax.scatter(data[:, 0], data[:, 1], color='k', zorder=2, s=1, alpha=0.4, lw=0)

    for i, elli in enumerate(ellipses):
        e = Ellipse(xy=[elli[0], elli[1]], width=elength[0], height=elength[1],
                    angle=1*elli[3], alpha=0.3)
        ax.add_artist(e)
        e.set_clip_box(ax.bbox)
        e.set_facecolor('r')
        e.set_edgecolor('k')

    plt.grid(True)
    plt.savefig(os.path.expanduser('~' + os.getenv("USER") + '/Documents/workspace/') +
                'result/test/' + str(int(time.time() * 1000) )+ '.png', dpi=700)
    plt.show()


ellipses = read_csv('/home/ivan/Documents/workspace/result/test/calif_01.csv', ['x', 'y', 'P', 'angles']).T
data = read_csv('/home/ivan/Documents/workspace/resources/csv/GEO/calif/calif_dps.csv').T

ellipses = ellipses[np.where(ellipses[:, 2] > 0.2)]

draw_ellipce(ellipses, data, [0.7, 0.2])


