import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys


def product_force(x, arr):
    # - `base`为底数。
    # - `left_right_translate`为左右平移量，缩写为`lr`。
    # - `up_down_translate`为上下平移量，缩写为`ud`。
    # - `abscissa_flexible`为横坐标伸缩量，缩写为`af`。
    # - `ordinate_flexible`为纵坐标伸缩量，缩写为`of`。

    base, lr, ud, af, of = arr[0], arr[1], arr[2], arr[3], arr[4]

    if not (
        base > 1.0
        and af > 0.0
        and of > 0.0
        and x >= (1.0 + lr) / af
        and x > (log(base, -1.0 * ud / of) + lr) / af
    ):
        print("Do not satisfy the function of product force.\nExit!")
        sys.exit()
    else:
        return of * log(base, af * x - lr) + ud


def log(base, x):
    return np.log(x) / np.log(base)


def get_product_cost_up_margin(market_price, profit_rate):
    return market_price / (1 + profit_rate)


market_price = 26.90
profit_rate = 0.30

# input datas of fixed_capital_independent
fixed_capital_independent_columns = ["生产要素", "总价值", "使用年限"]
fixed_capital_independent_datas = [["厂房", 1500, 10], ["流水线", 500, 5], ["辅助工具", 100, 2]]

fixed_capital_independent_df = pd.DataFrame(
    fixed_capital_independent_datas,
    columns=fixed_capital_independent_columns,
)

fixed_capital_independent_df["年度转移价值"] = (
    fixed_capital_independent_df["总价值"] / fixed_capital_independent_df["使用年限"]
)

# input datas of circulating_capital_except_labour
circulating_capital_except_labour_columns = ["生产要素", "单位产品投入量", "单位价值"]
circulating_capital_except_labour_datas = [
    ["馅", 1, 1.5],
    ["饼", 1, 0.5],
    ["包装", 1, 0.05],
]

circulating_capital_except_labour_df = pd.DataFrame(
    circulating_capital_except_labour_datas,
    columns=circulating_capital_except_labour_columns,
)

# labour nums as variable
labour_num_list = np.linspace(0, 200, 201)
labour_value_para = 10.0
surplus_value_rate = 1

# function of product force: f(x) = 8.5 * np.log(1.5x + 1)
product_num_list = [
    product_force(labour_num, [np.e, -1.0, 0.0, 1.5, 8.50])
    for labour_num in labour_num_list
]

# get list of market price and total revenue
market_price_list = [market_price for x in product_num_list]
revenue_total_list = [market_price * pn for pn in product_num_list]

# get list of total value and total cost etc.
value_total_list = []
cost_total_list = []
for i in range(len(product_num_list)):
    cost_fixed = fixed_capital_independent_df["年度转移价值"].sum()
    cost_circulating = (
        circulating_capital_except_labour_df["单位产品投入量"]
        * circulating_capital_except_labour_df["单位价值"]
    ).sum() * product_num_list[i]

    labour_value = labour_value_para * labour_num_list[i]
    value_total = cost_fixed + cost_circulating + labour_value
    value_total_list.append(value_total)

    wage = labour_value / (1 + surplus_value_rate)
    cost_total = cost_fixed + cost_circulating + wage
    cost_total_list.append(cost_total)

value_per_product_list = [
    value_total_list[i] / product_num_list[i] for i in range(len(product_num_list))
]

cost_per_product_list = [
    cost_total_list[i] / product_num_list[i] for i in range(len(product_num_list))
]

# get the up margin for cost per product
cost_per_product_up_margin = get_product_cost_up_margin(market_price, profit_rate)
cost_per_product_up_margin_list = [cost_per_product_up_margin for x in product_num_list]
print(f"\nIn order to ensure profit rate {profit_rate * 100}%,")
print(f"cost_per_product_up_margin: {cost_per_product_up_margin}")

# about min of cost per product
cost_per_product_min = min(cost_per_product_list)
print("\ncost_per_product_min:", cost_per_product_min)

cost_per_product_min_index = cost_per_product_list.index(cost_per_product_min)

cost_per_product_min_to_product_num = product_num_list[cost_per_product_min_index]
print("cost_per_product_min_to_product_num:", cost_per_product_min_to_product_num)

cost_per_product_min_to_labour_num = labour_num_list[cost_per_product_min_index]
print("cost_per_product_min_to_labour_num:", cost_per_product_min_to_labour_num)

# calc range of product num and labour num which can ensure the profit rate
product_num_min = 0
labour_num_min = 0
for i in range(len(product_num_list)):
    if cost_per_product_list[i] <= cost_per_product_up_margin:
        product_num_min = product_num_list[i]
        labour_num_min = labour_num_list[i]
        break

product_num_max = 0
labour_num_max = 0
for i in range(len(product_num_list) - 1, 0, -1):
    if cost_per_product_list[i] <= cost_per_product_up_margin:
        product_num_max = product_num_list[i]
        labour_num_max = labour_num_list[i]
        break

print(f"\nIn order to ensure profit rate {profit_rate * 100}%,")
print(f"product_num range: ({product_num_min}, {product_num_max})")
print(f"labour_num_list range: ({labour_num_min}, {labour_num_max})")

# about total profit
profit_total_list = [
    revenue_total_list[i] - cost_total_list[i] for i in range(len(product_num_list))
]

profit_total_max = max(profit_total_list)
print("\nprofit_total_max:", profit_total_max)

profit_total_max_idx = profit_total_list.index(profit_total_max)

profit_total_max_to_product_num = product_num_list[profit_total_max_idx]
print("profit_total_max_to_product_num:", profit_total_max_to_product_num)

profit_total_max_to_labour_num = labour_num_list[profit_total_max_idx]
print("profit_total_max_to_labour_num:", profit_total_max_to_labour_num)

# draw

# 劳动力作为核心自变量的生产力函数曲线
plt.figure(1)
plt.plot(labour_num_list, product_num_list, label="product_force")
plt.xlabel("labour_num")
plt.ylabel("product_num")
plt.legend()

# 个别总价值和个别总成本曲线
plt.figure(2)
plt.plot(product_num_list, value_total_list, label="value")
plt.plot(product_num_list, cost_total_list, label="cost")
plt.xlabel("product_num")
plt.ylabel("value")
plt.legend()

# 单位产品的价值、成本、市场价格和市场成本上边界综合图形
plt.figure(3)
plt.plot(
    product_num_list,
    value_per_product_list,
    linestyle="dotted",
    label="value_per_product",
)

plt.plot(product_num_list, cost_per_product_list, label="cost_per_product")

plt.plot(
    cost_per_product_min_to_product_num, cost_per_product_min, marker="o", color="m"
)
plt.annotate(
    "cost_per_product_min",
    xy=(cost_per_product_min_to_product_num, cost_per_product_min),
)

plt.plot(product_num_list, market_price_list, label="market_price")

plt.plot(
    product_num_list,
    cost_per_product_up_margin_list,
    label="cost_per_product_up_margin",
)

plt.xlabel("product_num")
plt.ylabel("value")
plt.legend()

# 总收入、总成本和总利润综合图形
plt.figure(4)
plt.plot(product_num_list, revenue_total_list, label="revenue_total")
plt.plot(product_num_list, cost_total_list, label="cost_total")
plt.plot(product_num_list, profit_total_list, label="profit_total")
plt.plot(
    product_num_list, [0 for i in range(len(product_num_list))], linestyle="dotted"
)

plt.plot(profit_total_max_to_product_num, profit_total_max, marker="o", color="c")
plt.annotate(
    "profit_total_max",
    xy=(profit_total_max_to_product_num, profit_total_max),
)

plt.plot(
    cost_per_product_min_to_product_num,
    profit_total_list[cost_per_product_min_index],
    marker="o",
    color="m",
)
plt.annotate(
    "cost_per_product_min",
    xy=(
        cost_per_product_min_to_product_num,
        profit_total_list[cost_per_product_min_index],
    ),
    xytext=(
        cost_per_product_min_to_product_num,
        profit_total_list[cost_per_product_min_index] - 50,
    ),
)

plt.xlabel("product_num")
plt.ylabel("value")
plt.legend()

plt.show()
