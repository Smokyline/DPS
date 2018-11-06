import numpy as np
import sys
import time
import math


eps = sys.float_info.epsilon


def calc_r(data, q):
    evk = 0
    count = 0

    for i, j in enumerate(data):
        evk_array = np.zeros((1, len(data[i + 1:])))
        for n, d in enumerate(j):
            evk_array += (d - data[i + 1:, n])**2
        evk_array = np.sqrt(evk_array[0])
        #evk_array = np.sqrt((j[0]-data[i+1:, 0])**2+(j[1]-data[i+1:, 1])**2+(j[2]-data[i+1:, 2])**2)
        evk_array = evk_array[np.where(evk_array > eps)]**q

        #evk_array = evk_array**q
        Earray = np.sum(evk_array)
        if Earray > eps:
            count += len(evk_array)
            evk += Earray
    r = (evk / count) ** (1 / q)
    print('r:{}'.format(r))
    return r

def find_rX(data, Rq):
    adaR = []
    for i in data:
        evk_array = np.zeros((1, len(data)))
        for n, d in enumerate(i):
            evk_array += (d - data[:, n]) ** 2
        evk = np.sqrt(evk_array[0])
        evk = evk[np.where(evk > 0)]
        adaR.append(np.power(np.sum(np.power(evk, Rq))/(len(evk)-1), 1/Rq))
    print('maxR:%f: minR:%f' % (min(adaR), max(adaR)))
    return np.asarray(adaR)

def find_nchRx(data, gamma):
    nchRarr = []

    def foo(dxy, gamma):
        R = (dxy * (1-gamma))/(1+gamma)
        return R

    for i in data:
        evk_array = np.zeros((1, len(data)))
        for n, d in enumerate(i):
            evk_array += (d - data[:, n]) ** 2
        dxy = np.mean(np.sqrt(evk_array[0]))
        r = foo(dxy, gamma)
        nchRarr.append(r)
    print('minR:%f; maxR:%f' % (min(nchRarr), max(nchRarr)))
    return np.asarray(nchRarr)


def calp_PwR(data, p_m, Pq):
    #pArray = np.zeros((1, len(data)))
    pArray = []
    #XYarray = np.empty((0, len(data)))
    #XYarray = [0 for i in range(len(data))]
    XYarray = np.zeros((1, len(data)))[0]


    def gXpFoo(evk):
        #return (np.sum(evk**Pq))/(len(evk))**(1/Pq)
        return np.power(np.sum(np.power(evk, Pq))/(len(evk)), 1/Pq)

    for w, i in enumerate(data):
        evk_array = [0 for i in range(len(data))]

        for n, d in enumerate(i):
            evk_array += (d - data[:, n]) ** 2
        evk_array = np.sqrt(evk_array)
        gxp = gXpFoo(evk_array[np.where(evk_array > 0)])
        nch = (gxp - evk_array)/(gxp + evk_array)
        delta_x = (nch + 1) / 2
        #print(min(delta_x), max(delta_x))
        #XYarray = np.vstack((XYarray, delta_x))
        XYarray += delta_x
        #XYarray = np.append(XYarray, [delta_x], axis=0)

    pArray = XYarray
    #pArray = XYarray
    if p_m is None:
        p_max = max(pArray)
        Pxa = np.true_divide(pArray, p_max)
        return np.array(Pxa), p_max
    else:
        p_max = p_m
        Pxa = np.true_divide(pArray, p_max)
        return np.array(Pxa)


def phi(M, m):
    if m < M:
        return m/M
    else:
        return 1

def calc_p(data, r, p_m, adaRadP=None, Pq=1, M=None, adaptR=False, nchR=False):
    array = []
    R=[]
    for j, i in enumerate(data):
        evk_array = np.zeros((1, len(data)))

        for n, d in enumerate(i):
            evk_array += (d - data[:, n]) ** 2
        evk_array = np.sqrt(evk_array[0])

        if adaRadP is not None:
            ri = max(r, adaRadP[j])
            #ri = adaRadP[j]
            #R.append([adaRadP[j], i[0], i[1]])
        else:
            ri = r

        evk_array = evk_array[np.where(evk_array <= ri)]
        if M is None:
            PxI = np.sum(np.subtract(1.0, np.true_divide(evk_array, ri)))**Pq
        else:
            m = M[1][j]
            phiM = phi(M[0], m)
            PxI = np.sum(np.subtract(1.0, np.true_divide(evk_array, ri)))*phiM
        array.append(PxI)



    if p_m is None:
        p_max = max(array)
        Pxa = np.true_divide(array, p_max)
        return np.array(Pxa), p_max
    else:
        p_max = p_m
        Pxa = np.true_divide(array, p_max)
        return np.array(Pxa)



def calc_a(Pxa, beta, dXY=None, adaA=False):
    min_x = 0.0
    max_x = 1.0
    alpha = 0
    epsl = 0.00001



    def foo(B, a, beta):
        EPx = []
        for b in B:
            EPx.append((a - b) / max(a, b))
        return np.mean(EPx) - beta

    def adaFoo(B, a, beta, dXY):
        EPx = []
        for i, b in enumerate(B):
            EPx.append((a - b) / max(a, b)*dXY[i])
        return (np.sum(EPx)/np.sum(dXY))-beta
    def adaFooMean(B, a, beta, dXY):
        c = np.sum(B*dXY)/sum(dXY)
        nch = (a-c)/max(a, c)
        return nch-beta

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

        if adaA:
            #fA_min = adaFoo(Pxa, min_x, beta, dXY)
            #fA_max = adaFoo(Pxa, max_x, beta, dXY)
            #fA_half = adaFoo(Pxa, half_x, beta, dXY)
            fA_min = adaFooMean(Pxa, min_x, beta, dXY)
            fA_max = adaFooMean(Pxa, max_x, beta, dXY)
            fA_half = adaFooMean(Pxa, half_x, beta, dXY)
        else:
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
    if not adaA:
        print('alpha:%f' % alpha)
    return alpha


def calc_adaA(data, Pxa, Aq, beta):
    adaAlphaArray = []

    for j, i in enumerate(data):
        evk_array = np.zeros((1, len(data)))
        for n, d in enumerate(i):
            evk_array += (d - data[:, n]) ** 2
        evk_array = np.sqrt(evk_array[0])
        #ri = max(r, adaRad[j])
        Rx = np.mean(evk_array)
        evkRindex = np.where(evk_array <= Rx)
        Pxy = Pxa[evkRindex]
        evk_array = evk_array[evkRindex]
        dXY = np.subtract(1.0, np.true_divide(evk_array, Rx))**Aq
        adaAi = calc_a(Pxy, beta, dXY, adaA=True)
        adaAlphaArray.append(adaAi)
    print('minAlpha:%f maxAlpha:%f' % (min(adaAlphaArray), max(adaAlphaArray)))
    return np.asarray(adaAlphaArray)


def searchAlphaIndex(Pxa, alpha, adaAlpha, adatpA):
    Aindex = []
    Bindex = []
    if adatpA:
        for i, p in enumerate(Pxa):
            if p >= adaAlpha[i]:
                Aindex.append(i)
            else:
                Bindex.append(i)
    else:
        for i, p in enumerate(Pxa):
            if p >= alpha:
                Aindex.append(i)
            else:
                Bindex.append(i)
    return Aindex, Bindex


def dps_clust(data, beta, r, q, Pq=1, Rq=1, Aq=1, g=1, M=None, adaptR=False, adaptA=False, nchR=False, pWr=False):
    X = np.arange(len(data)).astype(int)
    print('\nbeta:{} q:{}'.format(round(beta, 2), q))
    time_start = int(round(time.time() * 1000))
    if r is None:
        r = calc_r(data[X], q)
    it = 1
    a = None
    p_sample = None
    adaRad = []
    adaAlpha = []
    upd_dataIndex = X
    dps_set = None
    B_data = []

    while True:

        if it == 1:
            if nchR:
                adaRad = find_nchRx(data[upd_dataIndex], g)
            elif adaptR:
                adaRad = find_rX(data[upd_dataIndex], Rq)
            else:
                adaRad = None
            if pWr:
                Pxa, p_sample = calp_PwR(data[upd_dataIndex], None, Pq)
            else:
                Pxa, p_sample = calc_p(data[upd_dataIndex], r, None, adaRadP=adaRad, Pq=Pq, M=M, adaptR=adaptR, nchR=nchR)
            #print('minP:%f; maxP:%f' % (min(Pxa), max(Pxa)))
            if adaptA:
                adaAlpha = calc_adaA(data[upd_dataIndex], Pxa, Aq, beta)
            else:
                a = calc_a(Pxa, beta)
                #a = 1/p_sample
        else:
            if pWr:
                Pxa = calp_PwR(data[upd_dataIndex], p_sample, Pq)
            else:
                Pxa = calc_p(data[upd_dataIndex], r, p_sample, adaRadP=adaRad, Pq=Pq, M=M, adaptR=adaptR, nchR=nchR)


        #print(min(Pxa), max(Pxa))
        if adaptA:
            Aindex, Bindex = searchAlphaIndex(Pxa, None, adaAlpha, adaptA)
            adaAlpha = adaAlpha[Aindex]
        else:
            Aindex, Bindex = searchAlphaIndex(Pxa, a, None, adaptA)

        if adaRad is not None:
            adaRad = adaRad[Aindex]
        if M is not None:
            M[1] = M[1][Aindex]

        DPS_clust, B_clust = upd_dataIndex[Aindex], upd_dataIndex[Bindex]
        B_data.extend(B_clust)
        #if np.array_equal(DPS_clust, upd_dataIndex) or len(DPS_clust) == 0:
        if len(DPS_clust) == len(upd_dataIndex) or len(DPS_clust) == 0:

            dps_set = [DPS_clust, B_data, q, r, beta, a, p_sample]
            break
        else:
            upd_dataIndex = DPS_clust
            it += 1
    print('A:{}; B:{}'.format(len(dps_set[0]), len(dps_set[1])))
    print('main iteration:{}'.format(it))
    finishTime = int(round(time.time() * 1000))-time_start
    #print('%i ms | %i:%f min' % (finishTime, finishTime/1000/60,  finishTime/1000 % 60))
    print('%i ms | %s' % (finishTime, time.strftime("%H:%M:%S", time.gmtime(int(finishTime/1000)))))
    return np.array(dps_set)
