from matplotlib import pyplot as plt
import math

plt.style.use(['science', "grid"])

plt.xlabel("x")
plt.ylabel("y")

xs = []
ys = []
for i in range(3000):
    x = math.pi/30*i
    xs.append(x)
    ys.append(math.sin(0.05*x))

plt.ylim(-4,4)
plt.plot(xs, ys)
plt.savefig("imgs/string.png", dpi=500)