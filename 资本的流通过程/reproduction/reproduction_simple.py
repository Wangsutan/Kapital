from department import (
    CapitalFormProducingSurplusValue,
    CapitalFormLiquidity,
    CapitalFormCirculation,
    CapitalFormMean,
    CapitalFormExistence,
    CapitalField,
    Capital,
    Income,
    Department,
)


dept_1: Department = Department(name="Department 1")

dept_1.constant_capital = Capital(
    value=4000,
    owner="capitalist",
    is_capital=True,
    form_producing_surplus_value=CapitalFormProducingSurplusValue.CONSTANT,
    form_liquidity=CapitalFormLiquidity.OTHER,
    form_circulation=CapitalFormCirculation.COMMODITY,
    form_mean=CapitalFormMean.PRODUCTION_MEANS,
    form_physical=CapitalFormExistence.PHYSICAL,
    field=CapitalField.INDUSTRIAL,
)

dept_1.variable_capital = Capital(
    value=1000,
    owner="capitalist",
    is_capital=True,
    form_producing_surplus_value=CapitalFormProducingSurplusValue.VARIABLE,
    form_liquidity=CapitalFormLiquidity.OTHER,
    form_circulation=CapitalFormCirculation.COMMODITY,
    form_mean=CapitalFormMean.PRODUCTION_MEANS,
    form_physical=CapitalFormExistence.PHYSICAL,
    field=CapitalField.INDUSTRIAL,
)

dept_1.surplus_value = Capital(
    value=1000,
    owner="capitalist",
    is_capital=True,
    form_producing_surplus_value=CapitalFormProducingSurplusValue.SURPLUS_VALUE,
    form_liquidity=CapitalFormLiquidity.OTHER,
    form_circulation=CapitalFormCirculation.COMMODITY,
    form_mean=CapitalFormMean.PRODUCTION_MEANS,
    form_physical=CapitalFormExistence.PHYSICAL,
    field=CapitalField.INDUSTRIAL,
)

dept_1.income_worker = Income(value=1000, owner="worker")

dept_2: Department = Department(name="Department 2")

dept_2.constant_capital = Capital(
    value=2000,
    owner="capitalist",
    is_capital=True,
    form_producing_surplus_value=CapitalFormProducingSurplusValue.CONSTANT,
    form_liquidity=CapitalFormLiquidity.OTHER,
    form_circulation=CapitalFormCirculation.COMMODITY,
    form_mean=CapitalFormMean.CONSUMPTION_MEANS,
    form_physical=CapitalFormExistence.PHYSICAL,
    field=CapitalField.INDUSTRIAL,
)

dept_2.variable_capital = Capital(
    value=500,
    owner="capitalist",
    is_capital=True,
    form_producing_surplus_value=CapitalFormProducingSurplusValue.VARIABLE,
    form_liquidity=CapitalFormLiquidity.OTHER,
    form_circulation=CapitalFormCirculation.COMMODITY,
    form_mean=CapitalFormMean.CONSUMPTION_MEANS,
    form_physical=CapitalFormExistence.PHYSICAL,
    field=CapitalField.INDUSTRIAL,
)

dept_2.surplus_value = Capital(
    value=500,
    owner="capitalist",
    is_capital=True,
    form_producing_surplus_value=CapitalFormProducingSurplusValue.SURPLUS_VALUE,
    form_liquidity=CapitalFormLiquidity.OTHER,
    form_circulation=CapitalFormCirculation.COMMODITY,
    form_mean=CapitalFormMean.CONSUMPTION_MEANS,
    form_physical=CapitalFormExistence.PHYSICAL,
    field=CapitalField.INDUSTRIAL,
)

dept_2.income_worker = Income(value=500, owner="worker")

year_reproduct: int = int(input("Year(s) of Reproduction: "))
for i in range(1, year_reproduct + 1):
    print(f"\nYear {i}:")

    print("\nOriginal Status:")
    print(dept_1)
    print(dept_2)

    print("\nExchange and Consumption:")
    # step 1
    dept_1.constant_capital.transform(
        CapitalFormCirculation,
        CapitalFormCirculation.COMMODITY,
        CapitalFormCirculation.PRODUCTION,
    )

    # step 2
    value_temp = dept_1.income_worker.value
    dept_1.income_worker.spend(value_temp)
    dept_2.money.increase(value_temp)
    dept_2.constant_capital.decrease(value_temp)

    # step 3
    dept_2.money.decrease(value_temp)
    dept_1.money.increase(value_temp)
    dept_1.variable_capital.decrease(value_temp)
    dept_2.constant_capital.increase(value_temp)
    dept_2.constant_capital.transform(
        CapitalFormCirculation,
        CapitalFormCirculation.COMMODITY,
        CapitalFormCirculation.OTHER,  # mixed
    )
    dept_2.constant_capital.transform(
        CapitalFormMean,
        CapitalFormMean.CONSUMPTION_MEANS,
        CapitalFormMean.OTHER,  # mixed
    )

    # step 4
    dept_2.constant_capital.transform(
        CapitalFormCirculation,
        CapitalFormCirculation.OTHER,
        CapitalFormCirculation.PRODUCTION,
    )
    dept_2.constant_capital.transform(
        CapitalFormMean,
        CapitalFormMean.OTHER,
        CapitalFormMean.PRODUCTION_MEANS,
    )
    dept_1.surplus_value.transform(
        CapitalFormMean,
        CapitalFormMean.PRODUCTION_MEANS,
        CapitalFormMean.CONSUMPTION_MEANS,
    )

    # step 5
    dept_1.money.decrease(value_temp)
    dept_1.income_worker.increase(value_temp)
    dept_1.variable_capital.increase(value_temp)
    dept_1.variable_capital.transform(
        CapitalFormCirculation,
        CapitalFormCirculation.COMMODITY,
        CapitalFormCirculation.PRODUCTION,
    )
    dept_1.variable_capital.transform(
        CapitalFormMean,
        CapitalFormMean.PRODUCTION_MEANS,
        CapitalFormMean.LABOUR_FORCE,
    )
    dept_1.variable_capital.transform(
        CapitalFormExistence,
        CapitalFormExistence.PHYSICAL,
        CapitalFormExistence.LABOUR_FORCE,
    )

    # step 6
    value_temp = dept_2.income_worker.value
    dept_2.income_worker.spend(value_temp)
    dept_2.money.increase(value_temp)
    dept_2.variable_capital.decrease(value_temp)

    # step 7
    dept_2.money.decrease(value_temp)
    dept_2.variable_capital.increase(value_temp)
    dept_2.variable_capital.transform(
        CapitalFormCirculation,
        CapitalFormCirculation.COMMODITY,
        CapitalFormCirculation.PRODUCTION,
    )
    dept_2.variable_capital.transform(
        CapitalFormMean,
        CapitalFormMean.CONSUMPTION_MEANS,
        CapitalFormMean.LABOUR_FORCE,
    )
    dept_2.variable_capital.transform(
        CapitalFormExistence,
        CapitalFormExistence.PHYSICAL,
        CapitalFormExistence.LABOUR_FORCE,
    )

    # step 8
    dept_1.surplus_value.decrease(dept_1.surplus_value.value)
    dept_1.surplus_value.transform(
        CapitalFormMean,
        CapitalFormMean.CONSUMPTION_MEANS,
        CapitalFormMean.PRODUCTION_MEANS,
    )

    # step 9
    dept_2.surplus_value.decrease(dept_2.surplus_value.value)

    print(dept_1)
    print(dept_2)

    print("\nProduction:")
    surplus_value_rate_of_dept_1: float = 1.0
    surplus_value_rate_of_dept_2: float = 1.0

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
        CapitalFormMean,
        CapitalFormMean.LABOUR_FORCE,
        CapitalFormMean.PRODUCTION_MEANS,
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
        CapitalFormMean,
        CapitalFormMean.LABOUR_FORCE,
        CapitalFormMean.CONSUMPTION_MEANS,
    )
    dept_2.variable_capital.transform(
        CapitalFormExistence,
        CapitalFormExistence.LABOUR_FORCE,
        CapitalFormExistence.PHYSICAL,
    )

    print(dept_1)
    print(dept_2)
