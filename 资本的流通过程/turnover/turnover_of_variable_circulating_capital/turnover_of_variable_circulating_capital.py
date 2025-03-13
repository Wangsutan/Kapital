def calc_advanced_variable_circulating_capital(
        annual_used_variable_circulating_capital, turnover_time):
    return annual_used_variable_circulating_capital / turnover_time


def calc_annual_used_variable_circulating_capital(
        advanced_variable_circulating_capital, turnover_time):
    return advanced_variable_circulating_capital * turnover_time


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    turnover_times = list(range(1, 13))

    # About Advanced Variable Circulating Capital
    annual_used_variable_circulating_capital = 5000
    advanced_variable_circulating_capitals = [
        calc_advanced_variable_circulating_capital(
            annual_used_variable_circulating_capital, tt)
        for tt in turnover_times]

    plt.title("Advanced Variable Circulating Capital")
    plt.plot(turnover_times, advanced_variable_circulating_capitals)

    plt.xlabel("Turnover Time(Month)")
    plt.ylabel("Value")

    plt.show()

    # About Annual Used Variable Circulating Capital
    advanced_variable_circulating_capital = 500
    annual_used_variable_circulating_capitals = [
        calc_annual_used_variable_circulating_capital(
            advanced_variable_circulating_capital, tt)
        for tt in turnover_times]

    plt.title("Annual Used Variable Circulating Capital")
    plt.plot(turnover_times, annual_used_variable_circulating_capitals)

    plt.xlabel("Turnover Time(Month)")
    plt.ylabel("Value")

    plt.show()
