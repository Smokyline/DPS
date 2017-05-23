import numpy as np
from alghTools.tools import read_csv
from alghTools.importData import ImportData
from alghTools.drawData import visual_data


path = '/Users/Ivan/Documents/workspace/result/baikal/baikal_it4_Mc2.7_I/q=-2.25/'
dps_A = read_csv(path+'coord_q=-2.25_final.csv', ['DPSx', 'DPSy']).T
dps_B = read_csv(path+'coord_q=-2.25_final.csv', ['Bx', 'By']).T


region_name = 'baikal'

imp = ImportData(region_name, main_mag='q', mag_array=['5,5', '5,75', '6'])
sample_eq, eq_labels = imp.get_eq_stack()


visual_data(dps_A, dps_B, 'dps res I', False, path, eqs=sample_eq, labels=eq_labels,
            origData_name=region_name + '2,7')
