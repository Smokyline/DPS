from alghTools.drawData import visual_FCAZ, check_pix_ext, get_border_coord
from alghTools.importData import ImportData
from dpsCore.core import dps_clust
import numpy as np
import pandas as pd
from itertools import product
import math
import sys
import os

def createGrid(delta, coord):

    x_min, x_max, y_min, y_max = coord
    coordinates = list(product(np.arange(x_min, x_max, delta), np.arange(y_min, y_max, delta)))
    grid = np.array(coordinates)

    return grid

def D_pa(A, Z, omega, v):
    #eps = sys.float_info.epsilon
    eps = 0.0000000006
    dpa = np.array([])
    zero_array = np.array([]).astype(int)
    for i, p in enumerate(Z):
        evk_array = np.zeros((1, len(A)))
        for n, d in enumerate(p):
            evk_array += (d - A[:, n]) ** 2
        evk_array = np.sqrt(evk_array[0])

        if np.min(evk_array) <= eps:
            zero_array = np.append(zero_array, i)

        evk_array_woEPS = evk_array[np.where(evk_array > eps)]
        meanEvk = np.mean(evk_array_woEPS)
        evk_array_mEVK = evk_array_woEPS[np.where(evk_array_woEPS <= meanEvk)]
        expMeans = np.mean(evk_array_mEVK ** omega) ** (1 / omega)
        dpa = np.append(dpa, expMeans)

    deltaD = (np.sum(dpa**v) / len(dpa)) ** (1/v)
    idxZ = np.union1d(np.where(dpa <= deltaD)[0], zero_array)
    Apix = Z[idxZ]
    #Apix = Z[np.where(dpa <= deltaD)[0]]
    #Apix = zero_array
    return Apix



def ext_run(A, omega=-4, v=-3, delta=0.05, coord=None):
    print('\ne2xt')
    if coord is None:
        coord = [min(A[:, 0])-1, max(A[:, 0])+1, min(A[:, 1])-1, max(A[:, 1])+1]
    Z = createGrid(delta, coord)
    ZA = D_pa(A, Z, omega, v)
    return ZA


def run_sfcaz(omega, v, delta, region_name, mc_mag, mag_array, q, read_k, target_it):

    imp = ImportData(region_name, main_mag=mc_mag.replace('.', ','),
                     mag_array=mag_array)
    DPS_A = imp.read_dps_res(zone=region_name,
                             mod=region_name+'_%s'%read_k, q=q, iter=target_it)

    origin_data = imp.data_to_dps
    dps_dir = imp.DPS_dir
    eqs, eqs_labels = imp.get_eq_stack()

    """param"""
    #omega = -4
    #v = -2.25
    #delta = 0.05

    coord = get_border_coord()

    Z = createGrid(delta, coord)
    print('len grid', len(Z))

    EXT = D_pa(DPS_A, Z, omega, v)

    pers = check_pix_ext(EXT, pols=[[coord[0], coord[2]], [coord[0], coord[3]],
                                           [coord[1], coord[3]], [coord[1], coord[2]]])

    original_umask = os.umask(0)
    title = 'ext S=%s delta=%s omega=%s v=%s' % (pers, delta, omega, v)
    visual_FCAZ(origin_data, DPS_A, EXT, eqs, eqs_labels, title, path=dps_dir)

    Adf = pd.DataFrame(EXT, columns=['x', 'y'])
    Adf.to_csv(dps_dir + 'ext2.csv', index=False, header=True,
              sep=';', decimal=',')
    os.umask(original_umask)




