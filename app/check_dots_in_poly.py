from alghTools.tools import read_csv
from shapely.geometry import Polygon, Point
import numpy as np
import os


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

workspace_path = os.path.expanduser('~' + os.getenv("USER") + '/Documents/workspace/')
data = read_csv(workspace_path+'resources/csv/geop/altaiSay/altaiSay_3,5.csv').T




#coordPoly = [[32.5, 43], [32.5, 45.2], [44.5, 45.2], [42, 41.5], [41, 41.5], [39, 43]]  # kvz crm
coordPoly = [[84, 47], [84, 53], [101, 53], [101, 48.5], [91.5, 48.5], [91.5, 45.5], [89, 45.5], [89, 47]]

p_data = check_data_point_in_poly(coordPoly, data)
print(len(p_data))