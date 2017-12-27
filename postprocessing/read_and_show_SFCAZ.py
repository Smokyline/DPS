import os
import numpy as np
from fcaz_modules.tools import *
from fcaz_modules.importData import ImportData
from fcaz_modules.drawData import visual_SFCAZ


original_umask = os.umask(0)
workspace_path = os.path.expanduser('~' + os.getenv("USER") + '/Documents/workspace/')
region_name = 'kmch'
mc_mag = '3.5'
q = '[-2.0; -3.0]'
title = '%s KI KII KIII' % region_name
# COORD MAP!!!

imp = ImportData(region_name, main_mag=mc_mag.replace('.', ','), mag_array=['7', '7,5', '8'])
eqs, eq_labels = imp.get_eq_stack()


EXT = read_csv(workspace_path + 'result/DPS/%s/%s_%s/q=%s/'
                      % (region_name, region_name, 'I', q) + 'ext2.csv')

DPS_B = read_csv(workspace_path + 'result/DPS/%s/%s_%s/q=%s/'
                      % (region_name, region_name, 'I', q) + 'DPS.csv')[:, 2:]
DPS_A_set = []
for k in ['I', 'II', 'III']:
    dps = read_csv(workspace_path + 'result/DPS/%s/%s_%s/q=%s/'
                      % (region_name, region_name, k, q)+'DPS.csv')[:, :2]
    DPS_A_set.append(dps)

visual_SFCAZ(DPS_B, DPS_A_set, EXT, eqs, eq_labels, title, workspace_path + 'result/DPS/%s/%s_%s/q=%s/'
                      % (region_name, region_name, 'I', q))

os.umask(original_umask)
