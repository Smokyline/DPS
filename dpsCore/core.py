import numpy as np
import sys
import time
import math




def calc_r(data, q):
    evk = 0
    count = 0
    eps = sys.float_info.epsilon

    for i, j in enumerate(data):
        evk_array = np.zeros((1, len(data[i + 1:])))
        for n, d in enumerate(j):
            evk_array += (d - data[i + 1:, n])**2
        evk_array = np.sqrt(evk_array[0])
        evk_array = evk_array[np.where(evk_array > eps)[0]]**q
        Earray = np.sum(evk_array)
        if Earray > eps:
            count += len(evk_array)
            evk += Earray
    r = (evk / count) ** (1 / q)
    print('r:%f' % r)
    return r


def calc_p(data, r, p_max):
    array = []
    for j, xy in enumerate(data):
        evk_array = np.zeros((1, len(data)))
        for d, i in enumerate(xy):
            evk_array += (i - data[:, d]) ** 2
        evk_array = np.sqrt(evk_array[0])
        evk_array = evk_array[np.where(evk_array <= r)]
        PxI = np.sum(np.subtract(1.0, np.true_divide(evk_array, r)))
        array.append(PxI)

    if p_max is None:
        p_max = np.max(array)
        Pxa = np.true_divide(array, p_max)
        return Pxa, p_max
    else:
        Pxa = np.true_divide(array, p_max)
        return Pxa



def calc_a(Pxa, beta):
    min_x = 0.0
    max_x = 1.0
    epsl = 0.0000006

    def foo(B, a, beta):
        EPx = []
        for b in B:
            EPx.append((a - b) / max(a, b))
        return np.mean(EPx) - beta

    def foo_max(Pxa, max_x):
        x = max_x
        while True:
            zn = foo(Pxa, x, 0)
            if zn < beta:
                x *= 2
            else:
                return x
    max_x = foo_max(Pxa, max_x)

    while True:
        half_x = (max_x + min_x) / 2
        fA_min = foo(Pxa, min_x, beta)
        fA_max = foo(Pxa, max_x, beta)
        fA_half = foo(Pxa, half_x, beta)

        if fA_min == 0:
            alpha = min_x
            break
        if fA_half == 0:
            alpha = half_x
            break
        if fA_max == 0:
            alpha = max_x
            break

        if fA_min * fA_half < 0:
            max_x = half_x
        else:
            min_x = half_x

        if max_x - min_x < epsl:
            alpha = half_x
            break
    print('alpha:%f' % alpha)
    return alpha


def searchAlphaIndex(Pxa, alpha):
    Aindex = np.where(Pxa >= alpha)[0]
    Bindex = np.where(Pxa < alpha)[0]
    return Aindex, Bindex


def dps_clust(data, beta, q, r=None):
    time_start = int(round(time.time() * 1000))

    a = None
    norm_p = None
    B_data = []

    upd_dataIndex = np.arange(len(data)).astype(int)
    if r is None:
        r = calc_r(data[upd_dataIndex], q)


    it = 1

    while True:
        #time_start2 = int(time.time() * 1000)
        #print(int(time.time() * 1000) - time_start2)


        if it == 1:
            Pxa, norm_p = calc_p(data[upd_dataIndex], r=r, p_max=norm_p)

            a = calc_a(Pxa, beta)

        else:
            Pxa = calc_p(data[upd_dataIndex], r, norm_p)

        Aindex, Bindex = searchAlphaIndex(Pxa, a)
        A_clust, B_clust = upd_dataIndex[Aindex], upd_dataIndex[Bindex]


        B_data.extend(B_clust)
        #if np.array_equal(DPS_clust, upd_dataIndex) or len(DPS_clust) == 0:
        if len(A_clust) == len(upd_dataIndex) or len(A_clust) == 0:
            dps_set = [A_clust, B_data, q, r, beta, a, norm_p]
            break
        else:
            upd_dataIndex = A_clust
            it += 1

    print('A:{}; B:{}'.format(len(dps_set[0]), len(dps_set[1])))
    print('dpsCore iteration:{}'.format(it))
    finishTime = int(round(time.time() * 1000))-time_start  # millsec
    print('%i ms | %s' % (finishTime, time.strftime("%H:%M:%S", time.gmtime(int(finishTime/1000)))))
    return dps_set
