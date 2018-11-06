import os

import matplotlib

from main.dps_core import dps_clustering
from main.e2xt_core import E2XT
from main.tau_runner_mp import t_runner_mp
from fcaz_modules.tools import *

matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Circle




class SeismHist():
    def __init__(self):
        workspace_path = os.path.expanduser('~' + os.getenv("USER") + '/Documents/workspace/')
        region_name = 'kmch'
        res_dir = workspace_path + 'resources/csv/GEO/%s/' % (region_name)
        self.save_path = workspace_path+'result/DPS/%s/seism_hist/' % (region_name)
        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path, exist_ok=True)


        # x y year month day mag
        self.CATALOG = read_csv(res_dir + '%s_DPS_sh.csv' % region_name)
        self.EQ = read_csv(res_dir + '%s_m7_sh.csv' % region_name)

        #SFCAZ-DPS param beta, q
        self.dps_param = [[-0.3, -2],
                          [-0.2, -2]]
        self.sfcaz_epoch = 2

        #ext param
        self.omega = -4
        self.v = -2.25
        self.delta = 0.05




        self.border_coord = [154, 168, 48, 57]



    def sh_all_eqs(self):
        for eq_i, eq in enumerate(self.EQ):
            catalog_above = self.search_catalog_above(eq)

            dps, beta, q = self.calc_dps_clust(catalog_above[:, :2])
            ext = self.calc_ext(dps)

            eq_above = self.EQ[:eq_i, :2]
            eq_below = self.EQ[eq_i + 1:, :2]

            title = 'eq y_%i m_%i d_%i M_%.2f' % (eq[2], eq[3], eq[4], eq[5])
            self.visual_dps_clust(catalog_above[:, :2], dps, ext, eq_above, eq_below, eq, title)

    def sh_one_eqs_auto_beta(self, idx_eq, q):
        eq = self.EQ[idx_eq]
        catalog_above = self.search_catalog_above(eq)


        dps, beta, q = self.calc_dps_clust(catalog_above[:, :2], Q=q)
        ext = self.calc_ext(dps)

        eq_above = self.EQ[:idx_eq, :2]
        eq_below = self.EQ[idx_eq + 1:, :2]

        title = 'eq y_%i m_%i d_%i M_%.2f beta_%s q_%s' % (eq[2], eq[3], eq[4], eq[5], beta, q)
        self.visual_dps_clust(catalog_above[:, :2], dps, ext, eq_above, eq_below, eq, title)

    def search_catalog_above(self, eq):
        eq_x, eq_y, eq_year, eq_month, eq_day, eq_mag = eq
        catalog_above = self.CATALOG[np.where(np.logical_and(self.CATALOG[:, 2] <= eq_year,
                                                        self.CATALOG[:, 2] >= eq_year - 20))]
        del_idx_month = np.where(np.logical_and(catalog_above[:, 3] > eq_month,
                                                catalog_above[:, 2] == eq_year))[0]
        catalog_above = np.delete(catalog_above, del_idx_month, axis=0)
        del_idx_day = np.where(np.logical_and(catalog_above[:, 4] >= eq_day,
                                              catalog_above[:, 2] == eq_year,
                                              catalog_above[:, 3] == eq_month))[0]
        catalog_above = np.delete(catalog_above, del_idx_day, axis=0)
        return catalog_above

    def calc_dps_clust(self, catalog_above, Q=None):

        twoDcoord = catalog_above.copy()
        dim_data = toDesc(catalog_above)

        it = 1
        idxX = np.arange(len(dim_data)).astype(int)
        idx_Aclust = np.array([]).astype(int)
        while True:
            if Q is None:
                beta, q = self.dps_param[it-1]
            else:
                beta_array = np.arange(-1, 1.05, 0.05).round(2)
                beta, q = t_runner_mp(dim_data[idxX], Q, beta_array)

            dps_set = dps_clustering(dim_data[idxX], beta, q, r=None)
            Ax, Bx = idxX[dps_set[0]], idxX[dps_set[1]]
            idx_Aclust = np.append(idx_Aclust, Ax)
            idxX = Bx
            it += 1
            if it > self.sfcaz_epoch or len(Bx) == 0:
                out = twoDcoord[idx_Aclust]
                break
        return out, beta, q


    def calc_ext(self, A):
        e = E2XT(A, omega=self.omega, v=self.v, delta=self.delta)
        ext_square = e.e2xt_out_square
        return ext_square

    def visual_dps_clust(self, X, DPS, EXT, eq_above, eq_below, eq, title):
        eq_x, eq_y, eq_year, eq_month, eq_day, eq_mag = eq



        fig = plt.figure(figsize=(16, 12))
        ax = fig.add_subplot(111)

        cd = self.border_coord
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
        ax.scatter(DPS[:, 0], DPS[:, 1], c='g', marker='.', s=90, linewidths=0.1, label='DPS')

        for x, y, r in zip(eq_above[:, 0], eq_above[:, 1], [0.2 for i in range(len(eq_above))]):
            circleA = ax.add_artist(Circle(xy=(x, y),
                                           radius=r, alpha=1, linewidth=4, zorder=4,
                                           edgecolor='r', facecolor='none',))
            ax.scatter(x, y, marker='x', color='k', alpha=0.75)


        circleA = ax.add_artist(Circle(xy=(eq_x, eq_y),
                                       radius=0.3, alpha=1, linewidth=4, zorder=4,
                                       edgecolor='y', facecolor='none', ))
        ax.scatter(eq_x, eq_y, marker='x', color='k', alpha=0.75)

        for x, y, r in zip(eq_below[:, 0], eq_below[:, 1], [0.2 for i in range(len(eq_below))]):
            circleA = ax.add_artist(Circle(xy=(x, y),
                                           radius=r, alpha=1, linewidth=4, zorder=4,
                                           edgecolor='b', facecolor='none', ))
            ax.scatter(x, y, marker='x', color='k', alpha=0.75)

        plt.scatter([], [], c='r', marker='o', s=50, linewidths=0.5,  label='eq before target',
                    zorder=4)
        plt.scatter([], [], c='y', marker='o', s=50, linewidths=0.5, label='target eq',
                    zorder=4)
        plt.scatter([], [], c='b', marker='o', s=50, linewidths=0.5, label='eq after target',
                    zorder=4)


        plt.grid(True)
        plt.title(title)
        plt.legend(loc=8, bbox_to_anchor=(0.5, -0.15), ncol=4)

        plt.savefig(self.save_path + title + '.png', dpi=500)
        plt.close()



original_umask = os.umask(0)
sh = SeismHist()


sh.sh_all_eqs()
#sh.sh_one_eqs_auto_beta(idx_eq=5, q=[-2])


os.umask(original_umask)
