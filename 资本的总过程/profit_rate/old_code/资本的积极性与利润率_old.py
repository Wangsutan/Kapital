import sys


def get_profit_rate():
    input_str = input("请输入实际的利润率（单位%，输入q退出）：")
    if not is_number(input_str):
        sys.exit()
    else:
        real_profit_rate = float(input_str)
        return real_profit_rate


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata

        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False


profit_rate_margin = [0.05, 0.10, 0.20, 0.50, 1.00, 3.00]

while True:
    real_profit_rate = get_profit_rate()

    print("如果有%.2lf%%的利润率，" % real_profit_rate)
    if real_profit_rate < profit_rate_margin[0] * 100:
        print("资本就没有积极性。")
    elif real_profit_rate < profit_rate_margin[1] * 100:
        print("资本就胆大起来。")
    elif real_profit_rate < profit_rate_margin[2] * 100:
        print("资本就保证到处被使用。")
    elif real_profit_rate < profit_rate_margin[3] * 100:
        print("资本就活跃起来。")
    elif real_profit_rate < profit_rate_margin[4] * 100:
        print("资本就铤而走险。")
    elif real_profit_rate < profit_rate_margin[5] * 100:
        print("资本就敢践踏一切人间法律。")
    else:
        print("资本就敢犯任何罪行，甚至冒绞首的危险。") 
