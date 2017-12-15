import numpy as np
import random
import codecs
import os

from shapely.geometry import Polygon, Point
from monte_ext.calc_ext_w import calcW_pix_ext

class Monte():
    def __init__(self, ext, eq, coord_poly, rand_it, dot_size, save_path):
        self.eq = eq
        self.num_dots = len(eq)
        self.ext = ext
        self.random_it = rand_it

        self.coord_poly = coord_poly
        self.polygon = Polygon(coord_poly)

        self.dot_size = dot_size
        self.save_path = save_path


    def calc_real_w(self):
        """мат ожидание реальных точек"""
        real_ext = self.get_data_point_in_poly(self.ext)
        real_eq = self.get_data_point_in_poly(self.eq)
        print('\nMonteCarlo\next:%i eq%i' % (len(real_ext), len(real_eq)))

        self.w_real, self.Areal, self.Breal = calcW_pix_ext(real_ext, real_eq, self.coord_poly, self.dot_size)
        print('\nreal eq ext eps:%f   real eq ext A:%i B:%i' %
              (100 - (self.w_real * 100), self.Areal, self.Breal))


    def calc_random_w(self, save_acc=False):
        """мат ожидание случайных точек"""

        w_rand_array = []
        Arand, Brand = 0, 0
        omission = []
        print('\niteration')
        for i in range(self.random_it):
            if (i * 100 / self.random_it) % 20 == 0 and i != 0:
                print('%i of %i' % (i, self.random_it))

            rEQ_dots = self.generate_random_dots_in_poly(num_dots=self.num_dots)
            # save_points_to_txt(rEQ_dots, savedir, i)

            w_rand, Ai, Bi = calcW_pix_ext(self.ext, rEQ_dots, self.coord_poly, self.dot_size)
            omission.append(Bi)

            Arand += Ai
            Brand += Bi
            w_rand_array.append(w_rand)

        if save_acc:
            self.save_acc_to_txt(omission, self.save_path)

        self.w_rand = np.sum(w_rand_array) / self.random_it
        self.Arand = Arand / self.random_it
        self.Brand = Brand / self.random_it
        print('\nrandom eq eps:%f  random eq A:%s B:%s' %
              (100 - (self.w_rand * 100), round(self.Arand, 2), round(self.Brand, 2)))





    def calc_eps_disc(self, A, B, N, p):
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



    def get_data_point_in_poly(self, data):
        """возвращает точки из data, лежащие в [xy1..xyn] полигоне"""
        newData = []
        for i in data:
            x, y = i[0], i[1]
            p = Point(x, y)
            if self.polygon.contains(p):
                newData.append([x, y])
        return np.array(newData)



    def generate_random_dots_in_poly(self, num_dots):
        """возвращает n случайных точкек в полигоне"""

        def random_dot(poly):
            """генерация точки в полигоне"""
            (minx, miny, maxx, maxy) = poly.bounds
            while True:
                x, y = random.uniform(minx, maxx), random.uniform(miny, maxy)
                p = Point(x, y)
                if poly.contains(p):
                    return [x, y]

        randPoints = np.empty((0, 2))
        for i in range(num_dots):
            ranXY = random_dot(self.polygon)
            randPoints = np.append(randPoints, [ranXY], axis=0)
        return randPoints

    def create_fullPoly(self, data):
        """создание полигона из границ множества"""
        xMin, xMax, yMin, yMax = min(data[:, 0]), max(data[:, 0]), min(data[:, 1]), max(data[:, 1])
        border_array = np.array([
            [xMin, yMin],
            [xMin, yMax],
            [xMax, yMax],
            [xMax, yMin],
        ])
        return border_array

    def save_points_to_txt(self, points, path, itr):
        save_path = path + 'random_eqs/'
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        for p in points:
            f = open(save_path + 'p_coord_it%i.txt' % (itr + 1), 'a')
            s = '%s %s' % (p[0], p[1])
            f.write('%s\n' % s)
            # f.close()

    def save_acc_to_txt(self, omission, path):
        f = codecs.open(path + 'omission.txt', "w", "utf-8")
        for o in omission:
            f.write(u'%s\n' % o)
        f.close()