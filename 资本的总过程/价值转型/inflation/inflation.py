import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter


def calc_product_price(
    constant_capital,
    variable_capital,
    variable_capital_change_rate,
    profit_rate_general,
):
    cost_price = constant_capital + variable_capital * (1 + variable_capital_change_rate)
    product_price = cost_price * (1 + profit_rate_general)
    return product_price


def percent_formatter(x, pos):
    return f"{100 * x:.2f}%"


constant_capital_orig = 80
variable_capital_orig = 20
profit_orig = 20

product_price_orig = constant_capital_orig + variable_capital_orig + profit_orig
profit_rate_avg = profit_orig / (constant_capital_orig + variable_capital_orig)

variable_capital_change_rates = np.linspace(-1, 1, 100)

product_prices = calc_product_price(
    constant_capital_orig,
    variable_capital_orig,
    variable_capital_change_rates,
    profit_rate_avg
)

plt.plot(variable_capital_change_rates, product_prices)

plt.title("Product Price Variation with Variable Capital Change Rate")
plt.xlabel("Rate of Change of Variable Capital")
plt.ylabel("Product Price")

plt.gca().xaxis.set_major_formatter(FuncFormatter(percent_formatter))
plt.xticks(rotation=45)

plt.plot(
    variable_capital_change_rates,
    [product_price_orig for i in range(variable_capital_change_rates.size)]
)

plt.show()
