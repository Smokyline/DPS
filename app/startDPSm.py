import os
import time

import numpy as np
import pandas as pd

from dpsCore.core import dps_clust
from dpsModif.tau_runner import t_runner
from alghTools.tools import read_csv, toDesc, remove_zero_depth
from alghTools.drawData import visual_data
from alghTools.importData import ImportData


def runDPSm_qIteration(desc_data, sph_data, bInp, save_path, epochs, Q, sample_eq, betaType):

    dim_data = desc_data
    twoDcoord = sph_data

    if len(Q) == 1:
        q_dir = '%s/q=%s/' % (save_path, Q[0])

    else:
        q_dir = '%s/q=[%s; %s]/' % (save_path, max(Q), min(Q))


    if not os.path.exists(q_dir):
        os.makedirs(q_dir)

    iter = 1
    idxX = np.arange(len(dim_data)).astype(int)
    idx_Aclust = np.array([]).astype(int)
    while True:
        print('\nQ=%s' % Q)
        if betaType == 'find':
            beta, q = t_runner(dim_data[idxX], Q, beta_array)
        if betaType == 'inp':
            beta = bInp

        dps_set = dps_clust(dim_data[idxX], beta, q, r=None)
        Ax, Bx = idxX[dps_set[0]], idxX[dps_set[1]]
        Ait_coord = twoDcoord[Ax]
        Bit_coord = twoDcoord[Bx]

        idx_Aclust = np.append(idx_Aclust, Ax)
        #TODO запись результата в txt

        title = 'it={}; q={}, r={}; b={}'.format(iter, q, round(dps_set[3], 4), beta)

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


region_name = 'baikal'

imp = ImportData(region_name, main_mag='2,7', mag_array=['5,5', '5,75', '6'])

desc_data = imp.data_dps
eqs, eq_labels = imp.get_eq_stack()


sph_data = desc_data.copy()
desc_data = toDesc(desc_data)
# data, sph_data = remove_zero_depth(data, dataDep)

# directory = '/Users/Ivan/Documents/workspace/result/kmchfIIdepth/'
# directory = '/Users/Ivan/Documents/workspace/result/kmchDepth>0oldB/'
save_path = '/Users/Ivan/Documents/workspace/result/%s/%s_it6_Mc2.7/' % (region_name, region_name)

print(len(desc_data), 'data size')

Q = [-2.25]
#Q = np.arange(-2.4, -3.1, -0.1)
#Q = np.arange(-2., -3.1, -0.1)

epochs = 4

# beta_array = np.arange(-1, 1.1, 0.5)
beta_array = np.arange(-1, 1.1, 0.1).round(1)

time_start = int(round(time.time() * 1000))
runDPSm_qIteration(desc_data, sph_data, bInp=None, save_path=save_path, epochs=epochs, Q=Q, sample_eq=eqs, betaType='find')  # betaType: find, read, inp
#readAlg()

finishTime = int(round(time.time() * 1000)) - time_start
print(time.strftime("\n\ntotal time\n%H:%M:%S", time.gmtime(int(finishTime / 1000))))
# выключить эпицентры на карте!!!
