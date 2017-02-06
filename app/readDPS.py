import os
import time

import numpy as np
import pandas as pd

from dpsCore.DPSold import dps_clust
from dpsModif.tau_runner import t_runner
from alghTools.tools import read_csv, toDesc, remove_zero_depth
from alghTools.drawData import visual_data


def read():
    DPSarray = []
    Barray = []
    frame = pd.read_csv(read_file, header=0, sep=';', decimal=",")
    for i, title in enumerate(['DPSx', 'DPSy']):
        try:
            val = frame[title].values
            val = val[np.logical_not(np.isnan(val))]
            DPSarray.append(val)
        except:
            print('no_' + title, end=' ')
    for i, title in enumerate(['Bx', 'By']):
        try:
            val = frame[title].values
            val = val[np.logical_not(np.isnan(val))]
            Barray.append(val)
        except:
            print('no_' + title, end=' ')
    A_coord, B_coord = np.asarray(DPSarray).T, np.asarray(Barray).T
    title = 'dps q=-2 b=[0.1,-0.1,-0.1] A=%s B=%s' % (len(A_coord), len(B_coord))
    visual_data(A_coord, B_coord, title=title, display_plot=True, direc=q_dir, eqs=eqs, baseM=baseM, labels=['M5.5+'])

read_file = '/Users/Ivan/Documents/workspace/result/altaiSayIII/q=-2.0/coord_q=-2.0_final.csv'
eq55 = read_csv('/Users/Ivan/Documents/workspace/resourses/csv/geop/altaiSay/altaiSay_5,5.csv').T
eqs = [eq55]
q_dir = '/Users/Ivan/Documents/workspace/result/altaiSayIII/'
if not os.path.exists(q_dir):
        os.makedirs(q_dir)

baseM = [76, 102, 42, 56]

read()