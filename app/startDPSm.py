import os
import time


from dpsCore.core import dps_clust
from dpsModif.tau_runner import t_runner
from dpsModif.tau_runner_mp import t_runner_mp
from alghTools.tools import *
from alghTools.drawData import visual_eq_DPS
from alghTools.importData import ImportData


def runDPSm_qIteration(desc_data, sph_data, save_path, epochs, Q, sample_eq, multiprocess):

    dim_data = desc_data
    twoDcoord = sph_data

    if len(Q) == 1:
        q_dir = '%s/q=%s/' % (save_path, Q[0])

    else:
        q_dir = '%s/q=[%s; %s]/' % (save_path, max(Q), min(Q))


    if not os.path.exists(q_dir):
        os.makedirs(q_dir)

    iter = 1
    idxX = np.arange(len(dim_data)).astype(int)
    idx_Aclust = np.array([]).astype(int)
    while True:
        print('\nQ=%s' % Q)

        #beta, q = t_runner(dim_data[idxX], Q, beta_array)
        beta, q = t_runner_mp(dim_data[idxX], Q, beta_array)


        dps_set = dps_clust(dim_data[idxX], beta, q, r=None)
        Ax, Bx = idxX[dps_set[0]], idxX[dps_set[1]]
        Ait_coord = twoDcoord[Ax]
        Bit_coord = twoDcoord[Bx]

        idx_Aclust = np.append(idx_Aclust, Ax)
        #TODO запись результата в txt

        title = 'it={}; q={}, r={}; b={}'.format(iter, q, round(dps_set[3], 4), beta)

        visual_eq_DPS(twoDcoord[idx_Aclust], Bit_coord, title, False, q_dir, eqs=sample_eq, labels=eq_labels, origData_name=region_name + mc_mag)

        save_DPS_coord(Ait_coord, Bit_coord, path=q_dir, title='coord_it' + str(iter))

        idxX = Bx

        iter += 1
        if iter > epochs or len(Bx) == 0:
            save_DPS_coord(twoDcoord[idx_Aclust], twoDcoord[idxX], path=q_dir, title='coord_q=%s_final' % q)
            break

workspace_path = os.path.expanduser('~' + os.getenv("USER") + '/Documents/workspace/')
region_name = 'baikal'
mc_mag = '2.7'

imp = ImportData(region_name, main_mag=mc_mag.replace('.', ','), mag_array=['5,5', '5,75', '6'])
#imp = ImportData(region_name, main_mag=None, mag_array=['5,5', '5,75', '6'])
eqs, eq_labels = imp.get_eq_stack()

desc_data = imp.data_dps
#desc_data = imp.read_dps_res('baikal', mod='baikal_it4_Mc2.8_I', q='-2.5')

print(len(desc_data), 'data size')


sph_data = desc_data.copy()
desc_data = toDesc(desc_data)


Q = [-2.25]
#Q = np.arange(-2., -3.1, -0.1)


beta_array = np.arange(-1, 1.1, 0.1).round(2)
epochs = 4
save_path = workspace_path+'result/%s/%s_it%s_Mc%s/' % (region_name, region_name, epochs, mc_mag)


time_start = int(round(time.time() * 1000))
runDPSm_qIteration(desc_data, sph_data, save_path=save_path, epochs=epochs, Q=Q, sample_eq=eqs, multiprocess=True)  # betaType: find, read, inp
finishTime = int(round(time.time() * 1000)) - time_start
print(time.strftime("\n\ntotal time\n%H:%M:%S", time.gmtime(int(finishTime / 1000))))
