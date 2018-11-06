from dps_ellipce.dps_elli_core import DPSEllipce

from fcaz_modules.drawData import visual_FCAZ
from fcaz_modules.importData import ImportData
from fcaz_modules.tools import *
from main.tau_runner_mp import t_runner_mp
import os
import time

original_umask = os.umask(0)
workspace_path = os.path.expanduser('~' + os.getenv("USER") + '/Documents/workspace/')
region_name = 'kmch'
mc_mag = '3.5'

imp = ImportData(region_name, main_mag=mc_mag.replace('.', ','), mag_array=['7', '7,5', '8'])
eqs, eq_labels = imp.get_eq_stack()
save_path = workspace_path + 'result/DPS/%s/%s_elli/' % (region_name, region_name)

# COORD MAP!!!

# DPS set
desc_data = imp.data_to_dps


beta_array = np.arange(-0.7, 0.5, 0.1).round(2)

time_start = int(round(time.time() * 1000))
for beta in beta_array:
    a = 0.5
    b = 0.1
    angle_tick = 1

    dpse = DPSEllipce(data=desc_data, beta=beta, a=a, b=b, angle_tick=angle_tick)
    dps_set = dpse.clustering()
    A, B, Px, alpha, p_max = dps_set

    save_path = workspace_path + 'result/DPS/%s/%s_elli/beta=%s/' % (region_name, region_name, beta)
    title = 'beta=%s |B|=%s |H|=%s alpha=%s p=%s' % (beta, len(A), len(B), alpha, p_max)

    if not os.path.exists(save_path):
        os.makedirs(save_path, exist_ok=True)
    save_DPS_coord(desc_data[A], desc_data[B], path=save_path, title=title)
    save_p(Px, save_path, title)

    visual_FCAZ(desc_data[B], desc_data[A], EXT=None,
                eqs=eqs, eqs_labels=eq_labels, title=title, path=save_path)


finishTime = int(round(time.time() * 1000)) - time_start
print(time.strftime("\n\ntotal time\n%H:%M:%S", time.gmtime(int(finishTime / 1000))))

os.umask(original_umask)
