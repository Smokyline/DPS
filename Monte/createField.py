import numpy as np
import random
from shapely.geometry import Polygon, Point


def get_random_point_in_polygon(poly):
    """генерация точки в полигоне"""
    (minx, miny, maxx, maxy) = poly.bounds
    while True:
        x, y = random.uniform(minx, maxx), random.uniform(miny, maxy)
        p = Point(x, y)
        if poly.contains(p):
            return [x, y]


def check_data_point_in_poly(xy, data):
    """возвращает точки из data, лежащие в [xy1..xyn] полигоне"""
    newData = []
    poly = Polygon(xy)
    for i in data:
        x, y = i[0], i[1]
        p = Point(x, y)
        if poly.contains(p):
            newData.append([x, y])
    return np.array(newData)


def random_dots(p, num_dots):
    """генерация num_d случайных точек в p полигоне """
    ran = np.empty((0, 2))
    for i in range(num_dots):
        ranXY = get_random_point_in_polygon(p)
        ran = np.append(ran, [ranXY], axis=0)
    return ran


def inputPoly(xy, num_dots):
    """возвращает случайные точки в полигоне"""
    p = Polygon(xy)
    randPoints = random_dots(p, num_dots)
    return randPoints


def create_fullPoly(data):
    """создание полигона из границ множества"""
    xMin, xMax, yMin, yMax = min(data[:, 0]), max(data[:, 0]), min(data[:, 1]), max(data[:, 1])
    border_array = np.array([
        [xMin, yMin],
        [xMin, yMax],
        [xMax, yMax],
        [xMax, yMin],
    ])
    return border_array


def create_customPoly(coord):
    return np.asarray(coord)
