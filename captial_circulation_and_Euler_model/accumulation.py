import numpy as np
import math
import matplotlib.pyplot as plt


def calc_surplus_value(total_capital, value_composition, surplus_value_rate):
    return total_capital * value_composition * surplus_value_rate


plt.rcParams["font.sans-serif"] = ["SimHei"]  # 用于正常显示中文
plt.rcParams["axes.unicode_minus"] = False  # 用于正常显示负号

fig = plt.figure()  # Eular total plot
ax = fig.add_subplot(111, projection="3d")
plt.title("简单再生产与扩大再生产\n即资本循环的欧拉螺线模型")
ax.text(0.90, 0.0, 0.0, s="G", zdir="x")
ax.text(0.0, 0.90, 0.0, s="W", zdir="x")
ax.text(-0.9, 0.0, 0.0, s="W'", zdir="x")
ax.text(0.0, -0.9, 0.0, s="G'", zdir="x")

fig_circle = plt.figure()  # circle plot
ax_circle = fig_circle.add_subplot(111)
ax_circle.axis("equal")

fig_sin = plt.figure()  # sine wave plot
ax_sin = fig_sin.add_subplot(111)

fig_time = plt.figure()  # capital scale historical plot
ax_time = fig_time.add_subplot(111)

circle_num = 3
theta_list = np.arange(0, 2 * math.pi * circle_num, math.pi / 180)
history = np.arange(0, 2 * math.pi * circle_num, math.pi / 180)

edge_need = [math.pi * 0.5, math.pi, math.pi * 1.5, math.pi * 2]
value_composition = 0.5
surplus_value_rate = 0.25
accumulate_rate = 1.0
step_num = len(theta_list) / 4  # we add surplus value step by step.

# simple reproduction, same circle
r_orig = 1
r = 1
r_simple, x_simple, y_simple = [], [], []
for i, t in enumerate(theta_list):
    if edge_need[0] < t % (2 * math.pi) <= edge_need[1]:
        surplus_value = calc_surplus_value(r, value_composition, surplus_value_rate)
        r = r + surplus_value * accumulate_rate / step_num
    if edge_need[2] < t % (2 * math.pi) <= edge_need[3]:
        r = r_orig  # clean surplus value
    r_simple.append(r)
    x_simple.append(r * math.cos(t))
    y_simple.append(r * math.sin(t))

ax.plot(x_simple, y_simple, history)
ax_circle.plot(x_simple, y_simple)
ax_sin.plot(history, y_simple)
ax_time.plot(history, r_simple)

# expand reproduction, enlarged circle
r = 1
r_expand, x_expand, y_expand = [], [], []
for i, t in enumerate(theta_list):
    if edge_need[0] < t % (2 * math.pi) <= edge_need[1]:
        surplus_value = calc_surplus_value(r, value_composition, surplus_value_rate)
        r = r + surplus_value * accumulate_rate / step_num
    r_expand.append(r)
    x_expand.append(r * math.cos(t))
    y_expand.append(r * math.sin(t))

ax.plot(x_expand, y_expand, history)
ax_circle.plot(x_expand, y_expand)
ax_sin.plot(history, y_expand)
ax_time.plot(history, r_expand)

# original capital scale, image circle
r = 1
x_image, y_image = [], []
for i, t in enumerate(np.arange(0, 2 * math.pi, math.pi / 180)):
    x_image.append(r * math.cos(t))
    y_image.append(r * math.sin(t))

ax.plot(x_image, y_image, 0, "--")
ax_circle.plot(x_image, y_image, linestyle="--")

plt.show()
