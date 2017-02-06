import numpy as np

from dpsCore.core import dps_clust, calc_r
from alghTools.tools import to2DSpher, toDesc
from alghTools.drawData import visual_data


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


def calc_p(A, B, r, p_max):
    pA = calc_range(A, A, r)
    pB = calc_range(A, B, r)
    maxA = p_max
    pA = np.true_divide(pA, maxA)
    pB = np.true_divide(pB, maxA)

    return pA.reshape((len(pA), 1)), pB.reshape((len(pB), 1))


def t_runner(data, Q, beta_array, iteration, q_dir):
    tau_array = []
    #data = toDesc(data)

    param_array = np.empty((0, 7))

    R = calc_r(data, q=Q)

    for b in beta_array:
        beta = round(b, 2)
        idxA, idxB, q, r, b, a, p_max = dps_clust(data, beta=round(beta, 3), r=R, q=Q)

        if (len(idxA) == 0) or (len(idxB) == 0):
            tau = 0
            param_array = np.append(param_array, [[q, r, b, a, 0, 0, 0]], axis=0)
        else:
            pA, pB = calc_p(data[idxA], data[idxB], R, p_max)
            a_m = p_mean(pA, -2)
            b_m = p_mean(pB, 2)
            tau = a_m - b_m
            param_array = np.append(param_array, [[q, r, b, a, a_m, b_m, tau]], axis=0)
        print('tau:{}'.format(round(tau, 7)))
        tau_array.append(tau)

    ans = np.empty((0, 3))
    tau_array = np.asarray(tau_array)
    for i, t in enumerate(tau_array):
        if t == 0:
            ans = np.vstack((ans, [beta_array[i], 0, t]))
        else:
            y = tau_c(tau_array[np.where(tau_array > 0)], t)
            ans = np.vstack((ans, [beta_array[i], y, t]))

    y = ans[:, 1].reshape((1, len(ans[:, 1])))
    param_array = np.append(param_array.T, y, axis=0)

    print('\n------------------')

    for y in ans:
        print('beta:{}; y:{}; tau:{}'.format(
            round(y[0], 3),
            round(y[1], 4),
            round(y[2], 4)))


    abs_array = np.asarray(abs(ans[:, 1] - 0.2))
    abs_array = abs_array.reshape(len(abs_array), 1)
    b_array = np.asarray(ans[:, 0]).reshape(len(ans[:, 0]), 1)
    close_2sample = np.append(b_array, abs_array, axis=1)
    close_2sample = close_2sample[np.where(ans[:, 1] != 0)]
    arg_min = np.argmin(close_2sample[:, 1])


    best_beta = round(close_2sample[arg_min, 0], 3)
    print('\nbest beta:{}'.format(round(best_beta, 3)))
    #title = 'tau q={}; it={}, r={}; b={}'.format(round(Q, 3), iteration, round(R, 5), round(best_beta, 3))

    return best_beta, R

