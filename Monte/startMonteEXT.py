from E2XT.e2xt import *
from Monte.create_ext_squares import *
from Monte.plotingMonteEXT import *
from alghTools.drawData import visual_MontePlot, check_pix_ext
from alghTools.tools import read_csv_pandas
import numpy as np
import os


from alghTools.drawData import visual_MC_dataPoly


def run_EQiteration(extTrue, xyPoly, num_dots, iteration=100, savedir=None):
    rand_eps_array = []
    A, B = 0, 0
    print('\niteration')
    for i in range(iteration):
        if (i * 100 / iteration) % 20 == 0 and i != 0:
            print('%i of %i' % (i, iteration))

        rEQ_dots = input_random_dots_in_poly(xyPoly, num_dots=num_dots)

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
    #visual_dataPoly(real_ext[A], None, real_eq, , 'real_eq'+title, direct)
    #data_real, data_rand, title, versions, directory
    #visual_ext(Breal, [[],], EXT, eqs, eqs_labels, cd, title, path=None)



def get_pols_coord():
    #pols_coords = [[84, 47], [84, 53], [101, 53], [101, 48.5], [91.5, 48.5], [91.5, 45.5], [89, 45.5], [89, 47]]
    pols_coord = [[155, 49], [155, 51], [157, 52.2], [157.3,53.7], [159, 56.5],
                  [162.5, 56.6], [165, 56.6], [167.7,55.5], [167, 54], [164.5,54],
                  [159, 49],[155, 49]]

    return pols_coord

def import_dps_and_ext():
    ext_data = read_csv_pandas(save_path + 'ext2.csv')
    dps = read_csv_pandas(save_path + 'DPS.csv')

    return dps, ext_data


workspace_path = os.path.expanduser('~' + os.getenv("USER") + '/Documents/workspace/')


region_name = 'kmch'
k_iter = 'III'
mc_mag = '3.5'
mag_array = ['7', '7,5', '8']
q='[-2.0; -3.0]'


save_path = workspace_path + 'result/DPS/%s/%s_%s/q=%s/' % (region_name, region_name, k_iter, q)
eq_dots = read_csv_pandas('/home/ivan/Documents/workspace/resources/csv/GEO/%s/%s_%smonte.csv'%(
    region_name, region_name, '8'))  # monte M>=

original_umask = os.umask(0)
if not os.path.exists(save_path):
    os.makedirs(save_path)

dps, ext_data = import_dps_and_ext()
pols_coord = get_pols_coord()
visual_MC_dataPoly(dps[:, :2], dps[:, 2:], ext_data, eq_dots, pols_coord, title='pols', direct=save_path)

s_ext = check_pix_ext(ext_data, pols_coord)
print('S ext: %s' % s_ext)

# monte carlo
num_it = 500

epsRe, epsRa = [], []
eps_real, eps_rand, title, strREAL, strRANDeq = monteCarlo(ext_data, eq_dots, pols_coord,
                                                           num_it, save_path)


text_file = open(save_path + "monte_log.txt", "w")
text_file.write("%s\n%s\n%s" % (title, strREAL, strRANDeq))
text_file.close()

os.umask(original_umask)
