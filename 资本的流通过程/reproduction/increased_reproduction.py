from basic_functions import print_departments
from typing import Dict, TypeAlias

Department: TypeAlias = Dict[str, float]


def produce(department: Department, surplus_value_rate: float) -> None:
    department["m"] = department["v"] * surplus_value_rate


def accumulate(
    dept_1: Department,
    dept_2: Department,
    m_accumulate_rate_of_dept_1: float,
) -> None:
    m_accumulated_of_dept_1: float = dept_1["m"] * m_accumulate_rate_of_dept_1

    m_reinvest_rate_to_c_of_dept_1: float = dept_1["c"] / (dept_1["c"] + dept_1["v"])
    v_c_rate_of_dept_2: float = dept_2["v"] / (dept_2["c"])

    # Accumulation of department 1:
    dept_1["m"] -= m_accumulated_of_dept_1
    dept_1["c"] += m_accumulated_of_dept_1 * m_reinvest_rate_to_c_of_dept_1
    dept_1["v"] += m_accumulated_of_dept_1 * (1.0 - m_reinvest_rate_to_c_of_dept_1)

    # Accumulation of department 2:
    m_accumulated_to_c_of_dept_2: float = dept_1["v"] + dept_1["m"] - dept_2["c"]
    dept_2["c"] += m_accumulated_to_c_of_dept_2

    m_accumulated_to_v_of_dept_2: float = dept_2["c"] * v_c_rate_of_dept_2 - dept_2["v"]
    dept_2["v"] += m_accumulated_to_v_of_dept_2

    dept_2["m"] -= m_accumulated_to_c_of_dept_2 + m_accumulated_to_v_of_dept_2


dept_1: Department = {"c": 4000.00, "v": 1000.00, "m": 0.00}
dept_2: Department = {"c": 1500.00, "v": 750.00, "m": 0.00}

department_changes: list = []
department_changes.append([list(dept_1.values()), list(dept_2.values())])

year_reproduct = int(input("Year(s) of Reproduction: "))
for i in range(1, year_reproduct + 1):
    print(f"\nYear {i}:")

    print("\nOriginal Status:")
    print_departments(dept_1, dept_2)

    print("\nProduction:")
    surplus_value_rate_of_dept_1: float = float(
        input("Surplus Value Rate of Dept1(1.00 for example): ")
    )
    surplus_value_rate_of_dept_2: float = float(
        input("Surplus Value Rate of Dept2(1.00 for example): ")
    )

    produce(dept_1, surplus_value_rate_of_dept_1)
    produce(dept_2, surplus_value_rate_of_dept_2)

    print_departments(dept_1, dept_2)

    print("\nAccumulation:")
    m_accumulate_rate_of_dept_1: float = float(
        input("Accumulate Rate of Surplus Value of Dept1(0.5 for example): ")
    )

    accumulate(dept_1, dept_2, m_accumulate_rate_of_dept_1)

    print_departments(dept_1, dept_2)

    print("\nConsumption of Surplus Value:")
    dept_1["m"] = 0.0
    dept_2["m"] = 0.0

    print_departments(dept_1, dept_2)

    department_changes.append([list(dept_1.values()), list(dept_2.values())])

print("\nDepartment Changes:")
print(department_changes)
