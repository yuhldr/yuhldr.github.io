# fpu配置

steps = 1000000
dt = 0.01

constant_model_beta = "beta"
constant_model_alpha = "alpha"

m = 1

# # **** alpha模型参数 ****
# N = 32
# alpha = 0.25
# beta = 0
# k = 0
# a = 1
# ks = [0, 1, 2, 3, 4]
# # **** alpha模型参数 ****

# # **** beta模型参数 ****
N = 32
alpha = 0
beta = 0.4
k = 2
a = 1
ks = [0, 1, 2, 3, 4]
# # **** beta模型参数 ****

# # **** 五模模型参数 ****
# sigma = 0.042
# mu = 0.704
# # sigma = 0.085
# # mu = 1.408

# N = 16
# alpha = 0
# beta = mu
# k = 10
# a = (2 * sigma / (3 * mu))**0.5
# ks = [8, 9, 10, 11, 12]
# # **** 五模模型参数 ****

model = ""
if (alpha == 0):
    model = constant_model_beta
elif (beta == 0):
    model = constant_model_alpha
else:
    print("模型设置错误")
print(model + "模型")

# 各个模式能量随时间变化
path_np_ets = "cache/data/ets.npy"
# 各个原子，不同时刻位移分布
path_np_xst = "cache/data/xst.npy"
# 各个原子，不同时刻速度分布
path_np_vst = "cache/data/vst.npy"
# 各个模式初始位移图，横坐标：第几个原子，纵坐标这个原子的初始位移
path_img_bzn = "cache/imgs/bz/%d"
# 各个模式本征值
path_img_bz = "cache/imgs/bz/bz"

# 各个模式的本征值
path_np_bzzs = "data/bzzs.npy"
# 各个模式的本征向量
path_np_bzxls = "data/bzxls.npy"
# 哈密顿向量
path_np_vs = "data/V.npy"
# 上面三个矩阵，matlab方便打开
path_mat_data = "data/data.mat"

# 某个模式，能量变化
path_img_nt = "test/nt"
# 位移变化
path_img_xst = "test/xst"
# 位移投影到各个模式以后的变化
path_img_ty_xst = "cache/imgs/ty_xst"
# 某个时刻，各个模式能量
path_img_eks = "test/eks"
# 随着时间，各个模式能量求和，看看总能量的变化
path_img_eok = "test/eok"
# 随时间，ks对应的模拟能量变化
path_img_ets = "test/ets"
