import numpy as np
import multiprocessing as mp



def calc_a(Pxa, beta):
    min_x = 0.0
    max_x = 1.0
    epsl = 0.000000000006

    Pxa = Pxa[np.where(Pxa>0)]

    def foo(B, a, beta):
        EPx = []
        for b in B:
            EPx.append((a - b) / max(a, b))
        return np.mean(EPx) - beta

    def foo_max(Pxa, max_x):
        x = max_x
        while True:
            zn = foo(Pxa, x, 0)
            if zn < beta:
                x *= 2
            else:
                return x
    max_x = foo_max(Pxa, max_x)

    while True:
        half_x = (max_x + min_x) / 2
        fA_min = foo(Pxa, min_x, beta)
        fA_max = foo(Pxa, max_x, beta)
        fA_half = foo(Pxa, half_x, beta)

        if fA_min == 0:
            alpha = min_x
            break
        if fA_half == 0:
            alpha = half_x
            break
        if fA_max == 0:
            alpha = max_x
            break

        if fA_min * fA_half < 0:
            max_x = half_x
        else:
            min_x = half_x

        if max_x - min_x < epsl:
            alpha = half_x
            break
    print('alpha:%f' % alpha)
    return alpha


def eucl_range(a, b):
    return np.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)


def evk_vector_range(i, data):
    evk_array = np.zeros((1, len(data)))
    for n, d in enumerate(i):
        evk_array += (d - data[:, n]) ** 2
    evk_array = np.sqrt(evk_array[0])
    return evk_array


def check_dots_in_elli(que, xy,  a, f1, f2, dots):
    l = evk_vector_range(f1, dots) + evk_vector_range(f2, dots)
    elli_dots = dots[np.where(l <= a*2)]

    """evk_array = np.zeros((1, len(elli_dots)))
    for d, i in enumerate(xy):
        evk_array += (i - elli_dots[:, d]) ** 2
    evk_array = np.sqrt(evk_array[0])
    evk_array = evk_array[np.where(evk_array <= a*2)]
    PxI = np.sum(np.subtract(1.0, np.true_divide(evk_array, a*2)))"""

    return que.put(len(elli_dots))
    #return que.put(PxI)

"""
def calc_p(ellipses, full_dots, p_max):
    p_out_array = []
    angles_out_array = []
    for j, elli in enumerate(ellipses):
        x, y, a, b, angles_array, f1_array, f2_array = [v for v in elli]

        # точки в горизонтальном диаметре эллипса
        evk_array = np.zeros((1, len(full_dots)))
        for d, i in enumerate([x, y]):
            evk_array += (i - full_dots[:, d]) ** 2
        evk_array = np.sqrt(evk_array[0])
        a_idx = np.where(evk_array <= (a*2))[0]

        angles_p = np.array([])

        # mp cycle
        for f_idx_start in range(0, len(f1_array), 8):
            core_f1_array = f1_array[f_idx_start:f_idx_start+8]
            core_f2_array = f2_array[f_idx_start:f_idx_start+8]
            core_que = []
            for k in range(len(core_f1_array)):
                #
                qe = mp.Queue()
                p = mp.Process(target=check_dots_in_elli,
                               args=(qe, [x, y], a, core_f1_array[k], core_f2_array[k], full_dots[a_idx]))
                core_que.append(qe)
                p.start()
                #
            angles_p = np.append(angles_p, [qe.get() for qe in core_que])


        # плотность - кол-во точек в эллипсе
        max_idx = np.argmax(angles_p)
        p_out_array.append(angles_p[max_idx])
        angles_out_array.append(angles_array[max_idx])
    if p_max is None:
        p_max = np.max(p_out_array)
        #Pxa = np.true_divide(p_out_array, p_max)
        Pxa = np.array(p_out_array)
        return Pxa, angles_out_array, p_max
    else:
        #Pxa = np.true_divide(p_out_array, p_max)
        Pxa = np.array(p_out_array)
        return Pxa, angles_out_array
"""


def calc_rotate_ellipse(qe, elli, full_dots):
    x, y, a, b, angles_array, f1_array, f2_array = [v for v in elli]

    # точки в горизонтальном диаметре эллипса
    evk_array = np.zeros((1, len(full_dots)))
    for d, i in enumerate([x, y]):
        evk_array += (i - full_dots[:, d]) ** 2
    evk_array = np.sqrt(evk_array[0])
    a_idx = np.where(evk_array <= (a * 2))[0]
    radius_dots = full_dots[a_idx]

    angles_p = []
    # check p for all angles
    for k in range(len(f1_array)):
        l = evk_vector_range(f1_array[k], radius_dots) + evk_vector_range(f2_array[k], radius_dots)
        angles_p.append(len(np.where(l <= a * 2)[0]))

    # плотность - кол-во точек в эллипсе
    max_idx = np.argmax(angles_p)

    return qe.put([angles_p[max_idx], angles_array[max_idx]])

def calc_p(ellipses, full_dots, p_max):
    out_array = np.empty((0, 2))  # p and angles



    #  mp elli
    for e_start in range(0, len(ellipses), 8):
        core_ellipses = ellipses[e_start:e_start+8]
        core_que = []

        for c_elli in core_ellipses:
            qe = mp.Queue()
            p = mp.Process(target=calc_rotate_ellipse,
                           args=(qe, c_elli, full_dots))
            core_que.append(qe)
            p.start()
        core_que = [qe.get() for qe in core_que]
        for c_elli in core_que:
            out_array = np.append(out_array, [c_elli], axis=0)

    if p_max is None:
        p_max = np.max(out_array[:, 0])
        #Pxa = np.true_divide(p_out_array, p_max)
        Pxa = np.array(out_array[:, 0])
        return Pxa, out_array[:, 1], p_max
    else:
        #Pxa = np.true_divide(p_out_array, p_max)
        Pxa = np.array(out_array[:, 0])
        return Pxa, out_array[:, 1]




def searchAlphaIndex(Pxa, alpha):
    Aindex = np.where(Pxa >= alpha)[0]
    Bindex = np.where(Pxa < alpha)[0]
    return Aindex, Bindex


def elli_dps_clust(ellipses, full_data, beta):

    p_max = None
    Pxa, angles_array, p_max = calc_p(ellipses=ellipses, full_dots=full_data, p_max=p_max)
    #print(Pxa)
    #alpha = calc_a(Pxa, beta)

    #Aindex, Bindex = searchAlphaIndex(Pxa, alpha)
    #A_idx = np.where(Pxa >= beta)[0]


    out_ellipses = []
    angles_out_array = []
    for n, elli in enumerate(ellipses):
        #if n in A_idx:
        #if n in Aindex:
            out_ellipses.append(elli)
            angles_out_array.append(angles_array[n])
    #return out_ellipses, angles_out_array
    return Pxa, angles_array
