from department import (
    CapitalFormProducingSurplusValue,
    CapitalFormLiquidity,
    CapitalFormCirculation,
    CapitalFormMean,
    CapitalFormExistence,
    CapitalField,
    Capital,
    Department,
    accumulate,
)
from typing import List, Tuple, TypeAlias


CVM: TypeAlias = Tuple[float, float, float]
TwoDept: TypeAlias = Tuple[CVM, CVM]
DepartmentChanges: TypeAlias = List[TwoDept]


def add_data_to_list(
    department_changes: DepartmentChanges, dept_1: Department, dept_2: Department
) -> None:
    department_changes.append(
        (
            (
                dept_1.constant_capital.value,
                dept_1.variable_capital.value,
                dept_1.surplus_value.value,
            ),
            (
                dept_2.constant_capital.value,
                dept_2.variable_capital.value,
                dept_2.surplus_value.value,
            ),
        )
    )


dept_1: Department = Department(name="Department 1")

dept_1.constant_capital = Capital(
    value=4000,
    owner="capitalist",
    is_capital=True,
    form_producing_surplus_value=CapitalFormProducingSurplusValue.CONSTANT,
    form_liquidity=CapitalFormLiquidity.OTHER,
    form_circulation=CapitalFormCirculation.PRODUCTION,
    form_mean=CapitalFormMean.PRODUCTION_MEANS,
    form_physical=CapitalFormExistence.PHYSICAL,
    field=CapitalField.INDUSTRIAL,
)

dept_1.variable_capital = Capital(
    value=1000,
    owner="capitalist",
    is_capital=True,
    form_producing_surplus_value=CapitalFormProducingSurplusValue.VARIABLE,
    form_liquidity=CapitalFormLiquidity.CIRCULATING,
    form_circulation=CapitalFormCirculation.PRODUCTION,
    form_mean=CapitalFormMean.LABOUR_FORCE,
    form_physical=CapitalFormExistence.LABOUR_FORCE,
    field=CapitalField.INDUSTRIAL,
)

dept_1.surplus_value = Capital(
    value=0,
    owner="capitalist",
    is_capital=True,
    form_producing_surplus_value=CapitalFormProducingSurplusValue.SURPLUS_VALUE,
    form_liquidity=CapitalFormLiquidity.CIRCULATING,
    form_circulation=CapitalFormCirculation.COMMODITY,
    form_mean=CapitalFormMean.PRODUCTION_MEANS,
    form_physical=CapitalFormExistence.PHYSICAL,
    field=CapitalField.INDUSTRIAL,
)

dept_2: Department = Department(name="Department 2")

dept_2.constant_capital = Capital(
    value=1500,
    owner="capitalist",
    is_capital=True,
    form_producing_surplus_value=CapitalFormProducingSurplusValue.CONSTANT,
    form_liquidity=CapitalFormLiquidity.OTHER,
    form_circulation=CapitalFormCirculation.PRODUCTION,
    form_mean=CapitalFormMean.PRODUCTION_MEANS,
    form_physical=CapitalFormExistence.PHYSICAL,
    field=CapitalField.INDUSTRIAL,
)

dept_2.variable_capital = Capital(
    value=750,
    owner="capitalist",
    is_capital=True,
    form_producing_surplus_value=CapitalFormProducingSurplusValue.VARIABLE,
    form_liquidity=CapitalFormLiquidity.CIRCULATING,
    form_circulation=CapitalFormCirculation.PRODUCTION,
    form_mean=CapitalFormMean.LABOUR_FORCE,
    form_physical=CapitalFormExistence.LABOUR_FORCE,
    field=CapitalField.INDUSTRIAL,
)

dept_2.surplus_value = Capital(
    value=0,
    owner="capitalist",
    is_capital=True,
    form_producing_surplus_value=CapitalFormProducingSurplusValue.SURPLUS_VALUE,
    form_liquidity=CapitalFormLiquidity.CIRCULATING,
    form_circulation=CapitalFormCirculation.COMMODITY,
    form_mean=CapitalFormMean.CONSUMPTION_MEANS,
    form_physical=CapitalFormExistence.PHYSICAL,
    field=CapitalField.INDUSTRIAL,
)

department_changes: DepartmentChanges = []
add_data_to_list(department_changes, dept_1, dept_2)

year_reproduct: int = int(input("Year(s) of Reproduction: "))
for i in range(1, year_reproduct + 1):
    print(f"\nYear {i}:")

    print("\nOriginal Status:")
    print(dept_1)
    print(dept_2)

    print("\nProduction:")
    surplus_value_rate_of_dept_1: float = float(
        input("Surplus Value Rate of Dept1(1.00 for example): ")
    )
    surplus_value_rate_of_dept_2: float = float(
        input("Surplus Value Rate of Dept2(1.00 for example): ")
    )

    dept_1.produce(surplus_value_rate_of_dept_1)
    dept_2.produce(surplus_value_rate_of_dept_2)

    dept_1.constant_capital.transform(
        CapitalFormCirculation,
        CapitalFormCirculation.PRODUCTION,
        CapitalFormCirculation.COMMODITY,
    )
    dept_1.variable_capital.transform(
        CapitalFormCirculation,
        CapitalFormCirculation.PRODUCTION,
        CapitalFormCirculation.COMMODITY,
    )
    dept_1.variable_capital.transform(
        CapitalFormMean, CapitalFormMean.LABOUR_FORCE, CapitalFormMean.PRODUCTION_MEANS
    )
    dept_1.variable_capital.transform(
        CapitalFormExistence,
        CapitalFormExistence.LABOUR_FORCE,
        CapitalFormExistence.PHYSICAL,
    )
    dept_2.constant_capital.transform(
        CapitalFormCirculation,
        CapitalFormCirculation.PRODUCTION,
        CapitalFormCirculation.COMMODITY,
    )
    dept_2.constant_capital.transform(
        CapitalFormMean,
        CapitalFormMean.PRODUCTION_MEANS,
        CapitalFormMean.CONSUMPTION_MEANS,
    )
    dept_2.variable_capital.transform(
        CapitalFormCirculation,
        CapitalFormCirculation.PRODUCTION,
        CapitalFormCirculation.COMMODITY,
    )
    dept_2.variable_capital.transform(
        CapitalFormMean, CapitalFormMean.LABOUR_FORCE, CapitalFormMean.CONSUMPTION_MEANS
    )
    dept_2.variable_capital.transform(
        CapitalFormExistence,
        CapitalFormExistence.LABOUR_FORCE,
        CapitalFormExistence.PHYSICAL,
    )

    print(dept_1)
    print(dept_2)

    print("\nAccumulation:")
    m_accumulate_rate_of_dept_1: float = float(
        input("Accumulate Rate of Surplus Value of Dept1(0.5 for example): ")
    )

    accumulate(dept_1, dept_2, m_accumulate_rate_of_dept_1)

    dept_1.constant_capital.transform(
        CapitalFormCirculation,
        CapitalFormCirculation.COMMODITY,
        CapitalFormCirculation.PRODUCTION,
    )
    dept_1.variable_capital.transform(
        CapitalFormCirculation,
        CapitalFormCirculation.COMMODITY,
        CapitalFormCirculation.PRODUCTION,
    )
    dept_1.variable_capital.transform(
        CapitalFormMean, CapitalFormMean.PRODUCTION_MEANS, CapitalFormMean.LABOUR_FORCE
    )
    dept_1.variable_capital.transform(
        CapitalFormExistence,
        CapitalFormExistence.PHYSICAL,
        CapitalFormExistence.LABOUR_FORCE,
    )
    dept_2.constant_capital.transform(
        CapitalFormCirculation,
        CapitalFormCirculation.COMMODITY,
        CapitalFormCirculation.PRODUCTION,
    )
    dept_2.constant_capital.transform(
        CapitalFormMean,
        CapitalFormMean.CONSUMPTION_MEANS,
        CapitalFormMean.PRODUCTION_MEANS,
    )
    dept_2.variable_capital.transform(
        CapitalFormCirculation,
        CapitalFormCirculation.COMMODITY,
        CapitalFormCirculation.PRODUCTION,
    )
    dept_2.variable_capital.transform(
        CapitalFormMean, CapitalFormMean.CONSUMPTION_MEANS, CapitalFormMean.LABOUR_FORCE
    )
    dept_2.variable_capital.transform(
        CapitalFormExistence,
        CapitalFormExistence.PHYSICAL,
        CapitalFormExistence.LABOUR_FORCE,
    )

    print(dept_1)
    print(dept_2)

    print("\nConsumption of Surplus Value:")
    dept_1.surplus_value.decrease(dept_1.surplus_value.value)
    dept_2.surplus_value.decrease(dept_2.surplus_value.value)

    print(dept_1)
    print(dept_2)

    add_data_to_list(department_changes, dept_1, dept_2)

print("\nDepartment Changes:")
print(department_changes)
