import matplotlib.pyplot as plt


def if_withdraw(ptrs_begin, step):
    """If withdraw money capital from the form of good capital."""
    global money_capital
    for ptr in reversed(ptrs_begin):
        if (step - ptr) == turnover_time:
            money_capital += Arbeitsperiode * flüssiges_Kapital_per_week
            step_money_capital_list.append([step, money_capital])
            ptrs_withdraw.append(step)
            break


def get_begin_point(step):
    """Collect the point of beginning."""
    if step % Arbeitsperiode == 0:
        ptrs_begin.append(step)


def get_special_point_from(ptrs_list, resources_list):
    target_list = []
    for ptr in ptrs_list:
        for i in range(len(resources_list)):
            if ptr == resources_list[i][0]:
                target_list.append(resources_list[i][1])
                break
    return target_list


Arbeitsperiode = 9  # labour time
Umlaufszeit = 3  # circulating time
other_Produktionsperiode = 0  # default 0 here
turnover_time = Arbeitsperiode + other_Produktionsperiode + Umlaufszeit

flüssiges_Kapital_per_week = 100
money_capital = turnover_time * flüssiges_Kapital_per_week

step_money_capital_list = [[0, money_capital]]
ptrs_begin = [0]
ptrs_withdraw = []

step_length = 1
for step in range(step_length * 1, step_length * int(50 / step_length + turnover_time)):
    money_capital -= flüssiges_Kapital_per_week * step_length
    step_money_capital_list.append([step, money_capital])

    if_withdraw(ptrs_begin, step)
    get_begin_point(step)

steps, money_capitals = zip(*step_money_capital_list)

# draw
plt.figure(figsize=(12, 8))

plt.plot(steps, money_capitals)

plt.scatter(
    ptrs_begin,
    get_special_point_from(ptrs_begin, step_money_capital_list),
    c="g",
    alpha=0.5,
    label="begin",
)

plt.scatter(
    ptrs_withdraw,
    get_special_point_from(ptrs_withdraw, step_money_capital_list[::-1]),
    c="k",
    marker="^",
    alpha=0.5,
    label="withdraw",
)

plt.legend()

plt.xlabel("Week")
plt.ylabel("Money Capital")

plt.xticks(range(int(min(steps)), int(max(steps)) + 1, 5))
plt.yticks(
    range(
        int(min(money_capitals)),
        int(max(money_capitals)) + 1,
        flüssiges_Kapital_per_week,
    )
)

plt.grid(linestyle="--", alpha=1)

plt.show()
