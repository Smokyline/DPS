import numpy as np
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse


def eucl_range(a, b):
    return np.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

class EllipceTest():
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.elli_centr_coord = [0, 0]


    def check_dots_in_elli(self, a, f1, f2, dots):
        acc_dots = []
        miss_dots = []
        const = a
        for dot in dots:
            l = eucl_range(f1,dot) + eucl_range(f2,dot)
            #print(l)
            if l > const:
                miss_dots.append(dot)
            else:
                acc_dots.append(dot)
        return np.array(acc_dots), np.array(miss_dots)


    def calc_focus_elli(self, a, b, centr):
        c = np.sqrt(a**2-b**2)/2
        print([centr[0]-c, centr[1]], [centr[0]+c, centr[1]])
        return [centr[0]-c, centr[1]], [centr[0]+c, centr[1]]

    def rotate_focus_elli(self, f1, f2, angle):
        rotate_matrix = [[np.cos(np.deg2rad(angle)), -1 * np.sin(np.deg2rad(angle))],
                         [np.sin(np.deg2rad(angle)), np.cos(np.deg2rad(angle))]]
        f_rotated = []
        for f in [f1, f2]:
            r = np.dot(f, rotate_matrix)
            f_rotated.append(r)
        print(f_rotated[0], f_rotated[1])
        return f_rotated[0], f_rotated[1]



    def draw_ellipce(self, angles):
        fig = plt.figure(0)
        ax = fig.add_subplot(111, aspect='equal')

        elli = [Ellipse(xy=[0, 0], width=self.a, height=self.b, angle=angles[1], alpha=0.2)
                ]
        ax.scatter(self.elli_centr_coord[0], self.elli_centr_coord[1], color='m', zorder=0)
        for i, e in enumerate(elli):
            ax.add_artist(e)
            e.set_clip_box(ax.bbox)
            e.set_facecolor(np.random.rand(3))
            f1, f2 = self.calc_focus_elli(self.a, self.b, self.elli_centr_coord)
            f1_rot, f2_rot = self.rotate_focus_elli(f1, f2, -1*angles[1])

            ax.scatter(f1_rot[0], f1_rot[1], color='r', zorder=0)
            ax.scatter(f2_rot[0], f2_rot[1], color='r', zorder=0)

            dots = (np.random.rand(100000, 2)*2-1)*10
            A, B = self.check_dots_in_elli(self.a, f1_rot, f2_rot, dots)

            ax.scatter(A[:, 0], A[:, 1], color='g', zorder=0, s=5)
            ax.scatter(B[:, 0], B[:, 1], color='k', zorder=0, s=5)




        ax.set_xlim(-7, 7)
        ax.set_ylim(-7, 7)

        plt.show()


#dots = np.random.rand(10, 2)


angles = [0, 360]
ellipse = EllipceTest(a=7, b=1)

#print(ellipse.calc_dot_alpha_angle(dots[0]))
ellipse.draw_ellipce(angles)


