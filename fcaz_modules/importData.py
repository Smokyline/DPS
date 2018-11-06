import os
import numpy as np
from fcaz_modules.tools import read_csv



class ImportData():
    def __init__(self, zone='', main_mag='', mag_array=['5,5', '5,75', '6']):
        self.workspace_path = os.path.expanduser('~' + os.getenv("USER") + '/Documents/workspace/')

        res_dir = self.workspace_path+'resources/csv/GEO/%s/' % (zone)


        try:
            self.data_to_dps = read_csv(res_dir + '%s_DPS_%s.csv' % (zone, main_mag))
        except Exception as e:
            print(e)
            print('dps import fail')


        self.mag_str = mag_array

        self.eqs = []
        self.eq_labels = []

        for mag in self.mag_str:

            try:
                eq_istor = read_csv(res_dir + '%s_%sistor.csv' % (zone, mag))
                # eqs_istor.append(eq_istor)
                self.eqs.append(eq_istor)
                self.eq_labels.append('M%s%s' % (mag, 'istor'))
                print('eq M%s%s add count:%i' % (mag, 'istor', len(eq_istor)))


            except:
                pass

            try:
                eq_instr = read_csv(res_dir + '%s_%sinstr.csv' % (zone, mag))
                self.eqs.append(eq_instr)
                self.eq_labels.append('M%s%s' % (mag, 'instr'))
                print('eq M%s%s add count:%i' % (mag, 'instr', len(eq_instr)))
            except:
                pass




    def get_eq_stack(self):

        return self.eqs, self.eq_labels

    def read_dps_res(self, zone='', mod = '', q='', iter=1):
        self.DPS_dir = self.workspace_path+'result/DPS/%s/%s/q=%s/' % (zone, mod, q)
        dps_A = np.empty((0, 2))
        for i in range(1, iter+1):
            print(i)
            i_dps = read_csv(self.DPS_dir + 'coord_it%i.csv' % (i))[:, :2]
            i_dps = i_dps[np.logical_not(np.isnan(i_dps))]
            i_dps = np.reshape(i_dps, (-1, 2))
            dps_A = np.append(dps_A, i_dps, axis=0)
        return dps_A


