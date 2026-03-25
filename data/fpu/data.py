# FPU数据配置


import numpy as np
from matplotlib import pyplot as plt
from pathos.multiprocessing import ProcessingPool as newPool
import config


def test_bz(bzzs, bzxls, V):
    print("测试")
    bzz = bzzs[0]
    bzxl = bzxls[0]
    test_ = (bzz * bzxl) - np.dot(bzxl, V)
    print(test_)

    # 通过投影，也可以查看是否对
    # ty_xst(xst[0, :], bzxls, False)
    # ty_xst(bzxls[2], bzxls, False)

    if (sum(test_) < 10**-8):
        print("本征值没问题")


def plot_n(xst, vst, n_see=16):

    legends = []
    plt.ylim(-1.5, 1.5)
    for i in [0]:
        s = "-."
        if (i == 0):
            s = "-"
        plt.plot(xst[:, n_see + i], s)
        # plt.plot(vst[:, n_see + i], s)
        legends.append("n=%d" % (n_see + i))

    plt.legend(legends)

    # plt.plot(vst[:, 1])
    plt.savefig(config.path_img_nt)
    plt.savefig(config.path_img_nt + ".pdf")

    # plt.show()
    plt.close()


def plot_t(xst, jump=100):
    for xs in xst[::jump]:
        plt.plot(xs)
    plt.savefig(config.path_img_xst)
    plt.savefig(config.path_img_xst + ".pdf")

    plt.close()

    # plt.show()


def get_Ets(xst, vst, bzzs, bzxls, m=1):

    bzxls = np.transpose(bzxls)

    xst_ = np.dot(xst, bzxls)
    vst_ = np.dot(vst, bzxls)

    Ets = m * vst_**2 / 2 + m * xst_**2 * np.abs(bzzs) / 2

    np.save(config.path_np_ets, Ets)
    test_eok(Ets)

    return Ets


def ty_xst(tys, bzxls, log=True):
    plt.figure()
    if (log):
        plt.axes(yscale="log")
    print(tys)
    ys = np.dot(tys, np.transpose(bzxls))
    plt.scatter(np.linspace(1, len(tys), len(tys)), ys)
    plt.savefig(config.path_img_ty_xst)
    plt.savefig(config.path_img_ty_xst + ".pdf")

    plt.close()


def plot_ek(Ets, t=1, onlyOdd=True, log=True):
    es = Ets[t, :]
    N = len(es)

    xs = np.linspace(1, N, N)

    if (onlyOdd):
        es = es[::2]
        xs = xs[::2]

    print(xs)

    plt.figure()
    if (log):
        plt.axes(yscale="log")
    plt.scatter(xs, es)
    for i in range(len(es)):
        plt.annotate(str(int(xs[i])), xy=(xs[i], es[i]), xytext=(xs[i], es[i]))
    plt.savefig(config.path_img_eks)
    plt.savefig(config.path_img_eks + ".pdf")

    plt.close()


def test_eok(Ets):
    plt.figure()
    et = np.sum(Ets, axis=1)
    plt.ylim(0, max(et) * 1.2)
    plt.plot(et)
    plt.savefig(config.path_img_eok)
    plt.savefig(config.path_img_eok + ".pdf")
    plt.close()


def plot_et(Es, ks=[0, 1, 2, 3, 4, 5], log=False):

    Es = np.array(Es)

    print(np.shape(Es))

    plt.figure()
    if (log):
        plt.axes(yscale="log")

    Es_ = []
    legend = []

    for k in ks:
        k = k
        print(k)
        legend.append(k)
        Es_.append(Es[:, k])

    # 归一化
    # Es_ = Es_ / Es[:, 0]

    ts = np.arange(len(Es[:, 0])) * config.dt

    for j in range(len(ks)):
        y = Es_[j]
        plt.plot(ts, y)

    plt.legend(legend)
    # plt.savefig("%s/imgs/cals/cal%d_ty.png" % (path_run, cal))
    plt.savefig(config.path_img_ets)
    plt.savefig(config.path_img_ets + ".pdf")

    plt.close()
    print(config.path_img_ets)
    # plt.show()


# 第k个模式，从1开始，j原子数从0开始到32
def plt_bz(k, bzxl, bzz):
    N = len(bzxls)

    x = np.linspace(1, N, N)
    print(x)
    js = np.linspace(0, N, N + 1)
    print(js)

    file = config.path_img_bzn % k
    plt.scatter(x, bzxl)

    plt.plot((2 / (N + 1))**0.5 * np.sin(np.pi * k * js / (N + 1)))

    title = "%d=%f" % (k, bzz)
    plt.title(title)
    print(title)

    plt.savefig(file)
    plt.savefig(file+".pdf")
    plt.close()


def plt_bzs(bzzs, bzxls):
    file = config.path_img_bz
    plt.plot(bzzs)
    plt.savefig(file)
    plt.savefig(file+".pdf")
    plt.close()

    pool = newPool()
    N = len(bzzs)
    pool.map(plt_bz, np.linspace(1, N, N), bzxls, bzzs)
    pool.close()
    pool.join()


# file_add = "_alpha"
# log = False
model = config.model

file_add = "_" + model
log = False
# file_add = ""
# N = 32
step_start = 0
steps = 1000000

xst = np.load(config.path_np_xst)[step_start:step_start +
                                                 steps, :]
vst = np.load(config.path_np_vst)[step_start:step_start +
                                                 steps, :]
print(np.shape(xst))
bzzs = np.load(config.path_np_bzzs)
bzxls = np.load(config.path_np_bzxls)
V = np.load(config.path_np_vs)

test_bz(bzzs, bzxls, V)
# plt_bzs(bzzs, bzxls)

# plot_t(xst[0:20000], jump=100)
plot_n(xst, vst, 15)

Ets = get_Ets(xst, vst, bzzs, bzxls, config.m)
print(np.shape(Ets))
plot_et(Ets, log=log, ks=config.ks)

# 25，26，27
# 11
# 12
# 14
plot_ek(Ets, 100000-1, log=True)

# ty_xst(xst[0, :], bzxls, False)
# ty_xst(bzxls[2], bzxls, False)
