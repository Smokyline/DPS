from fcaz_modules.tools import read_csv_pandas
from fcaz_modules.importData import ImportData
from fcaz_modules.drawData import visual_FCAZ

import os





original_umask = os.umask(0)
workspace_path = os.path.expanduser('~' + os.getenv("USER") + '/Documents/workspace/')
region_name = 'kmch'
mc_mag = '3.5'
k_iter = 'III'
q = '[-2.0; -3.0]'
# COORD MAP!!!

save_path = workspace_path+'result/DPS/%s/%s_%s/q=%s/' % (region_name, region_name, k_iter, q)
imp = ImportData(region_name, main_mag=mc_mag.replace('.', ','), mag_array=['7', '7,5', '8'])
eqs, eq_labels = imp.get_eq_stack()
X = imp.data_to_dps
DPS_clusters = read_csv_pandas(save_path + 'DPS.csv')[:, :2]
ext = read_csv_pandas(save_path + 'ext2.csv')

visual_FCAZ(X, DPS_clusters, ext, eqs, eq_labels, 'FCAZ kIII', save_path)


