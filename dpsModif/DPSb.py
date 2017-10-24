import matplotlib
matplotlib.use('Qt4Agg')
import matplotlib.pyplot as plt
import numpy as np
from dpsModif.DPSold import calc_a, calc_r, dps_clust, calc_p, searchAlphaIndex
from alghTools.tools import read_csv
from alghTools.drawData import visual_dps_iter
from itertools import product
import os
import sys

def parse(data, x, y):
    newData = []
    x0, x1 = x
    y0, y1 = y
    for i in data:
        if (x0 < i[0] < x1) and (y0 < i[1] < y1):
            newData.append(i)
    return np.asarray(newData)




def visualA0inXb(X, Xb, An, A0dot, title, direct, dot=True, drGrid=True):
    xX, yX  = data[X, 0], data[X, 1]
    xXb, yXb = data[Xb, 0], data[Xb, 1]
    xAn, yAn = data[An, 0], data[An, 1]

    if A0dot is not None:
        if len(A0dot) > 1:
            xA, yA = data[A0dot, 0], data[A0dot, 1]
        else:
            xA, yA = data[A0dot[0]], data[A0dot[1]]

    def drawGrid(An):
        G = []
        for a in A0:
            if a in An:
                G.append(data[a])
        G = np.array(G)
        if len(G) == 0:
            return [], []
        else:
            return G[:, 0], G[:, 1]

    if dot:
        plt.scatter(xX, yX, marker='.', c='k', linewidths=0, s=7)
        plt.scatter(xXb, yXb, marker='.', c='b', linewidths=0, s=10)
        plt.scatter(xAn, yAn, marker='.', c='r', linewidths=0, s=13)
        plt.scatter(xA, yA, marker='p', c='g', linewidths=0.3)
    else:
        plt.scatter(xX, yX, marker='.', c='k', linewidths=0, s=7)
        plt.scatter(xAn, yAn, marker='.', c='r', linewidths=0, s=13)
        plt.scatter(xXb, yXb, marker='.', c='b', linewidths=0, s=10)

    if drGrid:
        xG, yG = drawGrid(An)
        plt.scatter(xG, yG, marker='.', c='g', linewidths=0, s=10)

    plt.grid(True)
    plt.title(title)
    plt.savefig(direct+title+'.png', dpi=450)
    #plt.show()




def compare(data, Pxa, a):
    DPS_clust = data[np.where(Pxa >= a)]
    B_clust = data[np.where(Pxa < a)]
    return np.array(DPS_clust), np.array(B_clust)


def calc_pA(A, X, r, p_max, Pq):
    array = []
    for i in X:
        evk_array = np.zeros((1, len(A)))
        for d, n in enumerate(i):
            evk_array += (n - A[:, d]) ** 2
        evk_array = np.sqrt(evk_array[0])
        evk_array = evk_array[np.where(evk_array <= r)]
        Pa_i = np.sum((np.subtract(1.0, np.true_divide(evk_array, r)))**Pq)
        array.append(Pa_i)
    P = np.true_divide(array, p_max)
    return P




def createAinXb(Xall, X, A0, r, beta, drct, dot=False, alphaOLD = False, makeDPS=False):
    PX, p_max = calc_p(data[X], r, None, Pq=1)
    print('minP:%f; maxP:%f' % (min(PX), max(PX)))
    if alphaOLD:
        #PA = calc_p(data[A0], r, p_max, Pq=1)
        alpha = calc_a(PX, beta)
    else:
        alpha = 1 / p_max

    An = []
    iterat = 1


    while True:
        if iterat == 1:
            AuAn = A0
        else:
            AuAn = np.union1d(A0, An)
            print('A U An = %i' % len(AuAn))
        if alphaOLD:
            PaX = calc_pA(data[AuAn], data[X], r, p_max=p_max, Pq=1)
        else:
            PaX = calc_pA(data[AuAn], data[X], r, p_max=1, Pq=0)
        An1, Bn = compare(X, PaX, alpha)

        if len(An) == len(An1):
            print(len(An), 'final An')

            if dot:
                title = 'b_%f alpha_%f A1_%s lenAn_%i' % (beta, alpha, str(A0), len(An1))
                visualA0inXb(Xall, X, An1, A0, title, drct, dot)
            else:
                title = 'beta_%f q_%s alpha_%f lenA_%i lenAn_%i' % (beta, str(q), alpha, len(A0), len(An1))
                visualA0inXb(Xall, A0, An1, None, title, drct, dot=False)
            break
        else:
            title = 'it:{}; An-1:{}; An:{}'.format(iterat, len(An), len(An1))
            print(title)
            if dot:
                visualA0inXb(Xall, X, An1, A0, title, drct, dot)
            else:
                title = title + ' beta:' + str(beta)
                visualA0inXb(Xall, A0, An1, None, title, drct, dot=False)
            An = An1
            iterat += 1
    if makeDPS:
        m_dps(beta, alpha, drct, An, A0)
    return An



def find_Xb(X, beta, r, q, Pq):
    set = dps_clust(data[X], beta, r, q, Pq)
    Xb = set[0]
    return Xb

def checkXinXb(Xb, A0):
    for a in A0:
        if a not in Xb:
                return False
    return True

def m_dps(beta, a, b_dir, An, A0):
    dpsSaveDir = b_dir + 'dpsCore/'
    if not os.path.exists(dpsSaveDir):
        os.makedirs(dpsSaveDir)

    p_sample = None
    updA = An
    B_data = []
    it = 1
    dps_set = []
    while True:
        if it==1:
            Pxa, p_sample = calc_p(data[updA], r, None)
        else:
            Pxa = calc_p(data[updA], r, p_sample)

        Aindex, Bindex = searchAlphaIndex(Pxa, a, None, False)
        DPS_clust, B_clust = updA[Aindex], updA[Bindex]
        B_data.extend(B_clust)
        # if np.array_equal(DPS_clust, upd_dataIndex) or len(DPS_clust) == 0:
        if len(DPS_clust) == len(updA) or len(DPS_clust) == 0:

            dps_set = [DPS_clust, B_data, q, r, beta, a, p_sample]
            break
        else:
            ttl = 'it:%i An:%i DPS:%i B:%i' % (it, len(X), len(DPS_clust), len(B_data))
            visual_dps_iter(data[DPS_clust], data, data[A0], ttl, direc=dpsSaveDir+str(it))
            updA = DPS_clust
            it += 1
    print('A:{}; B:{}'.format(len(dps_set[0]), len(dps_set[1])))
    print('dpsCore iteration:{}'.format(it))


def run(X, r, Pq, A0, dot=False, makeDPS=False, alphaOLD=False):
    if dot:

        cd_dir = '{}/{}/'.format(res_directory, A0)
        if not os.path.exists(cd_dir):
            os.makedirs(cd_dir)

        #b = [-1, -0.9, -0.8, -0.7, -0.6, -0.5, -0.4, -0.3, -0.2, -0.1, 0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
        # b = np.arange(-0.7, -0.6, 0.02)
        b = [0]
        Xb_array = {}
        lastBeta = None
        for beta in b:
            Xbi = find_Xb(X, beta, r, q, Pq)
            status_x = checkXinXb(Xbi, A0)
            if status_x == False:
                print('x not in Xb')
                break
            else:
                Xb_array = Xbi
                lastBeta = beta

        print('\nlastBeta:{}'.format(lastBeta))
        if alphaOLD:
            b = [-1, -0.9, -0.8, -0.7, -0.6, -0.5, -0.4, -0.3, -0.2, -0.1, 0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8,
                 0.9, 1]
            for beta in b:
                print('beta:%f' % beta)
                b_dir = cd_dir + '/%f/' % beta
                if not os.path.exists(b_dir):
                    os.makedirs(b_dir)
                An = createAinXb(X, Xb_array, A0, r, beta, b_dir, dot=True, alphaOLD=True)
        else:
            An = createAinXb(X, Xb_array, A0, r, lastBeta, cd_dir, dot=True, alphaOLD=False)
    else:
        cd_dir = '{}{}/'.format(res_directory, 'q:%s;%s' % (str(q), str(len(A0))))
        if not os.path.exists(cd_dir):
            os.makedirs(cd_dir)

        An = None
        if alphaOLD:
            #b = [-1, -0.9, -0.8, -0.7, -0.6, -0.5, -0.4, -0.3, -0.2, -0.1, 0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
            b = [0]
            for beta in b:
                print('beta:%f' % beta)
                b_dir = cd_dir+'/%f/' % beta
                if not os.path.exists(b_dir):
                    os.makedirs(b_dir)
                An = createAinXb(X, X, A0, r, beta, b_dir, dot=False, alphaOLD=True, makeDPS=makeDPS)

        else:
            An = createAinXb(X, X, A0, r, 0, cd_dir, dot=False, alphaOLD=False, makeDPS=makeDPS)




def update_data(data):
    eps = sys.float_info.epsilon

    def make_grid(map_size):

        coordinates = list(
            product(np.arange(map_size[0], map_size[1], map_size[4]), np.arange(map_size[2], map_size[3], map_size[4])))
        return np.array(coordinates)

    nData = data
    #A = make_grid([39.65, 51.65, 36.25, 46.25, 0.25])
    #A = make_grid([40, 52, 36, 46, 0.2])
    #A = data[:2500]
    A = read_csv(workspace_path+'resources/csv/GEO/kvz/kvz_5-7.csv').T
    A0 = np.array([]).astype(int)
    idx = len(data)

    for a in A:
        evk_array = [0 for i in range(len(data))]
        for d, n in enumerate(a):
            evk_array += (n - data[:, d]) ** 2
        evk_array = np.sqrt(evk_array)
        index = np.where(evk_array == 0)[0]
        if len(index) > 0:
            A0 = np.union1d(A0, index)
        else:
            nData = np.append(nData, [a], axis=0)
            A0 = np.append(A0, [idx])
            idx += 1
    print('len X:%i' % len(data))
    print('len A0:%i' % len(A0))
    print('len XuA0:%i' % len(nData))
    return nData, A0



workspace_path = os.path.expanduser('~' + os.getenv("USER") + '/Documents/workspace/')

SpData = read_csv(workspace_path+'resources/csv/GEO/kvz/kvz_dps3.csv').T
#data = toDesc(SpData)
data = SpData
res_directory = workspace_path+'result/'

q = -4
Pq = 1
#y = [45.5, 43.5]
#y = [45.7, 43]
#y = [44, 41]
#Y = [[42.1, 40.3], [44, 39], [44, 41.1], [43.5, 41], [46, 42], [45.5, 43], [47, 43], [48.5, 40.6], [50, 40], [43.5, 42.5]]
r = calc_r(data, q)

data, A0 = update_data(data)
X = np.arange(0, len(data))

#A0 = []



#A0 = np.array([find_near_x(X, y)])
#A0 = np.arange(0, 2500)
#A0 = parse(data, [44.4, 44.6], [38.87, 39])
#A0 =

#X = np.arange(0, len(data))



run(X, r, Pq, A0, dot=False, makeDPS=True, alphaOLD=True)


