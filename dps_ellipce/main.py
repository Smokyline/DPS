import pandas as pd
import numpy as np
import os

from dps_ellipce.generate_elli import generate_ellipses
from dps_ellipce.core import elli_dps_clust
from dps_ellipce.draw_map import draw_ellipce

import time

def read_csv(path, col=['x', 'y']):
    array = []
    frame = pd.read_csv(path, header=0, sep=';', decimal=",")
    for i, title in enumerate(col):
        cell = frame[title].values

        try:
            cell = cell[~np.isnan(cell)]
        except Exception as ex:
            print(ex)
            for j, c in enumerate(cell):
                try:
                    np.float(c.replace(',', '.'))
                except:
                    print('Error in row:%s "%s"' % (j, c))

        array.append(cell)
    return np.array(array)


def save_to_csv(ellipses, Pxa, angles, title):
    X = []
    Y = []


    for i, elli in enumerate(ellipses):
        x, y, a, b, angles_array, f1_array, f2_array = [v for v in elli]
        X.append(x)
        Y.append(y)


    """сохранение расстояний XV в csv файл """
    path = '/home/ivan/Documents/workspace/result/test/'
    original_umask = os.umask(0)
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

    xydf = pd.DataFrame(np.array([X, Y]).T, columns=['x', 'y'])
    pdf = pd.DataFrame(Pxa, columns=['P'])
    angldf = pd.DataFrame(angles, columns=['angles'])
    df = pd.concat([xydf, pdf], axis=1)
    df = pd.concat([df, angldf], axis=1)

    df.to_csv(path + title + '.csv', index=False, header=True,
              sep=';', decimal=',')

    os.umask(original_umask)

def save_to_csv_matrix(ellipses, Pxa, angles, title):
    XYP = []




    for i, elli in enumerate(ellipses):
        x, y, a, b, angles_array, f1_array, f2_array = [v for v in elli]
        XYP.append([x, y, Pxa[i]])


    out_matrix = np.resize(XYP, (len(ellipses), len(ellipses)))
    print(out_matrix.shape)


    """сохранение расстояний XV в csv файл """
    path = '/home/ivan/Documents/workspace/result/test/'
    original_umask = os.umask(0)
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

    #xydf = pd.DataFrame(np.array([X, Y]).T, columns=['x', 'y'])
    #pdf = pd.DataFrame(Pxa, columns=['P'])
    #angldf = pd.DataFrame(angles, columns=['angles'])
    #df = pd.concat([xydf, pdf], axis=1)
    #df = pd.concat([df, angldf], axis=1)

    df = pd.DataFrame(out_matrix)
    df.to_csv(path + title + '.csv', index=False, header=True,
              sep=';', decimal=',')

    os.umask(original_umask)

#path = '/home/ivan/Documents/workspace/resources/csv/GEO/kmch/kmch_dps.csv'
#path = '/home/ivan/Documents/workspace/resources/csv/GEO/calif/calif_dps.csv'
path = '/home/ivan/Documents/workspace/resources/csv/GEO/kmch/kmch_40.csv'
#path = '/home/ivan/Documents/workspace/resources/csv/GEO/calif/California_ANSS_3_0.csv'
data = read_csv(path).T

xy_lim = [155, 170, 49, 60, 0.1]
#xy_lim = [-126, -114, 31, 42, 1]
angle_tick = 2


#elli_len = [1.2, 0.1]
elli_len = [xy_lim[4]*np.sqrt(2), (xy_lim[4]*np.sqrt(2))/5]
ellipses = generate_ellipses(xy_lim, angle_tick, elli_len)

print('data count:', len(data))
print('ellipses count:', len(ellipses))


time_start = int(round(time.time() * 1000))
ellipses_out, angles_out_array = elli_dps_clust(ellipses, data, beta=0.0)
print('seismic ellipses count:', len(ellipses_out))
finishTime = int(round(time.time() * 1000)) - time_start
print(time.strftime("\n\ntotal time\n%H:%M:%S", time.gmtime(int(finishTime / 1000))))

save_to_csv(ellipses, ellipses_out, angles_out_array, title='kmch_40_elli_1')
#save_to_csv_matrix(ellipses, ellipses_out, angles_out_array, title='calif_test')
#draw_ellipce(ellipses_out, angles_out_array, data)
