import matplotlib.pyplot as plt


def if_withdraw(ptrs_begin, step):
    """If withdraw money capital from the form of good capital."""
    global money_capital
    for p in ptrs_begin[::-1]:  # search from the tail of list
        if (step - p) == turnover_time:
            # the quantity is depended on how much it cost before
            money_capital += Arbeitsperiode * flüssiges_Kapital_per_week
            # ATTENTION:
            # change the last element of this list which was 0 just now by add new point
            money_capital_list.append([step, money_capital])
            ptrs_withdraw.append(step)
            break  # decrease the search time


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


# These parameters can be changed.
Arbeitsperiode = 9  # labour time
Umlaufszeit = 3  # circulating time
other_Produktionsperiode = 0  # default 0 here
turnover_time = Arbeitsperiode + other_Produktionsperiode + Umlaufszeit

# invasted money capital on floating capital per week
flüssiges_Kapital_per_week = 100
# advance capital at the beginning of first invest
money_capital = turnover_time * flüssiges_Kapital_per_week
money_capital_list = [[0.0, money_capital]]

ptrs_begin = [0]
ptrs_withdraw = []

# ATTENTION:
# step_length should conform to the function of if_withdraw .
step_length = 1
step_list = [step_length * i for i in range(1, int(50 / step_length + turnover_time))]

for step in step_list:
    # invested money capital per week
    money_capital -= flüssiges_Kapital_per_week * step_length
    money_capital_list.append([step, money_capital])  # save this data

    if_withdraw(ptrs_begin, step)
    get_begin_point(step)

# split money_capital_list
steps, money_capitals = [], []
for i in range(len(money_capital_list)):
    steps.append(money_capital_list[i][0])
    money_capitals.append(money_capital_list[i][1])

# draw the figure from specific datas
plt.figure(figsize=(12, 8))

plt.plot(steps, money_capitals)

plt.scatter(ptrs_begin, get_special_point_from(ptrs_begin, money_capital_list), c="g", alpha=0.5, label='begin')
plt.scatter(ptrs_withdraw, get_special_point_from(ptrs_withdraw, money_capital_list[::-1]), c="k", marker='^', alpha=0.5, label='withdraw')
plt.legend()
plt.xlabel("week")
plt.xticks(steps)

plt.ylabel("money capital")
plt.yticks(sorted(list(set(money_capitals))))

plt.grid(linestyle="--", alpha=1)

plt.show()
