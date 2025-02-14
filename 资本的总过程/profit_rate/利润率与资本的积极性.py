def print_capital_response(profit_rate):
    messages = [
        "资本就没有积极性。",
        "资本就胆大起来。",
        "资本就保证到处被使用。",
        "资本就活跃起来。",
        "资本就铤而走险。",
        "资本就敢践踏一切人间法律。",
        "资本就敢犯任何罪行，甚至冒绞首的危险。",
    ]

    profit_rate_margin = [0.05, 0.10, 0.20, 0.50, 1.00, 3.00]
    for i, margin in enumerate(profit_rate_margin):
        if profit_rate < margin:
            print(messages[i])
            break
    else:
        print(messages[-1])


if __name__ == "__main__":
    profit_rate = float(input("请输入利润率（单位%）："))
    print(f"如果有{profit_rate:.2f}%的利润率，")
    print_capital_response(profit_rate / 100)
