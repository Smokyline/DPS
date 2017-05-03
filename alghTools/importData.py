import os
import numpy as np
from alghTools.tools import read_csv



class ImportData:
    def __init__(self, zone='', main_mag='', mag_array=['5,5', '5,75', '6']):
        res_dir = '/Users/Ivan/Documents/workspace/resources/csv/geop/%s/' % (zone)


        self.data_dps = read_csv(res_dir + '%s_DPS_%s.csv' % (zone, main_mag), col=['x', 'y']).T


        self.mag_str = mag_array
        self.mag_type = ['instr']

        self.eqs = []
        eqs_istor = []

        for mag in self.mag_str:

            eq_instr = read_csv(res_dir + '%s_%sinstr.csv' % (zone, mag), ['x', 'y']).T
            self.eqs.append(eq_instr)
            try:
                eq_istor = read_csv(res_dir + '%s_%sistor.csv' % (zone, mag), ['x', 'y']).T
                eqs_istor.append(eq_istor)
            except:
                pass
        if len(eq_istor) > 0:
            self.mag_type.append('istor')
            self.eqs.extend(eqs_istor)



    def get_eq_stack(self):
        eq_labels = ['M%s%s' % (mag, tp) for tp in self.mag_type for mag in self.mag_str]
        return self.eqs, eq_labels

    def read_dps_res(self, zone='', mod = '', q=''):
        self.DPS_dir = '/Users/Ivan/Documents/workspace/result/%s/%s/q=%s/' % (zone, mod, q)
        dps_A = read_csv(self.DPS_dir + 'coord_q=%s_final.csv' % q, col=['DPSx', 'DPSy']).T
        return dps_A


