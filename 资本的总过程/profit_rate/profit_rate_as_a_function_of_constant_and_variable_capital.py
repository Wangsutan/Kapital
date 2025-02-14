# 在既定剩余价值率条件下，由不变资本和可变资本共同决定的利润率及其3维图形。

import numpy as np
import matplotlib.pyplot as plt


def calc_profit_rate_distinctly(constant_capital, variable_capital, surplus_value):
    return surplus_value / (constant_capital + variable_capital)


def calc_surplus_value_indirectly(variable_capital, surplus_value_rate):
    return variable_capital * surplus_value_rate


surplus_value_rate = 1.00

c_list = np.linspace(0, 100, 100)
v_list = np.linspace(0, 100, 100)

C, V = np.meshgrid(c_list, v_list)
M = calc_surplus_value_indirectly(V, surplus_value_rate)

Profit_Rate = calc_profit_rate_distinctly(C, V, M)

fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")
ax.plot_surface(C, V, Profit_Rate, cmap="rainbow")

plt.title("Profit Rate as a Function of\nConstant and Variable Capital")

ax.set(
    xlabel="Constant Capital (c)",
    ylabel="Variable Capital (v)",
    zlabel="Profit Rate (p')"
)

plt.show()
