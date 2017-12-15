from monte_ext.monte_carlo import Monte
from fcaz_modules.tools import read_csv
import os
import numpy as np


def get_pols_coord():
    #pols_coords = [[84, 47], [84, 53], [101, 53], [101, 48.5], [91.5, 48.5], [91.5, 45.5], [89, 45.5], [89, 47]]
    pols_coord = [[155, 49], [155, 51], [157, 52.2], [157.3,53.7], [159, 56.5],
                  [162.5, 56.6], [165, 56.6], [167.7,55.5], [167, 54], [164.5,54],
                  [159, 49],[155, 49]]

    return np.array(pols_coord)



region_name = 'kmch'
k_iter = 'III'
mc_mag = '3.5'
mag_array = ['7', '7,5', '8']
q='[-2.0; -3.0]'
num_it = 500
dot_size = 350

workspace_path = os.path.expanduser('~' + os.getenv("USER") + '/Documents/workspace/')
save_path = workspace_path + 'result/DPS/%s/%s_%s/q=%s/' % (region_name, region_name, k_iter, q)
eq_dots = read_csv('/home/ivan/Documents/workspace/resources/csv/GEO/%s/%s_%smonte.csv'%(
    region_name, region_name, '8'))  # monte M>=

original_umask = os.umask(0)
if not os.path.exists(save_path):
    os.makedirs(save_path)

dps = read_csv(save_path + 'ext2.csv')
ext_data = read_csv(save_path + 'DPS.csv')
pols_coord = get_pols_coord()

# MONTE

m = Monte(ext_data, eq_dots, pols_coord, rand_it=num_it, dot_size=dot_size, save_path=save_path)
m.calc_real_w()
m.calc_random_w(save_acc=False)



