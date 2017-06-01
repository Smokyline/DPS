import numpy as np

from dpsCore.core import dps_clust, calc_r
from alghTools.tools import to2DSpher, toDesc
from alghTools.drawData import visual_eq_DPS


def tau_c(T, tauI):
    N = []
    for t in T:
        # n = (c,a); c=t,a=tauI
        N.append((tauI - t) / max(tauI, t))
    return np.mean(np.array(N))


def p_mean(X, p):
    return (np.mean(X ** p)) ** (1 / p)


def calc_range(A, B, r):
    array = []
    for i in B:
        evk_array = np.zeros((1, len(A)))
        for n, d in enumerate(i):
            evk_array += (d - A[:, n]) ** 2
        evk_array = np.sqrt(evk_array)
        evk_array = evk_array[np.where(evk_array <= r)]
        Pa_i = np.sum(np.subtract(1.0, np.true_divide(evk_array, r)))
        array.append(Pa_i)
    return array


def calc_tau_p(A, B, r, p_max):
    pA = calc_range(A, A, r)
    pB = calc_range(A, B, r)
    pA = np.true_divide(pA, p_max)
    pB = np.true_divide(pB, p_max)

    return pA.reshape((len(pA), 1)), pB.reshape((len(pB), 1))


def t_runner(data, Q, beta_array):
    tau_array = []
    b_and_q_comb = [(b, q) for b in beta_array for q in Q]
    rads = [calc_r(data, q=q) for q in Q]

    for bq in b_and_q_comb:
        beta = round(bq[0], 2)
        q = round(bq[1], 2)

        if len(Q) == 1:
            r = rads[0]
        else:
            r = rads[np.ravel(np.where(Q == bq[1]))[0]]

        print('/////////////////////\nbeta:%s q:%s r:%s' % (beta, q, r))

        dps_set = dps_clust(data, beta=beta,  q=q, r=r)
        idxA, idxB, p_max = dps_set[0], dps_set[1], dps_set[6]

        if (len(idxA) == 0) or (len(idxB) == 0):
            tau = 0
        else:
            pA, pB = calc_tau_p(data[idxA], data[idxB], r, p_max)
            a_m = p_mean(pA, -2)
            b_m = p_mean(pB, 2)
            tau = a_m - b_m
        print('tau:%f' % tau)
        tau_array.append(tau)

    ans = []
    tau_array = np.asarray(tau_array)
    for i, t in enumerate(tau_array):
        if t == 0:
            ans.append([b_and_q_comb[i], 0, t])
        else:
            y = tau_c(tau_array[np.where(tau_array > 0)], t)
            ans.append([b_and_q_comb[i], y, t])
    ans = np.array(ans)

    print('\n------------------')
    for y in ans:
        print(y)

    close_idx = np.argmin(abs(ans[:, 1] - 0.2))
    best_beta, best_q = b_and_q_comb[close_idx]

    print('\nbest beta:%s q:%s' % (best_beta, best_q))

    return round(best_beta, 2), round(best_q, 2)

