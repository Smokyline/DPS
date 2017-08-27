import numpy as np
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse


def eucl_range(a, b):
    return np.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

class EllipceTest():
    def __init__(self, a, b, angle):
        self.a = a
        self.b = b
        self.angle = angle
        self.elli_coord = [0, 0]


    def calc_radius_ellipse(self, psi):
        out = (self.a*self.b)/(
            np.sqrt(self.b**2 * np.cos(np.deg2rad(psi))**2 + self.a**2 * np.sin(np.deg2rad(psi))**2))
        return out

    def calc_dot_alpha_angle(self, dot):
        c = eucl_range(self.elli_coord, dot)
        a = eucl_range(self.elli_coord, [self.elli_coord[0], dot[1]])
        b = eucl_range([self.elli_coord[0], dot[1]], dot)

        sinA = np.cos(a/c)
        return np.rad2deg(sinA)



    def draw_ellipce(self, dots):
        fig = plt.figure(0)
        ax = fig.add_subplot(111, aspect='equal')

        elli = Ellipse(xy=[0, 0], width=self.a, height=self.b, angle=self.angle,
                       facecolor=None, edgecolor='green', zorder=1, alpha=0.1)
        ax.add_artist(elli)
        #elli.set_clip_box(ax.bbox)

        for d in dots:
            ax.scatter(d[0], d[1], color='r', zorder=0)

        ax.scatter(self.elli_coord[0], self.elli_coord[1], color='m', zorder=0)
        ax.set_xlim(-7, 7)
        ax.set_ylim(-7, 7)
        plt.show()


#dots = np.random.rand(10, 2)
dots = np.array([[4, -1]])



ellipse = EllipceTest(a=7, b=4, angle=0)

print(ellipse.calc_dot_alpha_angle(dots[0]))
ellipse.draw_ellipce(dots)


