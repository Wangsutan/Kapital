import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter


def get_profit_rate(constant_capital, variable_capital, surplus_value_rate):
    return (variable_capital * surplus_value_rate) / (
        constant_capital + variable_capital
    )


def percent_formatter(x, pos):
    return f"{100 * x:.2f}%"


constant_capital_orig = 50
variable_capital_orig = 100
surplus_value_rate = 1.00

constant_capital_list = np.linspace(constant_capital_orig, 500, 100)
profit_rate_list = get_profit_rate(
    constant_capital_list, variable_capital_orig, surplus_value_rate
)

plt.plot(constant_capital_list, profit_rate_list)

plt.title("Profit Rate Variation with Constant Capital Change")
plt.xlabel("Constant Capital")
plt.ylabel("Profit Rate")

plt.gca().yaxis.set_major_formatter(FuncFormatter(percent_formatter))

plt.show()
