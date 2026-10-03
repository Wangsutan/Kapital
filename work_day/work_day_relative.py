import matplotlib.pyplot as plt


def calc_rate_surplus_value(work_for_other, work_for_oneself):
     return work_for_other / work_for_oneself


nature_day = 24
work_for_oneself = 6
work_for_other = 6
work_hours = work_for_oneself + work_for_other

surplus_value_datas = []
labels = ["v", "m", ""]
left_edge = work_for_oneself
for i in range(left_edge, 0, -1):
    work_for_oneself = i
    work_for_other_now = work_hours - i
    rate_surplus_value = calc_rate_surplus_value(work_for_other_now, work_for_oneself)
    print(work_for_other_now, rate_surplus_value)
    surplus_value_datas.append([work_for_other_now, rate_surplus_value])

    plt.pie([work_for_oneself, work_for_other_now, nature_day - work_hours], labels=labels)
    plt.text(-1, -1.5, "m': %.2f" % rate_surplus_value)
    plt.show()
    plt.clf()

plt.plot(
    [surplus_value_datas[i][0] for i in range(len(surplus_value_datas))],
    [surplus_value_datas[i][1] for i in range(len(surplus_value_datas))])
plt.xlabel("m")
plt.ylabel("m'")
