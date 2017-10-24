import os
from alghTools.tools import *
from alghTools.drawData import draw_DPS_res
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


workspace_path = os.path.expanduser('~' + os.getenv("USER") + '/Documents/workspace/')

data = read_csv(workspace_path+'resources/csv/GEO/baikal/baikal_DPS_2,7.csv', ['x', 'y']).T

SpData = data.copy()
data = toCast2(data[:, 0], data[:, 1])

dps = DPS(data, beta=0.0, q=-2, r=0.29)

dps_set = dps.clustering()

A, B = dps_set[0], dps_set[1]

Ac, Bc = toSpher2(data[A]), toSpher2(data[B])


title = 'q:%s b:%s r:%f' %(dps_set[2], dps_set[4], dps_set[3])
draw_DPS_res(Ac, Bc, title=title)
#visual_data(data[A], data, title, False, save_path=workspace_path+'/result/test/', eqs=sample_eq, labels=eq_labels, origData_name=region_name + mc_mag)


