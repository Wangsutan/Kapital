import matplotlib.pyplot as plt
import numpy as np


plt.rcParams["font.sans-serif"] = ["SimHei"]  # 用于正常显示中文标签
plt.rcParams["axes.unicode_minus"] = False  # 用来正常显示负号

fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")
font = {"size": 18}

lim_value = 1.3
w_list = [2, 4]  # 角速度
t = np.arange(0, 10, 0.02)
width = 1.5
for i, w in enumerate(w_list):
    re = np.cos(w * t)
    im = np.sin(w * t)
    width = 1.5
    if i == 0:
        width = 4  # 为了对比明显
        # theta不随时间变化的情况
        ax.plot(re, im, zs=0, zdir="z", label=r"$\theta$不随时间变化", linewidth=width)
        ax.plot(np.zeros(np.size(im)), im, zs=0, zdir="z", color="black")
        ax.plot(re, np.zeros(np.size(re)), zs=0, zdir="z", color="black")
    # e^{jwt}
    ax.plot(re, im, t, label=r"$e^{i\theta},\theta=%st$" % w, linewidth=width)
    # cos(wt)
    ax.plot(
        re,
        t,
        zs=lim_value,
        zdir="y",
        label=r"$cos(\theta),\theta=%st$" % w,
        linewidth=width,
    )
    ax.plot(np.zeros(np.size(re)), t, zs=lim_value, zdir="y", color="black")
    # sin(wt)
    ax.plot(
        im,
        t,
        zs=-lim_value,
        zdir="x",
        label=r"$sin(\theta),\theta=%st$" % w,
        linewidth=width,
    )
    ax.plot(np.zeros(np.size(im)), t, zs=-lim_value, zdir="x", color="black")

    ax.text(0, -1.8, 0, s="微信公众号：二进制人工智能", zdir="x")

stick = np.arange(-1, 1.25, 0.25)
stick_list = ["{}i".format(k) for k in stick]
plt.yticks(stick, stick_list)
ax.set_xlabel(r"Re（$cos(\theta)$）", font)
ax.set_ylabel(r"Im（$isin(\theta)$）", font)
ax.set_zlabel("t", font)
plt.xlim((-lim_value, lim_value))
plt.ylim((-lim_value, lim_value))
plt.legend()
plt.show()
