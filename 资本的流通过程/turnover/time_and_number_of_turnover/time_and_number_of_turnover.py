def calc_turnover_num(one_year, turnover_time):
    return one_year / turnover_time


if __name__ == "__main__":
    import numpy as np
    import matplotlib.pyplot as plt

    turnover_time_list = np.linspace(1, 24, num=24)
    turnover_num_list = [
        calc_turnover_num(12, turnover_time)
        for turnover_time in turnover_time_list
    ]

    plt.xlabel("Turnover Time(Months)")
    plt.ylabel("Turnover Number(Annual)")

    plt.plot(turnover_time_list, turnover_num_list)
