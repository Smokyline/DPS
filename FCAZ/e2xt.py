from alghTools.drawData import visual_ext
from alghTools.importData import ImportData
from dpsCore.core import dps_clust
import numpy as np
import pandas as pd
import math
import sys

def createGrid(delta, coord):
    xMin, xMax, yMin, yMax = coord
    grid = np.empty((0, 2))
    X = np.arange(xMin, xMax + delta, delta)
    Y = np.arange(yMin, yMax + delta, delta)
    for x in X:
        for y in Y:
            grid = np.append(grid, np.array([[x, y]]), axis=0)

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


def run():

    imp = ImportData(zone='baikal', main_mag='2,7', mag_array=['5,5', '5,75', '6'])
    DPS_A = imp.read_dps_res(zone='baikal', mod='baikal_it6_Mc2.8', q='-2.5')
    dps_dir = imp.DPS_dir
    eqs, eqs_labels = imp.get_eq_stack()

    """param"""
    omega = -4
    v = -3
    delta = 0.05
    # coord = [40, 52, 37, 45] #kvz
    # coord = [84, 102, 45, 56] #altai
    #coord = [75, 105, 45, 55]  # altai
    coord = [96, 123, 47, 59]  # baikal

    Z = createGrid(delta, coord)
    print('len grid', len(Z))

    EXT = D_pa(DPS_A, Z, omega, v)

    title = 'ext delta=%s omega=%s v=%s' % (delta, omega, v)
    visual_ext(DPS_A, EXT, eqs, eqs_labels, title, path=dps_dir)

    Adf = pd.DataFrame(EXT, columns=['x', 'y'])
    Adf.to_csv(dps_dir + 'ext2.csv', index=False, header=True,
              sep=';', decimal=',')

run()