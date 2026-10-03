import matplotlib.pyplot as plt


def print_departments(department_1, department_2):
    print("I:", department_1)
    print("II:", department_2)


def produce(department, surplus_value_rate):
    department["m"] = department["v"] * surplus_value_rate


def accumulate(department_1, department_2, add_c_rate_1, add_v_rate_1, v_c_rate_2):
    print_split_line("accumulating")

    # accumulation of department 1:
    acc_m_1 = department_1["m"] / 2
    print("acc_m_1: %.2f" % acc_m_1)

    add_to_c_1 = acc_m_1 * add_c_rate_1
    print("add_to_c_1: %.2f" % add_to_c_1)
    department_1["c"] += add_to_c_1

    add_to_v_1 = acc_m_1 * add_v_rate_1
    print("add_to_v_1: %.2f" % add_to_v_1)
    department_1["v"] += add_to_v_1

    department_1["m"] -= acc_m_1

    # accumulation of department 2:
    add_to_c_2 = department_1["v"] + department_1["m"] - department_2["c"]
    print("add_to_c_2: %.2f" % add_to_c_2)
    department_2["c"] += add_to_c_2

    add_to_v_2 = department_2["c"] * v_c_rate_2 - department_2["v"]
    print("add_to_v_2: %.2f" % add_to_v_2)
    department_2["v"] += add_to_v_2

    department_2["m"] -= (add_to_c_2 + add_to_v_2)


def calc_total_value(department_1, department_2):
    print_split_line("calc all")
    total_value = 0
    for department in [department_1, department_2]:
        for x in department.values():
            total_value += x
    print("total value: %.2f" % total_value)


def calc_dept_value(department):
    print_split_line("calc dept")
    print("calculating:", department)
    total_dept = 0
    for x in department.values():
        total_dept += x
    print("total_dept: %.2f" % total_dept)


def calc_cvm(department_1, department_2):
    print_split_line("calc cvm")
    cvm = list(department_1)
    for item in cvm:
        total_item = department_1[item] + department_2[item]
        print("total %s: %.2f" % (item, total_item))


def print_split_line(word):
    print("-" * 12, word, "-" * 12)


print("Expanded reproduction of Marx.")

department_1 = {"c": 4000.00, "v": 1000.00, "m": 0.00}
department_2 = {"c": 1500.00, "v": 750.00, "m": 0.00}

# department_1 = {"c": 5000.00, "v": 1000.00, "m": 0.00}
# department_2 = {"c": 1430.00, "v": 285.00, "m": 0.00}

add_c_rate_1 = department_1["c"] / (department_1["c"] + department_1["v"])
add_v_rate_1 = department_1["v"] / (department_1["c"] + department_1["v"])
v_c_rate_2 = department_2["v"] / (department_2["c"])

department_changes = []
year = 6
for i in range(year):
    print(f"\nYear {i + 1}:")
    print_departments(department_1, department_2)

    department_changes.append(
        [list(department_1.values()),
         list(department_2.values())]
    )

    produce(department_1, 1.00)
    produce(department_2, 1.00)
    print_split_line("produce")
    print_departments(department_1, department_2)

    accumulate(department_1, department_2, add_c_rate_1, add_v_rate_1, v_c_rate_2)
    print_split_line("expanded")
    print_departments(department_1, department_2)

    department_1["m"] = 0
    department_2["m"] = 0

    calc_total_value(department_1, department_2)
    calc_dept_value(department_1)
    calc_dept_value(department_2)
    calc_cvm(department_1, department_2)

# the first method to draw capitals: total capital
total_capitals = []
for y in department_changes:
    total_capital = 0
    for dept in y:
        total_capital += sum(dept)
    total_capitals.append(total_capital)

plt.plot(total_capitals, marker='o', ls='dashed')

plt.title("Expanded reproduction of Marx")
plt.xlabel("Year")
plt.ylabel("Capital")

plt.show()

# the second method to draw capitals: c and v
c_list = []
v_list = []
for y in department_changes:
    c_list.append(y[0][0] + y[1][0])
    v_list.append(y[0][1] + y[1][1])

plt.bar(list(range(year)), c_list, width=0.35, label='c')
plt.bar(list(range(year)), v_list, width=0.35, bottom=c_list, label='v')

plt.legend()
plt.title("Expanded reproduction of Marx")
plt.xlabel("Year")
plt.ylabel("Capital")

plt.show()

# the third method to draw capitals: Ⅰ and Ⅱ
dept_1_list = []
dept_2_list = []
for y in department_changes:
    dept_1_list.append(y[0][0] + y[0][1])
    dept_2_list.append(y[1][0] + y[1][1])

plt.bar(list(range(year)), dept_1_list, width=0.35, color='gray', label='Ⅰ')
plt.bar(list(range(year)), dept_2_list, width=0.35, bottom=dept_1_list, color='DarkSalmon', label='Ⅱ')

plt.legend()
plt.title("Expanded reproduction of Marx")
plt.xlabel("Year")
plt.ylabel("Capital")

plt.show()
