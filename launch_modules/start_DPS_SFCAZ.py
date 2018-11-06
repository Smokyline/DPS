import os
import time

from fcaz_modules.drawData import visual_FCAZ
from fcaz_modules.importData import ImportData
from fcaz_modules.tools import *
from main.dps_core import dps_clustering
from main.tau_runner_mp import t_runner_mp


def runDPSm_qIteration(desc_data, sph_data, save_path, epochs, Q, sample_eq):

    dim_data = desc_data
    twoDcoord = sph_data

    if len(Q) == 1:
        q_dir = '%s/q=%s/' % (save_path, Q[0])

    else:
        q_dir = '%s/q=[%s; %s]/' % (save_path, max(Q), min(Q))

    if not os.path.exists(q_dir):
        os.makedirs(q_dir, exist_ok=True)


    iter = 1
    idxX = np.arange(len(dim_data)).astype(int)
    idx_Aclust = np.array([]).astype(int)
    while True:
        print('\nQ=%s' % Q)

        #beta, q = t_runner(dim_data[idxX], Q, beta_array)
        beta, q = t_runner_mp(dim_data[idxX], Q, beta_array)


        dps_set = dps_clustering(dim_data[idxX], beta, q, r=None)
        Ax, Bx = idxX[dps_set[0]], idxX[dps_set[1]]
        Ait_coord = twoDcoord[Ax]
        Bit_coord = twoDcoord[Bx]

        idx_Aclust = np.append(idx_Aclust, Ax)

        title = 'it={}; q={}, r={}; b={}'.format(iter, q, round(dps_set[3], 4), beta)

        visual_FCAZ(Bit_coord,twoDcoord[idx_Aclust],  EXT=None,
                    eqs=sample_eq, eqs_labels=eq_labels, title=title, path=q_dir)

        save_DPS_coord(Ait_coord, Bit_coord, path=q_dir, title='coord_it' + str(iter))

        idxX = Bx

        iter += 1
        if iter > epochs or len(Bx) == 0:
            print('final DPS cluster count: %s' % len(idx_Aclust))
            save_DPS_coord(twoDcoord[idx_Aclust], twoDcoord[idxX], path=q_dir, title='coord_q=%s_final' % q)
            break



original_umask = os.umask(0)
workspace_path = os.path.expanduser('~' + os.getenv("USER") + '/Documents/workspace/')
region_name = 'kmch'
mc_mag = '3.5'
epochs = 5
# COORD MAP!!!

Q = [-2.75]
load_q = '-2.75'
#Q = np.arange(-1.7, -3.1, -0.1)


load_k_iter = 'I'
target_iter = 2

save_k_iter = 'II'


imp = ImportData(region_name, main_mag=mc_mag.replace('.', ','), mag_array=['7', '7,5', '8'])
eqs, eq_labels = imp.get_eq_stack()

# DPS set
desc_data = imp.data_to_dps
#desc_data = imp.read_dps_res(zone=region_name, mod='%s_%s' % (region_name, load_k_iter), q=load_q, iter=target_iter)





print(len(desc_data), 'data size')
sph_data = desc_data.copy()
desc_data = toDesc(desc_data)

beta_array = np.arange(-1, 1.05, 0.1).round(2)
save_path = workspace_path+'result/DPS/%s/%s_%s/' % (region_name, region_name, save_k_iter)


time_start = int(round(time.time() * 1000))
runDPSm_qIteration(desc_data, sph_data, save_path=save_path, epochs=epochs, Q=Q, sample_eq=eqs)  # betaType: find, read, inp
finishTime = int(round(time.time() * 1000)) - time_start
print(time.strftime("\n\ntotal time\n%H:%M:%S", time.gmtime(int(finishTime / 1000))))

os.umask(original_umask)
