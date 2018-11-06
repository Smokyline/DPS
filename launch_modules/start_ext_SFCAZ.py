from fcaz_modules.importData import ImportData
from main.e2xt_core import E2XT
from fcaz_modules.drawData import get_border_coord, check_pix_ext, visual_FCAZ
import os
import pandas as pd

omega=-4
v=-2.25
delta=0.05
region_name='kmch'
mc_mag='3.5'
mag_array=['7', '7,5', '8']
#q='[-2.0; -3.0]'
q='-3'
read_k='I'
target_it=2

# import data
imp = ImportData(region_name, main_mag=mc_mag.replace('.', ','),
                     mag_array=mag_array)
DPS_A = imp.read_dps_res(zone=region_name,
                         mod=region_name + '_%s' % read_k, q=q, iter=target_it)

origin_data = imp.data_to_dps
dps_dir = imp.DPS_dir
eqs, eqs_labels = imp.get_eq_stack()

# calc e2xt
e = E2XT(DPS_A, omega, v, delta)
ext_square = e.e2xt_out_square
ext_pers = check_pix_ext(ext_square)

# visual e2xt
original_umask = os.umask(0)
title = 'ext S=%s delta=%s omega=%s v=%s' % (ext_pers, delta, omega, v)
visual_FCAZ(origin_data, DPS_A, ext_square, eqs, eqs_labels, title, path=dps_dir)

Adf = pd.DataFrame(ext_square, columns=['x', 'y'])
Adf.to_csv(dps_dir + 'ext2.csv', index=False, header=True,
          sep=';', decimal=',')
os.umask(original_umask)