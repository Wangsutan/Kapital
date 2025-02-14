def calc_surplus_value_directly(new_created_value, labour_force_value):
    return new_created_value - labour_force_value


def calc_surplus_value_rate(variable_capital, surplus_value):
    return surplus_value / variable_capital


def calc_surplus_value_indirectly(variable_capital, surplus_value_rate):
    return variable_capital * surplus_value_rate


if __name__ == "__main__":
    print(f"Direct Surplus Value: {calc_surplus_value_directly(200.00, 100.00):.2f}")
    print(f"Surplus Value Rate: {calc_surplus_value_rate(100.00, 100.00):.2f}")
    print(f"Indirect Surplus Value: {calc_surplus_value_indirectly(100.00, 1.00):.2f}")
