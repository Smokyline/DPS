import numpy as np
import sys
import time
import math


class DPSEllipce():
    def __init__(self, data, beta, a, b, angle_tick):
        self.data = data

        self.beta = beta

        self.a = a
        self.b = b
        self.angle_tick = angle_tick

        print('data_count=%s beta=%s angle_tick=%s\n' % (len(data), beta, angle_tick))


    def clustering(self):
        time_start = int(round(time.time() * 1000))

        self.ellipses = self.generate_ellipses(self.data, angle_tick=self.angle_tick,
                                          a=self.a, b=self.b)

        alpha = None
        norm_p = None
        B_data = []

        upd_dataIndex = np.arange(len(self.data)).astype(int)

        it = 1
        while True:
            if it == 1:
                Pxa, norm_p = self.calc_p(upd_dataIndex, p_max=norm_p)
                Px_first_it = np.append(self.data[upd_dataIndex], np.array([Pxa]).T, axis=1)

                alpha = self.calc_a(Pxa)

            else:
                Pxa = self.calc_p(upd_dataIndex, p_max=norm_p)
            Aindex, Bindex = self.searchAlphaIndex(Pxa, alpha)
            A_clust, B_clust = upd_dataIndex[Aindex], upd_dataIndex[Bindex]

            B_data.extend(B_clust)
            if len(A_clust) == len(upd_dataIndex) or len(A_clust) == 0:
                dps_set = [A_clust, B_data, Px_first_it, alpha, norm_p]
                break
            else:
                upd_dataIndex = A_clust
                it += 1

        print('A:{}; B:{}'.format(len(dps_set[0]), len(dps_set[1])))
        print('alpha:%.5f main iteration:%i' % (alpha, it))
        finishTime = int(round(time.time() * 1000)) - time_start  # millsec
        print('%i ms | %s' % (finishTime, time.strftime("%H:%M:%S", time.gmtime(int(finishTime / 1000)))))
        return dps_set

    def evk_foo(self, i, data):
        evk_array = np.zeros((1, len(data)))
        for n, d in enumerate(i):
            evk_array += (d - data[:, n]) ** 2
        evk_array = np.sqrt(evk_array[0])
        return evk_array

    def calc_focus_elli(self, a, b, centr):
        c = np.sqrt((a ** 2) - (b ** 2))
        return [centr[0] - c, centr[1]], [centr[0] + c, centr[1]]

    def rotate_focus_elli(self, f1, f2, angle, centr):
        f_rotated = []
        for f in [f1, f2]:
            X = centr[0] + (f[0] - centr[0]) * np.cos(np.deg2rad(angle)) - (f[1] - centr[1]) * np.sin(np.deg2rad(angle))
            Y = centr[1] + (f[1] - centr[1]) * np.cos(np.deg2rad(angle)) - (f[0] - centr[0]) * np.sin(np.deg2rad(angle))
            f_rotated.append([X, Y])
        return f_rotated[0], f_rotated[1]

    def generate_ellipses(self, elli_center_coord, angle_tick, a, b):
        angles = np.arange(0, 180, angle_tick)
        print('generate ellipses with param:\ncount_elli=%s a=%s b=%s\nangles %s' % (
        len(elli_center_coord), a, b, angles))

        ellipses = []
        for i, xy in enumerate(elli_center_coord):
            x, y = xy

            ellipse = [x, y, a, b]

            f1, f2 = [], []
            f1_original, f2_original = self.calc_focus_elli(a, b, xy)
            for angle in angles:
                f1_rot, f2_rot = self.rotate_focus_elli(f1_original, f2_original, angle, centr=xy)
                f1.append(f1_rot)
                f2.append(f2_rot)
            for value in [angles, f1, f2]:
                ellipse.append(value)
            ellipses.append(ellipse)
        return ellipses

    def calc_p(self, upd_idx, p_max):
        iterat_data = self.data[upd_idx]
        elli_P_array = []
        for j in upd_idx:
            x, y, a, b, angles_array, f1_array, f2_array = [v for v in self.ellipses[j]]

            evk_array = np.zeros((1, len(iterat_data)))
            for d, i in enumerate([x, y]):
                evk_array += (i - iterat_data[:, d]) ** 2
            evk_array = np.sqrt(evk_array[0])
            radius_data = iterat_data[np.where(evk_array <= self.a*2)]

            angle_count_data_in_elli = []
            for f1_k, f2_k in zip(f1_array, f2_array):
                l = self.evk_foo(f1_k, radius_data) + self.evk_foo(f2_k, radius_data)
                count_data = len(np.where(l <= 2 * a)[0])
                angle_count_data_in_elli.append(count_data)

            elli_P_array.append(np.max(angle_count_data_in_elli))

        if p_max is None:
            p_max = np.max(elli_P_array)
            Pxa = np.true_divide(elli_P_array, p_max)
            return Pxa, p_max
        else:
            Pxa = np.true_divide(elli_P_array, p_max)
            return Pxa

    def searchAlphaIndex(self, Pxa, alpha):
        Aindex = np.where(Pxa >= alpha)[0]
        Bindex = np.where(Pxa < alpha)[0]
        return Aindex, Bindex

    def calc_a(self, Pxa):
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
                if zn < self.beta:
                    x *= 2
                else:
                    return x

        max_x = foo_max(Pxa, max_x)

        while True:
            half_x = (max_x + min_x) / 2
            fA_min = foo(Pxa, min_x, self.beta)
            fA_max = foo(Pxa, max_x, self.beta)
            fA_half = foo(Pxa, half_x, self.beta)

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







