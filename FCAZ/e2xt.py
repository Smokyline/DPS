from alghTools.tools import read_csv
from alghTools.drawData import visual_ext
from dpsCore.core import dps_clust
import numpy as np
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
    # data = read_csv('/Users/Ivan/Documents/workspace/resourses/csv/geop/kvz/kvz_dps3.csv').T
    # dps_set = dps_clust(data=data, beta=-0.4, r=None, q=-3.0)
    # A, r = data[dps_set[0]], dps_set[3]
    directory = '/Users/Ivan/Documents/workspace/result/altaiSayIV/'
    q_dir = directory + 'q=-2/'
    A = read_csv(q_dir + 'coord_q=-2_final.csv', ['DPSx', 'DPSy']).T
    data = np.array([])

    omega = -4
    v = -3
    delta = 0.05
    # coord = [40, 52, 37, 45] #kvz
    # coord = [84, 102, 45, 56] #altai
    coord = [75, 105, 45, 55]  # altai

    Z = createGrid(delta, coord)
    print('len grid', len(Z))

    ZA = D_pa(A, Z, omega, v)

    title = 'extIV delta=%s omega=%s v=%s' % (delta, omega, v)
    visual_ext(data, A, ZA, title)