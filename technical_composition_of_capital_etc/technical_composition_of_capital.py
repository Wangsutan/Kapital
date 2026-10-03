import sympy
import copy
import matplotlib.pyplot as plt


def main(technical_composition_of_capital):
    worker_num = sympy.symbols("worker_num")
    machine_num = sympy.symbols("machine_num")

    variable_capital = get_variable_capital(worker_num, worker_salary)
    constant_capital = get_constant_capital(machine_num, machine_price)
    used_money = get_value_total(variable_capital, constant_capital)

    result = sympy.nonlinsolve(
        [
            (machine_num / worker_num) - technical_composition_of_capital,
            money_capital - used_money,
        ],
        (machine_num, worker_num),
    )

    result = list(result)
    machine_num = float(result[0][0])
    worker_num = float(result[0][1])
    print("machines and workers:\n", round(machine_num, 2), ":", round(worker_num, 2))

    variable_capital = get_variable_capital(worker_num, worker_salary)
    constant_capital = get_constant_capital(machine_num, machine_price)
    value_composition_of_capital = get_value_composition_of_capital(
        constant_capital, variable_capital
    )
    return value_composition_of_capital


def get_variable_capital(variable_capital_num, variable_capital_value):
    return variable_capital_num * variable_capital_value


def get_constant_capital(constant_capital_num, constant_capital_value):
    return constant_capital_num * constant_capital_value


def get_value_total(variable_capital, constant_capital):
    return variable_capital + constant_capital


def get_value_composition_of_capital(constant_capital, variable_capital):
    return constant_capital / variable_capital


# annual data
# money_capital = float(input("Money:"))
money_capital = 1000
print("money_capital:", money_capital)

machine_price = 10
worker_salary = 0.6 * 12
print(
    "\nsalary of worker(annual):",
    worker_salary,
    "\nprice of machine(annual):",
    machine_price,
)

technical_composition_of_capital_list = []
value_composition_of_capital_list = []
technical_composition_of_capital = 0.5  # number, machines / workers
technical_composition_of_capital_orig = copy.deepcopy(technical_composition_of_capital)
diff = 0.2

for i in range(21):
    print("============================",)
    technical_composition_of_capital = technical_composition_of_capital_orig + diff * i
    technical_composition_of_capital_list.append(technical_composition_of_capital)
    print("technical composition:", round(technical_composition_of_capital, 2))

    value_composition_of_capital = main(technical_composition_of_capital)
    value_composition_of_capital_list.append(value_composition_of_capital)
    print("value composition:", round(value_composition_of_capital, 2))

plt.plot(technical_composition_of_capital_list, value_composition_of_capital_list)
plt.title("technical composition determines value composition")
plt.xlabel("technical composition")
plt.ylabel("value composition")
