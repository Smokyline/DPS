

import numpy as np
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt


data = np.random.rand(10, 2)

plt.clf()
figManager = plt.get_current_fig_manager()
figManager.window.showMaximized()
ax = plt.gca()

for X,Y in data:
    ax.scatter(X, Y, c=next(cycol))

plt.show()