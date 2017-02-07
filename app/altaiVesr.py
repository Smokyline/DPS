import numpy as np
import pandas as pd
import os

from dpsCore.core import dps_clust
from dpsModif.tau_runner import t_runner
from alghTools.tools import *
from alghTools.drawData import visual_data, visual_ext, check_pix_ext
from FCAZ.e2xt import ext_run


def set_var(q, it):
    itBeta = {-4.0: [0.1, -0.1, 0.1, -0.1],
              -3.75: [0.1, -0.2, -0.1, 0],
              -3.5: [0, -0.2, -0.1, 0],
              -3.25: [0, -0.1, -0.1, -0.1],
              -3.0: [0, -0.1, -0.1, -0.1],
              -2.75: [0, -0.1, -0.1, -0.1],
              -2.5: [-0.2, -0.1, -0.2, -0.1],
              -2.25: [-0.1, -0.2, -0.1, -0.2],
              -2.0: [0.0, -0.0, -0.1, -0.2]}

    return itBeta[q][it - 1]

def readAlg():

    DPSarray = []
    Barray = []
    frame = pd.read_csv(dps_path, header=0, sep=';', decimal=",")
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
    return A_coord, B_coord




q_dir = '/Users/Ivan/Documents/workspace/result/altaiSayVII/e2xt/'

eq_ist = read_csv('/Users/Ivan/Documents/workspace/resources/csv/geop/altaiSay/altaiSay_5,5istorA.csv').T
eq_inst = read_csv('/Users/Ivan/Documents/workspace/resources/csv/geop/altaiSay/altaiSay_5,5instA.csv').T
eq_inst10 = read_csv('/Users/Ivan/Documents/workspace/resources/csv/geop/altaiSay/altaiSay_5,5instC2010.csv').T
eqs = [eq_ist, eq_inst, eq_inst10]
eq_labels = ['M5.5+ istor', 'M5.5+ inst', 'M5.5 2010+']

dps_data = read_csv('/Users/Ivan/Documents/workspace/resources/csv/geop/altaiSay/altaiSay_DPS.csv').T
dps1_clust = read_csv('/Users/Ivan/Documents/workspace/resources/csv/geop/altaiSay/altaiSay_DPS_Bel.csv', ['DPSx', 'DPSy']).T
dps2_clust = read_csv('/Users/Ivan/Documents/workspace/resources/csv/geop/altaiSay/altaiSay_DPS_Dze.csv', ['DPSx', 'DPSy']).T

baseM = [84, 101, 45, 53]
##cd = [36, 52, 37, 46] #kvzln

#baseM = [87, 89, 49.5, 50.5]
#q = [-2.0]


#pols_coords = [[84, 47], [84, 53], [101, 53], [101, 48], [91.5, 48], [91.5, 45.5], [89, 45.5], [89, 47]]
pols_coords = [[84, 47], [84, 53], [101, 53], [101, 48.5], [91.5, 48.5], [91.5, 45.5], [89, 45.5], [89, 47]]
omega, v, delta = -4.25, -2., 0.05

dps1_clust = check_dots_in_poly(pols_coords, dps1_clust)

extA = ext_run(dps1_clust, omega=omega, v=v, delta=delta, coord=baseM)
extD = ext_run(dps2_clust, omega=-4, v=-2.25, delta=delta,  coord=baseM)
print('ext 2 %s ' % check_pix_ext(extD, baseM, pols_coords))


uniqueAD_dps, AwD_dps, DwA_dps = points_diff_runner(dps1_clust, dps2_clust)
uniqueAD_ext, AwD_ext, DwA_ext = points_diff_runner(extA, extD)
diffAD_ext = np.append(DwA_ext, AwD_ext,  axis=0)


Adf = pd.DataFrame(extA, columns=['x', 'y'])
Bdf = pd.DataFrame(extD, columns=['x', 'y'])

Adf.to_csv(q_dir+'ext_belov.csv', index=False, header=True, sep=';', decimal=',')
Bdf.to_csv(q_dir+'ext_dze.csv', index=False, header=True, sep=';', decimal=',')





title = 'e2xt o=%s v=%s (%s%s) & dps q=-2 b=[0.1,-0.1,-0.1]' % (omega, v, check_pix_ext(extA, baseM, pols_coords), '%')
print(title)
visual_data(clusterA=dps1_clust, dataX=dps_data, title=title, display_plot=False, direc=q_dir,
            eqs=eqs, baseM=baseM, labels=eq_labels, ext=extA, poly_field=pols_coords, diff_data=[AwD_dps, DwA_dps])


title_diff = '2e2xt_1 o=-4.25 v=-2 vs e2xt_2 o=-4 v=-2.25'
print('разность ext:%s%s' % (check_pix_ext(diffAD_ext, baseM, pols_coords, real_size=True), '%'))
visual_data(clusterA=np.empty((0, 2)), dataX=np.empty((0, 2)), title=title_diff, display_plot=False, direc=q_dir,
            eqs=eqs, baseM=baseM, labels=eq_labels, ext=diffAD_ext, poly_field=pols_coords, real_ext_size=True)

#ex_title = 'e2xt omega=%s v=%s delta=%s' % (omega, v, delta)
#visual_ext(B, A, extA, ex_title, q_dir)


