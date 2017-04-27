import os
import time

import numpy as np
import pandas as pd

from dpsCore.core import dps_clust
from dpsModif.tau_runner import t_runner
from alghTools.tools import read_csv, toDesc, remove_zero_depth
from alghTools.drawData import visual_data


def set_var(q, it):
    itBeta = {-4.0: [0.1, -0.1, 0.1, -0.1],
              -3.75: [0.1, -0.2, -0.1, 0],
              -3.5: [0, -0.2, -0.1, 0],
              -3.25: [0, -0.1, -0.1, -0.1],
              -3.0: [0, -0.1, -0.1, -0.1],
              -2.75: [0, -0.1, -0.1, -0.1],
              -2.5: [-0.2, -0.1, -0.2, -0.1],
              -2.25: [-0.1, -0.2, -0.1, -0.2],
              -2.0: [-0.2, -0.1, 0, -0.2]}

    return itBeta[q][it - 1]


def readAlg():
    for q in Q:
        q = round(q, 4)
        print('\nq=%f' % q)
        read_dir = '/Users/Ivan/Documents/workspace/result/kmchf/q=' + str(q) + '/'
        A_coord = np.empty((0, 2))
        iter = 1
        q_dir = '{}{}/'.format(save_path, 'q=' + str(q) + '/')
        if not os.path.exists(q_dir):
            os.makedirs(q_dir)
        while True:
            beta = set_var(q, iter)

            iter_path = read_dir + 'coord_it' + str(iter) + '.csv'
            DPSarray = []
            Barray = []
            frame = pd.read_csv(iter_path, header=0, sep=';', decimal=",")
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
            dps_coord, B_coord = np.asarray(DPSarray).T, np.asarray(Barray).T
            A_coord = np.append(A_coord, dps_coord, axis=0)
            title = 'q={}; it={}, b={}'.format(q, iter, beta)
            visual_data(A_coord, B_coord, title, False, q_dir)

            iter += 1
            if iter > 4:
                break


def runDPSm_qIteration(desc_data, sph_data, bInp, save_path, epochs, Q, sample_eq, betaType):
    for q in Q:
        q = round(q, 3)
        print('\nq=%f' % q)
        dim_data = desc_data
        twoDcoord = sph_data


        q_dir = '{}{}/'.format(save_path, 'q=' + str(q) + '/')
        if not os.path.exists(q_dir):
            os.makedirs(q_dir)

        iter = 1
        idxX = np.arange(len(dim_data)).astype(int)
        idx_Aclust = np.array([]).astype(int)
        while True:

            if betaType == 'find':
                beta, R = t_runner(dim_data[idxX], q, beta_array)
            if betaType == 'read':
                beta = set_var(q, iter)
            if betaType == 'inp':
                beta = bInp

            dps_set = dps_clust(dim_data[idxX], beta, q, r=None)
            Ax, Bx = idxX[dps_set[0]], idxX[dps_set[1]]
            Ait_coord = twoDcoord[Ax]
            Bit_coord = twoDcoord[Bx]

            idx_Aclust = np.append(idx_Aclust, Ax)

            title = 'q={}; it={}, r={}; b={}'.format(q, iter, round(dps_set[3], 4), beta)

            visual_data(twoDcoord[idx_Aclust], Bit_coord, title, False, q_dir, eqs=sample_eq, labels=eq_labels)

            Adf = pd.DataFrame(Ait_coord, columns=['DPSx', 'DPSy'])
            Bdf = pd.DataFrame(Bit_coord, columns=['Bx', 'By'])
            df = pd.concat([Adf, Bdf], axis=1)
            df.to_csv(q_dir + 'coord_it' + str(iter) + '.csv', index=False, header=True,
                      sep=';', decimal=',')

            idxX = Bx

            iter += 1
            if iter > epochs or len(Bx) == 0:
                Adf = pd.DataFrame(twoDcoord[idx_Aclust], columns=['DPSx', 'DPSy'])
                Bdf = pd.DataFrame(twoDcoord[idxX], columns=['Bx', 'By'])
                df = pd.concat([Adf, Bdf], axis=1)
                df.to_csv(q_dir + 'coord_q=%s_final' % q + '.csv', index=False, header=True,
                          sep=';', decimal=',')
                break


# data = read_csv('/Users/Ivan/Documents/workspace/resources/csv/geop/kvz/kvz_dps3.csv').T
# data = read_csv('/Users/Ivan/Documents/workspace/resources/csv/geop/kmch/kmch_dps.csv').T
#data = read_csv('/Users/Ivan/Documents/workspace/resources/csv/geop/altaiSay/altaiSay_DPS.csv').T
desc_data = read_csv('/Users/Ivan/Documents/workspace/resources/csv/geop/baikal/baikal_DPS_2,7.csv').T
# dataDep = read_csv('/Users/Ivan/Documents/workspace/resources/csv/geop/kmch/kmch_depth.csv', col=['d'])[0]

#eq6 = read_csv('/Users/Ivan/Documents/workspace/resources/csv/geop/kmch/kmch_65_71.csv').T
#eq7 = read_csv('/Users/Ivan/Documents/workspace/resources/csv/geop/kmch/kmch_75.csv').T
eq575 = read_csv('/Users/Ivan/Documents/workspace/resources/csv/geop/baikal/baikal_5,75instr.csv').T
eq55 = read_csv('/Users/Ivan/Documents/workspace/resources/csv/geop/baikal/baikal_5,5instr.csv').T
eq6 = read_csv('/Users/Ivan/Documents/workspace/resources/csv/geop/baikal/baikal_6instr.csv').T
eqs = [eq55, eq575, eq6]
eq_labels = ['M5.5+', 'M5.75+', 'M6+']
#eqs = None

sph_data = desc_data.copy()
desc_data = toDesc(desc_data)
# data, sph_data = remove_zero_depth(data, dataDep)

# directory = '/Users/Ivan/Documents/workspace/result/kmchfIIdepth/'
# directory = '/Users/Ivan/Documents/workspace/result/kmchDepth>0oldB/'
save_path = '/Users/Ivan/Documents/workspace/result/baikal_it4_Mc2.7_eq5.75/'

print(len(desc_data), 'data size')

#Q = np.arange(-2.7, -1.7, 0.1)
# Q = [-3.25, -2.75, -2.25]
Q = [-3]

iterStop = 6

# beta_array = np.arange(-1, 1.1, 0.5)
beta_array = np.arange(-1, 1.1, 0.1).round(1)

    #[-1, -0.9, -0.8, -0.7, -0.6, -0.5, -0.4, -0.3, -0.2, -0.1, 0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]

time_start = int(round(time.time() * 1000))

runDPSm_qIteration(desc_data, sph_data, bInp=None, save_path=save_path, epochs=iterStop, Q=Q, sample_eq=eqs, betaType='find')  # betaType: find, read, inp
#readAlg()

finishTime = int(round(time.time() * 1000)) - time_start
print(time.strftime("\n\ntotal time\n%H:%M:%S", time.gmtime(int(finishTime / 1000))))
# выключить эпицентры на карте!!!
