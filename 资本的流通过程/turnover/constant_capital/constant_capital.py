def calc_yield_value(
    total_value_of_constant_capital, entire_function_time, actual_function_time
):
    return total_value_of_constant_capital / entire_function_time * actual_function_time


def calc_current_value_of_constant_capital_orig(
    total_value_of_constant_capital, entire_function_time, actual_function_time
):
    return total_value_of_constant_capital - calc_yield_value(
        total_value_of_constant_capital, entire_function_time, actual_function_time
    )


def calc_current_value_of_constant_capital_simple(
    total_value_of_constant_capital, entire_function_time, actual_function_time
):
    return total_value_of_constant_capital * (
        1 - actual_function_time / entire_function_time
    )


if __name__ == "__main__":
    import numpy as np
    import matplotlib.pyplot as plt

    total_value_of_constant_capital = 100000
    entire_function_time = 5

    function_time_list = np.arange(
        0, entire_function_time, entire_function_time / 100)

    yield_value_list = [
        calc_yield_value(total_value_of_constant_capital,
                         entire_function_time, t)
        for t in function_time_list
    ]

    current_value_list = [
        calc_current_value_of_constant_capital_orig(
            total_value_of_constant_capital, entire_function_time, t
        )
        for t in function_time_list
    ]

    plt.plot(function_time_list, yield_value_list, label="Yield Value")
    plt.plot(function_time_list, current_value_list, label="Current Value")

    plt.title("Yield And Current Value of Constant Capital")
    plt.legend()
    plt.xlabel("Function Time(Year)")
    plt.ylabel("Value")
    plt.show()
