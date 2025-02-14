def calc_profit_rate_distinctly(constant_capital, variable_capital, surplus_value):
    return surplus_value / (constant_capital + variable_capital)


def calc_profit_rate_indistinctly(advanced_capital, surplus_value):
    return surplus_value / advanced_capital


if __name__ == "__main__":
    print(f"Distinct Profit Rate: {calc_profit_rate_distinctly(800.00, 200.00, 200.00) * 100.00:.2f}%")
    print(f"Indistinct Profit Rate: {calc_profit_rate_indistinctly(1000.00, 200.00) * 100.00:.2f}%")
