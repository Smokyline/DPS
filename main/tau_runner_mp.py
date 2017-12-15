import multiprocessing as mp

from main.dps_core import dps_clustering, calc_r
from main.tau_runner import tau_c, p_mean, calc_tau_p, np


def calc_bq_tau(queue, data, bq, Q, rads):
    beta = round(bq[0], 2)
    q = round(bq[1], 2)

    if len(Q) == 1:
        r = rads[0]
    else:
        r = rads[np.ravel(np.where(Q == bq[1]))[0]]

    #print('/////////////////////\nbeta:%s q:%s r:%s' % (beta, q, r))

    dps_set = dps_clustering(data, beta=beta, q=q, r=r)
    idxA, idxB, p_max = dps_set[0], dps_set[1], dps_set[6]

    if (len(idxA) == 0) or (len(idxB) == 0):
        tau = 0
    else:
        pA, pB = calc_tau_p(data[idxA], data[idxB], r, p_max)
        a_m = p_mean(pA, -2)
        b_m = p_mean(pB, 2)
        tau = a_m - b_m
    return queue.put(tau)

def t_runner_mp(data, Q, beta_array):
    b_and_q_comb = [(b, q) for b in beta_array for q in Q]
    rads = [calc_r(data, q=q) for q in Q]


    tau_array = []
    for bq_start in range(0, len(b_and_q_comb), 8):
        core_bq = b_and_q_comb[bq_start:bq_start + 8]
        core_que = []
        for bq in core_bq:
            qe = mp.Queue()
            p = mp.Process(target=calc_bq_tau, args=(qe, data, bq, Q, rads))
            core_que.append(qe)
            p.start()
        core_que = [qe.get() for qe in core_que]
        tau_array.extend(core_que)
    tau_array = np.array(tau_array)

    ans = []
    for i, t in enumerate(tau_array):
        if t == 0:
            ans.append([b_and_q_comb[i], 0, t])
        else:
            y = tau_c(tau_array[np.where(tau_array > 0)], t)
            ans.append([b_and_q_comb[i], y, t])
    ans = np.array(ans)



    close_idx = np.argmin(abs(ans[:, 1] - 0.2))
    best_beta, best_q = b_and_q_comb[close_idx]

    print('\nbest beta:%s q:%s' % (best_beta, best_q))

    return round(best_beta, 2), round(best_q, 2)