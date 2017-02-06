import numpy as np
import os

def calc_eps_disc(A, B, N, p):
    """w ожидание попаданий B множества в p границе"""
    w = 0
    idx_true_points = np.array([]).astype(int)
    idx_false_points = np.array([]).astype(int)
    for j, i in enumerate(B):
        evk_array = np.zeros((1, len(A)))
        for d, n in enumerate(i):
            evk_array += (n - A[:, d]) ** 2
        evk_array = np.sqrt(evk_array[0])
        idx_evk = np.where(evk_array <= p)[0]
        if len(idx_evk) > 0:
            idx_true_points = np.append(idx_true_points, j)
            w += 1
        else:
            idx_false_points = np.append(idx_false_points, j)
    return w / N, idx_true_points, idx_false_points

