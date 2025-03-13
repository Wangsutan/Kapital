def calc_turnover_capital_total_annual(capital_num_list, capital_time_list):
    turnover_capital_annual = [
        capital_num_list[i] / capital_time_list[i]
        for i in range(len(capital_num_list))
    ]
    turnover_capital_total_annual = sum(turnover_capital_annual)
    return turnover_capital_total_annual


if __name__ == "__main__":
    capital_num_list = [80000, 20000]
    capital_time_list = [10, 1 / 5]

    turnover_capital_total_annual = calc_turnover_capital_total_annual(
        capital_num_list, capital_time_list
    )
    print(f"Annual Total Turnover Capital: {turnover_capital_total_annual}")
