import numpy as np
from itertools import product


def calc_focus_elli(a, b, centr):
    c = np.sqrt((a) ** 2 - (b) ** 2)
    return [centr[0]-c, centr[1]], [centr[0]+c, centr[1]]

def rotate_focus_elli(f1, f2, angle, centr):
    f_rotated = []
    for f in [f1, f2]:
        X = centr[0] + (f[0] - centr[0]) * np.cos(np.deg2rad(angle)) - (f[1] - centr[1]) * np.sin(np.deg2rad(angle))
        Y = centr[1] + (f[1] - centr[1]) * np.cos(np.deg2rad(angle)) - (f[0] - centr[0]) * np.sin(np.deg2rad(angle))
        f_rotated.append([X, Y])
    return f_rotated[0], f_rotated[1]

def generate_ellipses(xy_limits, angle_tick, elli_lengths,):
    x_min, x_max, y_min, y_max, delta = [v for v in xy_limits]
    coordinates = list(product(np.arange(x_min, x_max, delta), np.arange(y_min, y_max, delta)))
    grid_coord = np.array(coordinates)

    angles = np.arange(0, 180, angle_tick)
    #angles = [0, 15]
    print(angles)
    a, b = [v for v in np.array(elli_lengths)/2]

    ellipses = []
    for i, xy in enumerate(grid_coord):
        x, y = xy
        ellipse = [x, y, a, b]

        f1, f2 = [], []
        f1_original, f2_original = calc_focus_elli(a, b, xy)
        for angle in angles:
            f1_rot, f2_rot = rotate_focus_elli(f1_original, f2_original, -angle, centr=xy)
            f1.append(f1_rot)
            f2.append(f2_rot)
        for value in [angles, f1, f2]:
            ellipse.append(value)
        ellipses.append(ellipse)
    return ellipses


