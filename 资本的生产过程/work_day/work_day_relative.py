import matplotlib.pyplot as plt


def calc_surplus_value_rate(work_hours_for_other, work_hours_for_oneself):
    return work_hours_for_other / work_hours_for_oneself


def draw_pie(work_hours_for_oneself, work_hours_for_other, other_hours, surplus_value_rate):
    plt.pie(
        [work_hours_for_oneself, work_hours_for_other, other_hours],
        labels=["v", "m", "o"],
        autopct="%.2f%%",
        explode=(0, 0.15, 0),
    )

    plt.text(0, 0, f"m': {surplus_value_rate:.2f}")
    plt.show()
    plt.clf()


hours_of_nature_day = 24
work_hours_for_oneself_orig = 6
work_hours_for_other_orig = 6
work_hours = work_hours_for_oneself_orig + work_hours_for_other_orig

work_hours_for_other_list = []
surplus_value_rate_list = []
left_edge = work_hours_for_oneself_orig

print("Work Hours for Others\tSurplus Value Rate")
for i in range(left_edge, 0, -1):
    work_hours_for_oneself_now = i
    work_hours_for_other_now = work_hours - i
    surplus_value_rate = calc_surplus_value_rate(
        work_hours_for_other_now, work_hours_for_oneself_now)
    print(f"{work_hours_for_other_now: .2f}\t{surplus_value_rate: .2f}")

    work_hours_for_other_list.append(work_hours_for_other_now)
    surplus_value_rate_list.append(surplus_value_rate)

    other_hours = hours_of_nature_day - work_hours

    draw_pie(work_hours_for_oneself_now, work_hours_for_other_now,
             other_hours, surplus_value_rate)

plt.plot(work_hours_for_other_list, surplus_value_rate_list)

plt.xlabel("Work Hours for Others")
plt.ylabel("Surplus Value Rate")

plt.show()
