import numpy as np
import os
import time
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse


def draw_ellipce(ellipses, angles, data):
    #fig = plt.figure(0)
    #ax = fig.add_subplot(111, aspect='equal')
    plt.clf()
    figManager = plt.get_current_fig_manager()
    figManager.window.showMaximized()
    ax = plt.gca()

    ax.scatter(data[:, 0], data[:, 1], color='k', zorder=2, s=1, alpha=0.4, lw=0)

    for i, elli in enumerate(ellipses):
        e = Ellipse(xy=[elli[0], elli[1]], width=2*elli[2], height=2*elli[3],
                    angle=1*angles[i], alpha=0.3)
        ax.add_artist(e)
        e.set_clip_box(ax.bbox)
        e.set_facecolor('r')
        e.set_edgecolor('k')

    plt.grid(True)
    plt.savefig(os.path.expanduser('~' + os.getenv("USER") + '/Documents/workspace/') +
                'result/test/' + str(int(time.time() * 1000) )+ '.png', dpi=700)
    plt.show()