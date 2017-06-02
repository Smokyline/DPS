import numpy as np
import pandas as pd
import math
import sys
from shapely.geometry import Polygon, Point


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


def save_DPS_coord(A, B, path, title):
    Adf = pd.DataFrame(A, columns=['DPSx', 'DPSy'])
    Bdf = pd.DataFrame(B, columns=['Bx', 'By'])
    df = pd.concat([Adf, Bdf], axis=1)
    df.to_csv(path + title + '.csv', index=False, header=True,
              sep=';', decimal=',')

def remove_zero_depth(data, dataDep):
    sph_data = data.copy()
    data = toDesc(data)
    depth_zero_idx = np.where(dataDep == 0)[0]
    data = np.delete(data, depth_zero_idx, 0)
    sph_data = np.delete(sph_data, depth_zero_idx, 0)
    return data, sph_data


def toCast2(sph_x, sph_y):
    r = 6371
    desc_data = np.empty((0, 3))
    for i in range(len(sph_x)):
        # az, el = sph_x[i] * math.pi / 180, sph_y[i] * math.pi / 180
        az, el = math.radians(sph_x[i]), math.radians(sph_y[i])
        rcos_theta = r * np.cos(el)
        x = rcos_theta * np.cos(az)
        y = rcos_theta * np.sin(az)
        z = r * np.sin(el)
        xyz = np.array([x, y, z]).reshape((1, 3))
        desc_data = np.append(desc_data, xyz, axis=0)
    return desc_data

def toSpher2(data):
    spher_data = np.empty((0, 2))
    for i in data:
        x, y, z = i[0], i[1], i[2]
        hxy = np.hypot(x, y)
        r = np.hypot(hxy, z)
        # r = 6377

        el = np.arctan2(z, hxy)
        az = np.arctan2(y, x)
        xy = np.array([math.degrees(az), math.degrees(el)]).reshape((1, 2))
        spher_data = np.append(spher_data, xy, axis=0)
    return spher_data

def toDesc(data):
    """
    x = r * sin(y) * cos(x)
    y = r * sin(y) * sin(x)
    z = r * cos(y)
    """
    r = 6371
    desc_data = np.empty((0, 3))
    for i in data:
        x, y = i[0] * math.pi / 180, i[1] * math.pi / 180
        xyz = []
        xyz.append(r * math.cos(y) * math.cos(x))
        xyz.append(r * math.cos(y) * math.sin(x))
        xyz.append(r * math.sin(y))
        xyz = np.array(xyz).reshape((1, 3))
        desc_data = np.append(desc_data, xyz, axis=0)
    return desc_data


def toSpher(data):
    spher_data = np.empty((0, 2))
    for i in data:
        x, y, z = i[0], i[1], i[2]
        r = math.sqrt(x ** 2 + y ** 2 + z ** 2)
        # r = 6371
        xy = []
        xy.append(math.atan2(y, x) * r / 180)
        xy.append(math.atan2(math.sqrt(x ** 2 + y ** 2), z) * r / 180)
        xy = np.array(xy).reshape((1, 2))
        spher_data = np.append(spher_data, xy, axis=0)
    return spher_data


def to2DSpher(sph_data, A, B):
    """
    time_start = int(round(time.time() * 1000))

    if len(A) == 0:
        Asph = A
        Bsph = sph_data
    elif len(B) == 0:
        Asph = sph_data
        Bsph = B
    else:
        if len(A[0]) == 2:
            Asph = A
            Bsph = B
        else:
            aIndex = []
            bIndex = []

            def search(i, A):
                for a in A:
                    if i[0] == a[0] and i[1] == a[1] and i[2] == a[2]:
                        return True

            for n, d in enumerate(data):
                if search(d, A):
                    aIndex.append(n)
                else:
                    bIndex.append(n)
            Asph = sph_data[aIndex]
            Bsph = sph_data[bIndex]
    print('%i ms to2d' % (int(round(time.time() * 1000))-time_start))
    """
    return sph_data[A], sph_data[B]

def checkLin(xyLin, X, Y):
    x0, y0 = xyLin[0, 0], xyLin[0, 1]
    x1, y1 = xyLin[1, 0], xyLin[1, 1]
    k = (y1 - y0) / (x1 - x0)
    x2 = []
    y2 = []
    for i in range(len(X)):

        y = k * X[i]
        if Y[i] >= y:
            x2.append(X[i])
            y2.append(Y[i])

def points_diff_runner(A, B):
    """coord"""
    #eps = sys.float_info.epsilon
    eps = 0.00000006
    def a_w_b(A, B):
        awbArray = np.empty((0, 2))
        for i, a in enumerate(A):
            fDimEQLS = np.where(abs(B[:, 0] - a[0]) < eps)[0]
            if len(fDimEQLS) > 0:
                sDimEQLA = np.where(abs(B[fDimEQLS, 1] - a[1]) < eps)[0]
                if len(sDimEQLA) == 0:
                    awbArray = np.append(awbArray, np.array([a]), axis=0)
            else:
                awbArray = np.append(awbArray, np.array([a]), axis=0)
        return awbArray

    AwB_array = a_w_b(A, B)
    BwA_array = a_w_b(B, A)
    uniqueArray = np.empty((0, 2))

    for i, a in enumerate(A):
        fDimEQLS = np.where(abs(B[:, 0] - a[0]) < eps)[0]
        if len(fDimEQLS) > 0:
            sDimEQLA = np.where(abs(B[fDimEQLS, 1] - a[1]) < eps)[0]
            if len(sDimEQLA) > 0:
                uniqueArray = np.append(uniqueArray, np.array([a]), axis=0)

    return uniqueArray, AwB_array, BwA_array

def check_dots_in_poly(coord_pols, dots):
    poly_dots = np.empty((0, 2))
    poly = Polygon(coord_pols)
    for dot in dots:
        p = Point(dot[0], dot[1])
        if poly.contains(p):
            poly_dots = np.append(poly_dots, [dot], axis=0)
    return poly_dots
