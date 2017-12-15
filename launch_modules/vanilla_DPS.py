import os
from fcaz_modules.tools import *
from fcaz_modules.drawData import draw_DPS_res
from main.dps_core import dps_clustering, calc_r


class DPS():
    def __init__(self, data_path, beta, q, r=None):
        workspace_path = os.path.expanduser('~' + os.getenv("USER") + '/Documents/workspace/')

        self.data = read_csv(workspace_path+data_path)
        self.sph_data, self.desc_data = self.convert_sph_data_to_desc(self.data)
        self.beta = beta
        self.q = q
        self.r = r

    def __str__(self):
        return 'DPS info:\ndata_len:%s beta:%s q%s\n' % (len(self.data), self.beta, self.q)

    def convert_sph_data_to_desc(self, data):
        sph_data = data.copy()
        desc_data = toDesc(data)
        return sph_data, desc_data

    def clustering(self):
        # vanilla dps clustering
        print('clustering data...')
        self.dps_set = dps_clustering(self.data, self.beta, self.q, self.r)

    def clustering_beta_array(self, B):
        print('clustering data in \nb=%s...' % B)
        self.dps_set = []
        for b in B:
            self.dps_set.append(dps_clustering(self.data, b, self.q, self.r))

    def clustering_q_array(self, Q):
        print('clustering data in \nq=%s...' % Q)
        self.dps_set = []
        for q in Q:
            self.dps_set.append(dps_clustering(self.data, self.beta, q, self.r))

    def parse_dps_set(self):
        self.A_idx, self.B_idx, self.q, self.r, self.beta, \
        self.alpha, self.norm_p = self.dps_set
        self.A_coord, self.B_coord = self.sph_data[self.A_idx], self.sph_data[self.B_idx]


original_umask = os.umask(0)


data_path = 'resources/csv/GEO/baikal/baikal_DPS_2,7.csv'


dps = DPS(data_path, beta=0.0, q=-2, r=None)
dps.clustering()
dps.parse_dps_set()


title = 'q:%s b:%s r:%.3f' %(dps.q, dps.beta, dps.r)
draw_DPS_res(dps.A_coord, dps.B_coord, title=title)


os.umask(original_umask)


