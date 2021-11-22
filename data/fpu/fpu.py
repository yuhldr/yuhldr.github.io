# FPU模拟


import numpy as np
import time
import scipy.io as scio
from config import N, steps, m, dt, a
import config


def get_bz(V):
    # ! 接近0的本征值对应的是第一个本征模式，而且默认算出来的是列一个本征向量
    bzzs_, bzxls_ = np.linalg.eig(V)

    # 排个序，绝对值最小的是第一个模式
    bzzs_arg = np.argsort(abs(bzzs_))
    bzzs = np.array([bzzs_[i] for i in bzzs_arg])
    bzxls = np.array([bzxls_[:, i] for i in bzzs_arg])

    scio.savemat(config.path_mat_data, {'V': V, "bzzs": bzzs, "bzxls": bzxls})

    np.save(config.path_np_bzzs, bzzs)
    np.save(config.path_np_bzxls, bzxls)
    np.save(config.path_np_vs, V)

    return bzzs, bzxls


def get_V(N):
    V = np.zeros((N, N))

    for i in range(N):
        for j in range(N):
            if (i == j):
                V[i, j] = -2
            elif (i == j + 1 or i == j - 1):
                V[i, j] = 1
    return V


# 受力，单独写出了，方便以后修改胡克定律的形式，比如以后beta模型
def get_fs(xs, k=1):

    N = len(xs)
    xs_ = np.hstack(([0], xs, [0]))
    xs_0 = xs_[0:N]
    xs_1 = xs_[0 + 1:N + 1]
    xs_2 = xs_[0 + 2:N + 2]
    xs_2_1 = xs_2-xs_1
    xs_1_0 = xs_1 - xs_0
    return k * (xs_2_1 - xs_1_0) + config.alpha * ((xs_2_1)**2 - (xs_1_0)**2) +\
        config.beta * ((xs_2_1)**3 - (xs_1_0)**3)


# 根据上一时刻，使用f=ma计算下一时刻，verlet算法，需要前两时刻的分布，但是本征向量只得到了一个时刻的，第二个时刻还是要用这个精度差的来计算
def get_x_t2(xs, vs, dt, m):
    a_list = get_fs(xs) / m
    xs = xs + vs * dt + a_list * dt**2 / 2
    vs = vs + a_list * dt

    return xs, vs


# 好处是，三阶导数那里约掉了，比直接用牛顿方程，精度高
def get_x_t2_verlet(xs_t0, xs_t1, dt, m):
    # 注意必须是t1时刻的xs，也就是中间时刻的
    a_list = get_fs(xs_t1) / m
    xs_t2 = 2 * xs_t1 - xs_t0 + a_list * dt**2
    vs = (xs_t2 - xs_t0) / (2 * dt)

    return xs_t1, xs_t2, vs


# 使用verlet计算，精度更高
def run_by_verlet(xs):

    model = config.model

    xst = []
    vst = []

    vs = np.linspace(0, 0, N)
    # 注意x与v对应，必须是同一时刻的
    xst.append(xs)
    vst.append(vs)

    xs_t0 = xs
    # 第二步必须还是直接用牛顿
    xs_t1, vs = get_x_t2(xs, vs, dt, m)

    xst.append(xs_t1)
    vst.append(vs)
    start_time = time.time()

    for step in range(steps):
        # !同步，用矩阵计算也是同步，要注意不要出现，更改这一时刻的分布了，上一时刻的矩阵也被修改了，python的矩阵不深度复制的话，是有指针问题的
        # 注意是第二时刻的分布，计算受力，得到第三时刻的分布
        xs_t0, xs_t1, vs = get_x_t2_verlet(xs_t0, xs_t1, dt, m)

        if (step % 10000 == 0):
            print("t=%d time=%f " % (step, time.time() - start_time))
            start_time = time.time()
        xst.append(xs_t1)
        vst.append(vs)

    xst = np.array(xst)
    vst = np.array(vst)

    np.save(config.path_np_xst, xst)
    np.save(config.path_np_vst, vst)

    print(model + "模型")


V = get_V(N)

bzzs, bzxls = get_bz(V)

start_time_ = time.time()

bzxl = bzxls[config.k]
xs = (bzxl / max(abs(bzxl))) * a
print(xs)
print(a)

run_by_verlet(xs)
# run(bzxls[0], steps=steps, dt=dt, m=m)

print("time=%f " % (time.time() - start_time_))
