import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter


def calc_profit_rate(
    constant_capital, variable_capital, profit, variable_capital_change_rate
):
    return (profit - variable_capital * variable_capital_change_rate) / (
        constant_capital + variable_capital * (1.0 + variable_capital_change_rate)
    )


def percent_formatter(x, pos):
    return f"{100 * x:.2f}%"


constant_capital_orig = 80
variable_capital_orig = 20
profit_orig = 20

variable_capital_change_rates = np.linspace(-1, 1, 100)

profit_rates = calc_profit_rate(
    constant_capital_orig,
    variable_capital_orig,
    profit_orig,
    variable_capital_change_rates,
)

profit_rate_orig = calc_profit_rate(
    constant_capital_orig, variable_capital_orig, profit_orig, 0
)

plt.plot(variable_capital_change_rates, profit_rates)

plt.annotate(
    f"Original Profit Rate: {profit_rate_orig * 100:.2f}%",
    xy=(0, profit_rate_orig),
    xytext=(0, profit_rate_orig),
    arrowprops=dict(facecolor="black", shrink=0.05),
)

plt.title("Profit Rate Variation with Variable Capital Change Rate")
plt.xlabel("Rate of Change of Variable Capital(%)")
plt.ylabel("Profit Rate")

plt.gca().xaxis.set_major_formatter(FuncFormatter(percent_formatter))
plt.gca().yaxis.set_major_formatter(FuncFormatter(percent_formatter))
plt.xticks(rotation=45, ha="right")

plt.show()
