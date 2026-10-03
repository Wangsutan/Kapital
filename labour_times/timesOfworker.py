import matplotlib.pyplot as plt


natural_time = 24
necessary_labour_time = 6
labels = ["necessary labour time", "surplus labour time", "other time"]

times_list = []
for t in range(2, 10, 1):
    surplus_labour_time = t
    other_time = natural_time - necessary_labour_time - surplus_labour_time
    surplus_value_rate = surplus_labour_time / necessary_labour_time
    times_now = [necessary_labour_time, surplus_labour_time, other_time]
    times_list.append(times_now)
    plt.pie(
        times_now, labels=labels, autopct="%.2f%%", explode=(0, 0.15, 0),
    )
    plt.text(
        x=0.5,
        y=-1.5,
        s="nlt, slt, ot: "
        + str(times_now)
        + "\nsurplus_value_rate:%.2f" % surplus_value_rate,
    )
    plt.show()
