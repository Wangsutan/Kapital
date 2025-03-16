from typing import Dict


def print_departments(
    department_1: Dict[str, float], department_2: Dict[str, float]
) -> None:
    print("I:", department_1)
    print("II:", department_2)


def calc_total_value(
    department_1: Dict[str, float], department_2: Dict[str, float]
) -> float:
    total_value: float = 0.0
    for department in [department_1, department_2]:
        for v in department.values():
            total_value += v
    return total_value


def calc_dept_value(department: Dict[str, float]) -> float:
    print("Calculating:", department)
    total_dept: float = 0.0
    for v in department.values():
        total_dept += v
    return total_dept


def calc_cvm(department_1: Dict[str, float], department_2: Dict[str, float]) -> None:
    cvm = list(department_1.keys())
    for item in cvm:
        total_item = department_1[item] + department_2[item]
        print(f"Total {item}: {total_item:.2f}")


if __name__ == "__main__":
    department_1: Dict[str, float] = {"c": 4000.00, "v": 1000.00, "m": 1000.00}
    department_2: Dict[str, float] = {"c": 2000.00, "v": 500.00, "m": 500.00}
    print_departments(department_1, department_2)

    total_value: float = calc_total_value(department_1, department_2)
    print(f"Total value: {total_value:.2f}\n")

    for department in [department_1, department_2]:
        total_dept: float = calc_dept_value(department)
        print(f"Total dept: {total_dept:.2f}\n")

    calc_cvm(department_1, department_2)
