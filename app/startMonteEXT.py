from FCAZ.e2xt import *
from Monte.createField import *
from Monte.MonteEXT import *
from alghTools.drawData import visual_MontePlot
from alghTools.tools import read_csv
import numpy as np
import os




def run_EQiteration(extTrue, xyPoly, num_dots, iteration=100, savedir=None):
    rand_eps_array = []
    A, B = 0, 0
    print('\niteration')
    for i in range(iteration):
        if (i * 100 / iteration) % 20 == 0 and i != 0:
            print('%i of %i' % (i, iteration))

        rEQ_dots = inputPoly(xyPoly, num_dots=num_dots)

        #save_points_to_txt(rEQ_dots, savedir, i)

        eps_random, Ai, Bi = calcW_pix_ext(extTrue, rEQ_dots, xyPoly)

        save_acc_to_txt(Bi, savedir)

        A += Ai
        B += Bi
        rand_eps_array.append(eps_random)
    return rand_eps_array, np.sum(rand_eps_array)/iteration, A/iteration, B/iteration


def monteCarlo(ext, eq, poly_coord, num_iter, savedir=None):
    xyPoly = np.array(poly_coord)
    real_ext = check_data_point_in_poly(xyPoly, ext)
    real_eq = check_data_point_in_poly(xyPoly, eq)
    print('\nMonteCarlo\next:%i eq%i' % (len(real_ext), len(real_eq)))
    A = range(len(real_ext))

    eq_r_count = len(real_eq)
    eps_eqReal, Areal, Breal = calcW_pix_ext(real_ext, real_eq, xyPoly)  # мат ожидание реальных точек
    strREAL = '\nreal eq ext eps:%f   real eq ext A:%i B:%i' % (100 - (eps_eqReal * 100), Areal, Breal)
    print(strREAL)


    # random eq
    eps_eqRandArray, eps_eqRand, Arand, Brand = run_EQiteration(extTrue=real_ext, xyPoly=xyPoly,
                                                                num_dots=eq_r_count, iteration=num_iter,
                                                                savedir=savedir)  # мат ожидание случайных точек
    strRANDeq = '\nrandom eq eps:%f  random eq A:%s B:%s' % (100 - (eps_eqRand * 100), round(Arand, 2), round(Brand, 2))
    print(strRANDeq)

    # random DPS
    #eps_dpsRand, AdpsRand, BdpsRand = 0, 0, 0
    #strRANDdps = '\nrandom dps eps:%f  random dps A:%s B:%s' % (100 - (eps_dpsRand * 100), round(AdpsRand, 2), round(BdpsRand, 2))
    #print(strRANDdps)

    title = '|ext|=%i |eq|=%i it=%i eps_real=%s eps_rand=%s' % (len(ext), len(real_eq), num_iter,
                                                                round((100 - (eps_eqReal * 100)), 2), round((100 - (eps_eqRand * 100)), 2))
    return eps_eqReal, eps_eqRandArray, title, strREAL, strRANDeq


    #random_dots = inputPoly(xyPoly, num_dots=eq_r_count)  # случайные точки в многоугольнике
    #visual_dataPoly(real_ext[A], None, random_dots, xyPoly, 'random_eq'+title, direct)
    #visual_dataPoly(real_ext[A], None, real_eq, xyPoly, 'real_eq'+title, direct)

"""
def run_ext(coord, ext_param):

    dir_dps = '/Users/Ivan/Documents/workspace/resources/csv/geop/altaiSay/'
    A = read_csv(dir_dps + 'altaiSay_'+versions[0]+'.csv', ['DPSx', 'DPSy']).T

    omega, v, delta = ext_param
    Z = createGrid(delta, coord)
    ZA = D_pa(A, Z, omega, v)
    return ZA
"""
def run_MCext():
    pols_coords = [[84, 47], [84, 53], [101, 53], [101, 48.5], [91.5, 48.5], [91.5, 45.5], [89, 45.5], [89, 47]]
    # coord = [40, 52, 37, 45] #kvz
    # coord = [84, 102, 45, 56] #altai
    field_coord = [84, 101, 45, 53]  # altai

    #saveDir = '/Users/Ivan/Documents/workspace/result/monte/altai_e2xt/'

    if not os.path.exists(saveDir):
        os.makedirs(saveDir)

    ext_param = -4.25, -2.0, 0.05  # omega v delta bel
    #ext_param = -4, -2.25, 0.05  # omega v delta dze

    #ext = run_ext(field_coord, ext_param)
    exts = []
    for i in range(len(versions)):
        exts.append(read_csv(saveDir+'ext_'+versions[i]+'.csv', list('xy')).T)
    print('ext finished')

    eq_ist = read_csv('/Users/Ivan/Documents/workspace/resources/csv/geop/altaiSay/altaiSay_5,5istorA.csv').T
    eq_inst = read_csv('/Users/Ivan/Documents/workspace/resources/csv/geop/altaiSay/altaiSay_5,5instA.csv').T
    eq_inst10 = read_csv('/Users/Ivan/Documents/workspace/resources/csv/geop/altaiSay/altaiSay_5,5instC2010.csv').T
    eq_dots = np.append(eq_ist, eq_inst, axis=0)
    eq_dots = np.append(eq_dots, eq_inst10, axis=0)

    num_it = 500
    epsRe, epsRa = [], []
    #for i, ext in enumerate(exts):
    for i, ext in enumerate(exts):
        print(versions[i], end='\n')
        eps_real, eps_rand, title, strREAL, strRANDeq = monteCarlo(ext, eq_dots, pols_coords, num_it, saveDir)
        epsRe.append([eps_real for n in range(num_it)])
        epsRa.append(eps_rand)


        text_file = open(saveDir + "monte_log" + versions[i] + ".txt", "w")
        text_file.write("%s\n%s\n%s" % (title, strREAL, strRANDeq))
        text_file.close()



    #visual_MontePlot(epsRe, epsRa, title, versions, saveDir)

#versions = ['belov', 'dze']
versions = ['dze']
#versions = ['belov']
saveDir = '/Users/Ivan/Documents/workspace/result/altaySay/altaiSay_control/e2xt/'

run_MCext()
