import numpy as np
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse


def eucl_range(a, b):
    return np.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)


def evk_vector_range(i, data):
    evk_array = np.zeros((1, len(data)))
    for n, d in enumerate(i):
        evk_array += (d - data[:, n]) ** 2
    evk_array = np.sqrt(evk_array[0])
    return evk_array

class EllipceTest():
    def __init__(self, a, b, coord):
        self.a = a/2
        self.b = b/2
        self.elli_centr_coord = coord


    def check_dots_in_elli(self, a, f1, f2, dots):
        const = a*2
        l = evk_vector_range(f1, dots) + evk_vector_range(f2, dots)
        elli_dots = dots[np.where(l <= const)]

        """evk_array = np.zeros((1, len(elli_dots)))
        for d, i in enumerate(xy):
            evk_array += (i - elli_dots[:, d]) ** 2
        evk_array = np.sqrt(evk_array[0])
        evk_array = evk_array[np.where(evk_array <= a*2)]
        PxI = np.sum(np.subtract(1.0, np.true_divide(evk_array, a*2)))"""

        return elli_dots


    def calc_focus_elli(self, a, b, centr):
        c = np.sqrt(a**2-b**2)
        return [centr[0]-c, centr[1]], [centr[0]+c, centr[1]]

    def rotate_focus_elli(self, f1, f2, angle, centr):
        f_rotated = []

        for f in [f1, f2]:
            X = centr[0] + (f[0]-centr[0]) * np.cos(np.deg2rad(angle)) - (f[1]-centr[1]) * np.sin(np.deg2rad(angle))
            Y = centr[1] + (f[1]-centr[1]) * np.cos(np.deg2rad(angle)) - (f[0]-centr[0]) * np.sin(np.deg2rad(angle))
            f_rotated.append([X, Y])

        return f_rotated[0], f_rotated[1]



    def draw_ellipce(self, angles, xy):
        fig = plt.figure(0)
        ax = fig.add_subplot(111, aspect='equal')

        ax.scatter(self.elli_centr_coord[0], self.elli_centr_coord[1], color='m', zorder=0)

        e = Ellipse(xy=xy, width=self.a*2, height=self.b*2, angle=-1*angles, alpha=0.2)
        ax.add_artist(e)
        e.set_clip_box(ax.bbox)
        e.set_facecolor(np.random.rand(3))
        f1, f2 = self.calc_focus_elli(self.a, self.b, self.elli_centr_coord)
        f1_rot, f2_rot = self.rotate_focus_elli(f1, f2, angles, self.elli_centr_coord)



        dots = (np.random.rand(100000, 2)*2-1)*100
        #dots = (np.random.rand(50000, 2))*100

        evk_array = np.zeros((1, len(dots)))
        for d, i in enumerate(xy):
            evk_array += (i - dots[:, d]) ** 2
        evk_array = np.sqrt(evk_array[0])
        a_idx = np.where(evk_array <= (self.a * 2))[0]

        A = self.check_dots_in_elli(self.a, f1_rot, f2_rot, dots[a_idx])

        ax.scatter(dots[:, 0], dots[:, 1], color='k', zorder=1, s=3, lw=0)

        ax.scatter(A[:, 0], A[:, 1], color='g', zorder=0, s=5)

        ax.scatter(f1_rot[0], f1_rot[1], color='r', zorder=0)
        ax.scatter(f2_rot[0], f2_rot[1], color='r', zorder=0)


        #ax.set_xlim(50, 100,)
        #ax.set_ylim(49, 60)

        plt.show()


#dots = np.random.rand(10, 2)


angles = 15
coord= [-50, 50]
ellipse = EllipceTest(a=15, b=6, coord=coord)

#print(ellipse.calc_dot_alpha_angle(dots[0]))
ellipse.draw_ellipce(angles, coord)


