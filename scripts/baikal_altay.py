import numpy as np
import os
from alghTools.tools import read_csv
from alghTools.importData import ImportData

import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import RegularPolygon
from matplotlib.patches import Circle

workspace_path = os.path.expanduser('~' + os.getenv("USER") + '/Documents/workspace/')
res_path = workspace_path + 'result/baikal/baikalAltay/'
baikal_xy_full = read_csv(res_path + 'ext_baikal.csv').T
altay_xy_full = read_csv(res_path + 'ext_altay.csv').T

x_min = 95
x_max = 102

baikal_xy = baikal_xy_full[np.where(np.logical_and(baikal_xy_full[:, 0] >= 95, baikal_xy_full[:, 0] <= 102))]
altay_xy = altay_xy_full[np.where(np.logical_and(altay_xy_full[:, 0] >= 95, altay_xy_full[:, 0] <= 102))]
union_xy = np.append(baikal_xy, altay_xy, axis=0)

imp = ImportData(zone='baikal', main_mag='2,7', mag_array=['5,5', '5,75', '6'])
baikal_eqs, _ = imp.get_eq_stack()

imp = ImportData(zone='altaiSay', main_mag='', mag_array=['5,5'])
altay_eqs, _ = imp.get_eq_stack()



plt.clf()
figManager = plt.get_current_fig_manager()
figManager.window.showMaximized()
ax = plt.gca()

m = Basemap(llcrnrlat=np.min(union_xy[:, 1]-1), urcrnrlat=np.max(union_xy[:, 1]+1),
            llcrnrlon=np.min(union_xy[:, 0]-1), urcrnrlon=np.max(union_xy[:, 0]+1),
            resolution='l')
m.drawcountries(zorder=1, linewidth=1)
parallels = np.arange(0., 90, 1)
m.drawparallels(parallels, labels=[1, 1, 0, 0], zorder=1, linewidth=0.5, alpha=0.8)
meridians = np.arange(0., 360, 1)
m.drawmeridians(meridians, labels=[0, 0, 0, 1], zorder=1, linewidth=0.5, alpha=0.8)

r = 0.05
a = 0.45
for x, y, r in zip(altay_xy[:, 0], altay_xy[:, 1], [r for i in range(len(altay_xy))]):
    squareA = ax.add_artist(
                    RegularPolygon((x, y), 4, r, alpha=a, linewidth=0, zorder=4, facecolor='b',
                                   edgecolor='none'))

for x, y, r in zip(baikal_xy[:, 0], baikal_xy[:, 1], [r for i in range(len(baikal_xy))]):
    squareB = ax.add_artist(
            RegularPolygon((x, y), 4, r, alpha=a, linewidth=0, zorder=4, facecolor='r',
                           edgecolor='none'))

ax.scatter([], [], c='b', marker='s', lw=0, label='altaiSay ext2')
ax.scatter([], [], c='r', marker='s', lw=0, label='baikal ext2')

for xy in baikal_eqs:
    for x, y, r in zip(xy[:, 0], xy[:, 1], [0.17 for i in range(len(xy))]):
        #circleA = ax.add_artist(Circle(xy=(x, y), radius=r, alpha=0.7, linewidth=3, zorder=4, edgecolor='c', facecolor='none'))
        ax.add_artist(RegularPolygon(xy=(x, y), numVertices=3, radius=r, lw=3,
                                     edgecolor='c', facecolor='none', alpha=0.9, zorder=10))
for xy in altay_eqs:
    for x, y, r in zip(xy[:, 0], xy[:, 1], [0.17 for i in range(len(xy))]):
        ax.add_artist(RegularPolygon(xy=(x, y), numVertices=3, radius=r, lw=3,
                                     edgecolor='k', facecolor='none', alpha=0.8, zorder=10))

ax.scatter([], [], marker='s', c='c', s=70, label='baikal_eq5,5')
ax.scatter([], [], marker='s', c='k', s=70, label='altai_eq5,5')


plt.grid(True)
plt.legend()

plt.savefig(res_path + 'union' + '.png', dpi=450)
#plt.show()
plt.close()
