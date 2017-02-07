import os
from alghTools.tools import *
from alghTools.drawData import visual_data
from dpsCore.core import dps_clust, calc_r


class DPS():
    def __init__(self, data, beta, q, r=None):
        self.data = data
        self.beta = beta
        self.q = q
        self.r = r

    def __str__(self):
        return 'DPS info:\ndata_len:%s beta:%s q%s\n' % (len(self.data), self.beta, self.q)

    def clustering(self):
        print('clustering data...')
        return dps_clust(self.data, self.beta, self.q, self.r)

    def clustering_beta_array(self, B):
        print('clustering data in \nb=%s...' % B)
        dps_sets = []
        for b in B:
            dps_sets.append(dps_clust(self.data, b, self.q, self.r))
        return dps_sets
    def clustering_q_array(self, Q):
        print('clustering data in \nq=%s...' % Q)
        dps_sets = []
        for q in Q:
            dps_sets.append(dps_clust(self.data, self.beta, q, self.r))
        return dps_sets



data = read_csv('/Users/Ivan/Documents/workspace/resources/csv/geop/altaiSay/altaiSay_all.csv', ['x', 'y']).T

#SpData = data.copy()
#data = toDesc(data)

dps = DPS(data, beta=-0.5, q=-2, r=0.29)

dps_set = dps.clustering()

A, B = dps_set[0], dps_set[1]

#Ac, Bc = to2DSpher(SpData, A, B)

#visual_data(data[A], data, display_plot=True, title='')

