import matplotlib.pyplot as plt


def reinvest(
        constant_capital, variable_capital,
        pct_of_surplus_value_in_reproduction,
        pct_of_surplus_value_as_variable_capital):
    """
    surplus_value_in_reproduction:
    the percent of surplus value that bourgeoisie reused in production
    pct_of_surplus_value_as_variable_capital:
    the percent of surplus value that bourgeoisie reused as variable capital
    """
    surplus_value_in_reproduction = surplus_value * \
        pct_of_surplus_value_in_reproduction

    variable_capital += surplus_value_in_reproduction * \
        pct_of_surplus_value_as_variable_capital
    constant_capital += surplus_value_in_reproduction * \
        (1 - pct_of_surplus_value_as_variable_capital)

    return constant_capital, variable_capital


constant_capital = float(input("constant capital： "))
variable_capital = float(input("variable capital： "))
advanced_capital_orig = constant_capital + variable_capital

surplus_value_list = []
capital_total_list = [advanced_capital_orig]
year_reproduct = int(input("Year(s) of Reproduction: "))

for i in range(1, year_reproduct + 1):
    surplus_value_rate_annual = float(input("surplus value rate annual: "))
    surplus_value = variable_capital * surplus_value_rate_annual
    surplus_value_list.append(surplus_value)
    capital_total_list.append(
        constant_capital + variable_capital + surplus_value)

    print(f"\nAfter {i} year(s):")
    print(f"Constant Capital (c): {constant_capital:.2f}")
    print(f"Variable Capital (v): {variable_capital:.2f}")
    print(f"Surplus Value (m): {surplus_value:.2f}")
    print(f"Capital Total: {capital_total_list[-1]:.2f}\n")

    if i != year_reproduct:
        pct_of_surplus_value_in_reproduction = float(
            input("percent of surplus value in reproduction: "))
        pct_of_surplus_value_as_variable_capital = float(
            input("percent of surplus value as variable_capital: "))

        constant_capital, variable_capital = reinvest(
            constant_capital, variable_capital,
            pct_of_surplus_value_in_reproduction,
            pct_of_surplus_value_as_variable_capital
        )

capital_diff = capital_total_list[-1] - advanced_capital_orig
print(f"Final capital - Advanced capital = {capital_diff:.2f}")

print(f"Total surplus value: {sum(surplus_value_list):.2f}")

plt.plot(capital_total_list, marker='o')

plt.title('Capital Total Over Time')
plt.xlabel('Time (years)')
plt.ylabel('Capital Total')
plt.grid(True)

plt.show()
