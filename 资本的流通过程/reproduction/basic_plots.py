import matplotlib.pyplot as plt
from typing import List, Dict, TypeAlias


DepartmentChanges: TypeAlias = List[Dict[str, Dict[str, float]]]


def draw_total_capital(department_changes: DepartmentChanges) -> None:
    """
    the first method to draw capitals: total capital
    """
    total_capitals: List[float] = []
    for year in department_changes:
        total_capital_per_year = sum(sum(dept.values()) for dept in year.values())
        total_capitals.append(total_capital_per_year)

    plt.plot(total_capitals, marker="o", ls="dashed")

    plt.title("Increased reproduction of Marx")
    plt.xlabel("Year")
    plt.ylabel("Capital")

    plt.show()


def draw_c_and_v(department_changes: DepartmentChanges) -> None:
    """
    the second method to draw capitals: c and v
    """
    c_list: List[float] = []
    v_list: List[float] = []
    for year in department_changes:
        c = sum(dept["c"] for dept in year.values())
        v = sum(dept["v"] for dept in year.values())
        c_list.append(c)
        v_list.append(v)

    years: List[int] = list(range(len(department_changes)))
    plt.bar(years, c_list, width=0.35, label="c")
    plt.bar(years, v_list, width=0.35, bottom=c_list, label="v")

    plt.legend()
    plt.title("Increased reproduction of Marx")
    plt.xlabel("Year")
    plt.ylabel("Capital")

    plt.show()


def draw_capital_in_department(department_changes: DepartmentChanges) -> None:
    """
    the third method to draw capitals: Ⅰ and Ⅱ
    """
    dept_1_list: List[float] = []
    dept_2_list: List[float] = []
    for year in department_changes:
        dept_1_total = sum(year["dept_1"].values())
        dept_2_total = sum(year["dept_2"].values())
        dept_1_list.append(dept_1_total)
        dept_2_list.append(dept_2_total)

    years: List[int] = list(range(len(department_changes)))
    plt.bar(years, dept_1_list, width=0.35, color="gray", label="Ⅰ")
    plt.bar(
        years,
        dept_2_list,
        width=0.35,
        bottom=dept_1_list,
        color="DarkSalmon",
        label="Ⅱ",
    )

    plt.legend()
    plt.title("Increased reproduction of Marx")
    plt.xlabel("Year")
    plt.ylabel("Capital")

    plt.show()


if __name__ == "__main__":
    department_changes = [
        {
            "dept_1": {"c": 4000.0, "v": 1000.0, "m": 0.0},
            "dept_2": {"c": 1500.0, "v": 750.0, "m": 0.0},
        },
        {
            "dept_1": {"c": 4400.0, "v": 1100.0, "m": 0},
            "dept_2": {"c": 1600.0, "v": 800.0, "m": 0},
        },
        {
            "dept_1": {"c": 4840.0, "v": 1210.0, "m": 0},
            "dept_2": {"c": 1760.0, "v": 880.0, "m": 0},
        },
        {
            "dept_1": {"c": 5324.0, "v": 1331.0, "m": 0},
            "dept_2": {"c": 1936.0, "v": 968.0, "m": 0},
        },
        {
            "dept_1": {"c": 5856.4, "v": 1464.1, "m": 0},
            "dept_2": {"c": 2129.6, "v": 1064.8, "m": 0},
        },
        {
            "dept_1": {"c": 6442.04, "v": 1610.51, "m": 0},
            "dept_2": {"c": 2342.56, "v": 1171.28, "m": 0},
        },
    ]

    draw_total_capital(department_changes)
    draw_c_and_v(department_changes)
    draw_capital_in_department(department_changes)
