from alghTools.tools import read_csv, visual_2d, visual_3d_data, toDesc
import numpy as np
import math

data = read_csv('/Users/Ivan/Documents/workspace/resources/csv/geop/kmch/kmch_dps.csv').T
dataDep = read_csv('/Users/Ivan/Documents/workspace/resources/csv/geop/kmch/kmch_depth.csv', col=['d'])[0]
print(max(dataDep))
data = toDesc(data)
#depth_zero_idx = np.where(dataDep == 0)[0]
#print(len(data[depth_zero_idx]))
#visual_2d(data[depth_zero_idx])
#data = np.delete(data, depth_zero_idx, 0)
#dataDep = np.delete(dataDep, depth_zero_idx)


newData = np.empty((0, 3))


for i, xyz in enumerate(data):
        if dataDep[i] != 0:
            newData = np.append(newData, [[xyz[0], xyz[1], xyz[2] - dataDep[i]]], axis=0)

#visual_3d_data(newData, 'depth0')
