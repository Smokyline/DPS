import numpy as np
import os
from fcaz_modules.tools import read_csv, save_DPS_coord



def read_dps_res(path, it):
    dps_A = np.empty((0, 2))
    dps_B = np.empty((0, 2))
    for i in range(1, it+ 1):
        print(i)
        i_dps = read_csv(path + 'coord_it%i.csv' % (i))
        dps_A = np.append(dps_A, i_dps[:, :2], axis=0)
        dps_B = np.append(dps_B, i_dps[:, 2:], axis=0)

    return dps_A, dps_B


#workspace_path = os.path.expanduser('~' + os.getenv("USER") + '/Documents/workspace/result/DPS/')

path = '/home/ivan/Documents/workspace/result/DPS/kmch/kmch_I/q=-3/'
out_name = 'DPS'


A, B = read_dps_res(path, it=2)
A = A[~np.isnan(A[:, 0])]
B = B[~np.isnan(B[:, 0])]

original_umask = os.umask(0)
save_DPS_coord(A, B, path, out_name)
os.umask(original_umask)


