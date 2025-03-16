from typing import Dict


def check_simple_equilibrium(
    department_1: Dict[str, float], department_2: Dict[str, float]
) -> bool:
    return department_1["v"] + department_1["m"] == department_2["c"]


if __name__ == "__main__":
    department_1: Dict[str, float] = {"c": 4000.00, "v": 1000.00, "m": 1000.00}
    department_2: Dict[str, float] = {"c": 2000.00, "v": 500.00, "m": 500.00}

    if_simple_equilibrium: bool = check_simple_equilibrium(department_1, department_2)

    if if_simple_equilibrium:
        print("Ⅰv + Ⅰm = Ⅱc")
        print(if_simple_equilibrium)
    else:
        print(if_simple_equilibrium)
