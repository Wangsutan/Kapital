import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter


def calc_surplus_value_rate(variable_capital, surplus_value):
    return surplus_value / variable_capital


def calc_profit_rate_distinctly(constant_capital, variable_capital, surplus_value):
    return surplus_value / (constant_capital + variable_capital)


def percent_formatter(x, pos):
    return f"{100 * x:.2f}%"


c = 80
v = 20

surplus_value_list = np.linspace(10, 40, 100)

surplus_value_rate_list = calc_surplus_value_rate(v, surplus_value_list)
profit_rate_list = calc_profit_rate_distinctly(c, v, surplus_value_list)

plt.plot(surplus_value_list, surplus_value_rate_list, label="Surplus Value Rate")
plt.plot(surplus_value_list, profit_rate_list, label="Profit Rate")

plt.title("Surplus Value Rate VS Profit Rate")
plt.xlabel("Surplus Value")
plt.ylabel("Rate")
plt.legend()

plt.gca().yaxis.set_major_formatter(FuncFormatter(percent_formatter))

plt.show()
