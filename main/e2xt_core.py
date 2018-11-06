import numpy as np
from itertools import product


class E2XT():
    def __init__(self, X, omega, v, delta):
        self.X = X
        self.omega = omega
        self.v = v
        self.delta = delta
        self.field_coord = [min(X[:, 0])-1, max(X[:, 0])+1, min(X[:, 1])-1, max(X[:, 1])+1]

        self.createGrid()
        self.D_pa()

    def createGrid(self):
        # creating e2xt square grid
        x_min, x_max, y_min, y_max = self.field_coord
        grid = list(product(np.arange(x_min, x_max, self.delta),
                                   np.arange(y_min, y_max, self.delta)))
        self.Z = np.array(grid)

    def D_pa(self):
        #eps = sys.float_info.epsilon
        eps = 0.0000000006
        dpa = np.array([])
        zero_array = np.array([]).astype(int)
        for i, p in enumerate(self.Z):
            evk_array = np.zeros((1, len(self.X)))
            for n, d in enumerate(p):
                evk_array += (d - self.X[:, n]) ** 2
            evk_array = np.sqrt(evk_array[0])

            if np.min(evk_array) <= eps:
                zero_array = np.append(zero_array, i)

            evk_array_woEPS = evk_array[np.where(evk_array > eps)]
            meanEvk = np.mean(evk_array_woEPS)
            evk_array_mEVK = evk_array_woEPS[np.where(evk_array_woEPS <= meanEvk)]
            expMeans = np.mean(evk_array_mEVK ** self.omega) ** (1 / self.omega)
            dpa = np.append(dpa, expMeans)

        deltaD = (np.sum(dpa**self.v) / len(dpa)) ** (1/self.v)
        idxZ = np.union1d(np.where(dpa <= deltaD)[0], zero_array)
        self.e2xt_out_square = self.Z[idxZ]


