import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter


def calc_profit_rate(
    surplus_value_rate,
    turnover_num_of_variable_capital_annual,
    constant_capital,
    variable_capital,
):
    return (
        turnover_num_of_variable_capital_annual
        * surplus_value_rate
        * variable_capital
        / (constant_capital + variable_capital)
    )


def percent_formatter(x, pos):
    return f"{100 * x:.2f}%"


constant_capital_orig = 80
variable_capital_orig = 20

surplus_value_rates = np.linspace(0.5, 1.5, 100)
turnover_nums_of_variable_capital_annual = np.linspace(1, 5, 100)
surplus_value_rate_grid, turnover_nums_of_variable_capital_annual_grid = np.meshgrid(
    surplus_value_rates, turnover_nums_of_variable_capital_annual
)

profit_rates = calc_profit_rate(
    surplus_value_rate_grid,
    turnover_nums_of_variable_capital_annual_grid,
    constant_capital_orig,
    variable_capital_orig,
)

fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")

ax.plot_surface(
    surplus_value_rate_grid, turnover_nums_of_variable_capital_annual_grid, profit_rates
)

ax.set_xlabel("Surplus Value Rate")
ax.set_ylabel("Turnover Number of\nVariable Capital Annual")
ax.set_zlabel("Profit Rate(%)", labelpad=10)

plt.gca().zaxis.set_major_formatter(FuncFormatter(percent_formatter))

plt.show()
