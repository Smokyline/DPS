from alghTools.tools import read_csv, toDesc
from alghTools.drawData import visual_MC_dataPoly
from dpsCore.core import dps_clust
from Monte.createField import inputPoly, create_customPoly, check_data_point_in_poly
from Monte.MonteCore import calc_eps_disc
import numpy as np
import os

class MonteCarlo():
    def __init__(self, data, eq):
        self.data = data
        self.eq = eq


def run_EQiteration(dataTrue, xyPoly, num_dots, p, iteration=100):
    rand_eps_array = []
    A, B = 0, 0
    print('\niteration')
    for i in range(iteration):
        if (i * 100 / iteration) % 20 == 0 and i != 0:
            print('%i of %i' % (i, iteration))

        r_dots = inputPoly(xyPoly, num_dots=num_dots)
        eps_random, Ai, Bi = calc_eps_disc(dataTrue, r_dots, num_dots, p)
        A += len(Ai)
        B += len(Bi)
        rand_eps_array = np.append(rand_eps_array, eps_random)
    return rand_eps_array, np.mean(rand_eps_array), A/iteration, B/iteration

def run_DPSiteration(eqTrue, xyPoly, dps_param, p, iteration):
    rand_eps_array = np.array([])
    A, B = 0, 0
    num_dots, beta, q = dps_param[0], dps_param[1], dps_param[2]
    print('\niteration')
    for i in range(iteration):
        if (i * 100 / iteration) % 20 == 0 and i != 0:
            print('%i of %i' % (i, iteration))

        r_dots = inputPoly(xyPoly, num_dots=num_dots)
        rand_dps = dps_clust(r_dots, beta, q, r=None)
        Adps = rand_dps[0]
        eps_random, Ai, Bi = calc_eps_disc(r_dots[Adps], eqTrue, num_dots, p)
        A += len(Ai)
        B += len(Bi)
        rand_eps_array = np.append(rand_eps_array, eps_random)
    return np.mean(rand_eps_array), A / iteration, B / iteration

def monteCarlo(dps, eq, polyCoord, dps_param, p, num_iter, direct=None):
    xyPoly = create_customPoly(polyCoord)
    data = check_data_point_in_poly(xyPoly, dps)
    eq_dots = check_data_point_in_poly(xyPoly, eq)
    print('\nMonteCarlo\ndata:%i eq%i' % (len(data), len(eq_dots)))
    A = range(len(data))

    eqRcount = len(eq_dots)
    eps_eqRand, eps_eqReal, Areal, Breal = calc_eps_disc(A=data[A], B=eq_dots, N=eqRcount, p=p)  # мат ожидание реальных точек
    strREAL = '\nreal eq dps eps:%f   real eq dps A:%i B:%i' % (100 - (eps_eqReal * 100), len(Areal), len(Breal))

    # random eq
    eps_eqArrayRand, eps_eqRand, Arand, Brand = run_EQiteration(dataTrue=data[A], xyPoly=xyPoly, num_dots=eqRcount, p=p, iteration=num_iter)  # мат ожидание случайных точек
    strRANDeq = '\nrandom eq eps:%f  random eq A:%s B:%s' % (100 - (eps_eqRand * 100), round(Arand, 2), round(Brand, 2))

    # random DPS
    eps_dpsRand, AdpsRand, BdpsRand = run_DPSiteration(eqTrue=eq_dots, xyPoly=xyPoly, dps_param=dps_param, p=p, iteration=num_iter)
    strRANDdps = '\nrandom dps eps:%f  random dps A:%s B:%s' % (100 - (eps_dpsRand * 100), round(AdpsRand, 2), round(BdpsRand, 2))
    print(strREAL, strRANDeq, strRANDdps)

    title = 'ndata=%i eq=%i it=%i' % (dps_param[0], len(eq_dots), num_iter)
    text_file = open(direct+"monte_log.txt", "w")
    text_file.write("%s\n%s\n%s%s" % (title, strREAL, strRANDeq, strRANDdps))
    text_file.close()

    random_dots = inputPoly(xyPoly, num_dots=eqRcount)  # случайные точки в многоугольнике
    visual_MC_dataPoly(data[A], None, random_dots, xyPoly, 'random_eq' + title, direct)
    visual_MC_dataPoly(data[A], None, eq_dots, xyPoly, 'real_eq' + title, direct)


data = read_csv('/Users/Ivan/Documents/workspace/resources/csv/geop/kvz/KAV_CRIM_M2_DPS.csv').T
#eq_dots = read_csv('/Users/Ivan/Documents/workspace/resources/csv/geop/altaiSay/altaiSay_5,5.csv').T
eq_dots = read_csv('/Users/Ivan/Documents/workspace/resources/csv/geop/kvz/KAV_CRIM_EQ4,5.csv').T

saveDir = '/Users/Ivan/Documents/workspace/result/monte/one/'
if not os.path.exists(saveDir):
    os.makedirs(saveDir)

coordPoly = [[32.5, 43], [32.5, 45.2], [44.5, 45.2], [42, 41.5], [41, 41.5], [39, 43]]  # kvz crm
#coordPoly = [[82, 46], [82, 53], [99, 53], [99, 48], [91, 48], [91, 46]]  # altai

p = 0.225
num_it = 500
dps_param = [2398, 0.1, -3]
monteCarlo(data, eq_dots, coordPoly, dps_param, p, num_it, direct=saveDir)