from enum import Enum


class Value:
    def __init__(self, value: float = 0, owner: str = "None", is_capital: bool = False):
        self.value = value
        self.owner = owner
        self.is_capital = is_capital

    def increase(self, value: float) -> None:
        self.value += value

    def decrease(self, value: float) -> None:
        self.value -= value

    def change_owner(self, new_owner: str) -> None:
        self.owner = new_owner


class CapitalFormProducingSurplusValue(Enum):
    CONSTANT = "constant capital"
    VARIABLE = "variable capital"
    SURPLUS_VALUE = "surplus value"
    OTHER = "other"


class CapitalFormLiquidity(Enum):
    FIXED = "fixed capital"
    CIRCULATING = "circulating capital"
    OTHER = "other"


class CapitalFormCirculation(Enum):
    PRODUCTION = "production capital"
    COMMODITY = "commodity capital"
    MONEY = "money capital"
    OTHER = "other"


class CapitalFormMean(Enum):
    PRODUCTION_MEANS = "production means"
    CONSUMPTION_MEANS = "consumption means"
    LABOUR_FORCE = "labour force"
    MONEY = "money"
    OTHER = "other"


class CapitalFormExistence(Enum):
    PHYSICAL = "physical"
    MONEY = "money"
    LABOUR_FORCE = "labour force"
    OTHER = "other"


class CapitalField(Enum):
    INDUSTRIAL = "industrial capital"
    COMMERCIAL = "commercial capital"
    BANK = "bank capital"
    OTHER = "other"


class Capital(Value):
    def __init__(
        self,
        value: float = 0,
        owner: str = "capitalist",
        is_capital: bool = True,
        form_producing_surplus_value: CapitalFormProducingSurplusValue = CapitalFormProducingSurplusValue.CONSTANT,
        form_liquidity: CapitalFormLiquidity = CapitalFormLiquidity.FIXED,
        form_circulation: CapitalFormCirculation = CapitalFormCirculation.PRODUCTION,
        form_mean: CapitalFormMean = CapitalFormMean.PRODUCTION_MEANS,
        form_physical: CapitalFormExistence = CapitalFormExistence.PHYSICAL,
        field: CapitalField = CapitalField.INDUSTRIAL,
    ) -> None:
        super().__init__(value, owner, is_capital)
        self.form_producing_surplus_value = form_producing_surplus_value
        self.form_liquidity = form_liquidity
        self.form_circulation = form_circulation
        self.form_mean = form_mean
        self.form_physical = form_physical
        self.field = field

    def __str__(self):
        return (
            f"Capital\nValue: {self.value}\nOwner: {self.owner}\n"
            f"Capital form producing surplus value: {self.form_producing_surplus_value}\n"
            f"Capital form liquidity: {self.form_liquidity}\n"
            f"Capital form circulation: {self.form_circulation}\n"
            f"Capital form mean: {self.form_mean}\n"
            f"Capital form physical: {self.form_physical}\n"
            f"Field: {self.field}\n"
        )

    def transform(self, form_class, form_src, form_dest):
        if not isinstance(form_class, type) or not issubclass(form_class, Enum):
            raise ValueError("form_class must be an Enum subclass")
        if form_src.name not in form_class.__members__:
            raise ValueError(f"{form_src} is not a valid member of {form_class}")
        if form_dest.name not in form_class.__members__:
            raise ValueError(f"{form_dest} is not a valid member of {form_class}")

        if (
            form_class == CapitalFormProducingSurplusValue
            and self.form_producing_surplus_value != form_src
        ):
            raise ValueError(
                f"Source form {form_src} does not match current form {self.form_producing_surplus_value}"
            )
        if form_class == CapitalFormLiquidity and self.form_liquidity != form_src:
            raise ValueError(
                f"Source form {form_src} does not match current form {self.form_liquidity}"
            )
        if form_class == CapitalFormCirculation and self.form_circulation != form_src:
            raise ValueError(
                f"Source form {form_src} does not match current form {self.form_circulation}"
            )
        if form_class == CapitalFormMean and self.form_mean != form_src:
            raise ValueError(
                f"Source form {form_src} does not match current form {self.form_mean}"
            )
        if form_class == CapitalFormExistence and self.form_physical != form_src:
            raise ValueError(
                f"Source form {form_src} does not match current form {self.form_physical}"
            )
        if form_class == CapitalField and self.field != form_src:
            raise ValueError(
                f"Source form {form_src} does not match current field {self.field}"
            )

        if form_class == CapitalFormProducingSurplusValue:
            self.form_producing_surplus_value = form_dest
        elif form_class == CapitalFormLiquidity:
            self.form_liquidity = form_dest
        elif form_class == CapitalFormCirculation:
            self.form_circulation = form_dest
        elif form_class == CapitalFormMean:
            self.form_mean = form_dest
        elif form_class == CapitalFormExistence:
            self.form_physical = form_dest
        elif form_class == CapitalField:
            self.field = form_dest
        else:
            raise ValueError(f"Unknown form class {form_class}")


class Income(Value):
    def __init__(
        self,
        value: float = 0,
        owner: str = "worker",
        form: str = "money",
        is_capital: bool = False,
    ) -> None:
        super().__init__(value, owner, is_capital)
        self.form = form

    def earn(self, value):
        self.increase(value)

    def spend(self, value):
        self.decrease(value)


class Department:
    def __init__(
        self,
        name: str = "",
        constant_capital_value: float = 0,
        variable_capital_value: float = 0,
        surplus_value: float = 0,
        money: float = 0,
        income_capitalist: float = 0,
        income_worker: float = 0,
    ) -> None:
        self.name = name
        self.constant_capital = Capital()
        self.variable_capital = Capital()
        self.surplus_value = Capital()

        self.money = Capital(
            value=money,
            owner="capitalist",
            is_capital=True,
            form_producing_surplus_value=CapitalFormProducingSurplusValue.OTHER,
            form_liquidity=CapitalFormLiquidity.CIRCULATING,
            form_circulation=CapitalFormCirculation.MONEY,
            form_mean=CapitalFormMean.MONEY,
            form_physical=CapitalFormExistence.MONEY,
            field=CapitalField.INDUSTRIAL,
        )

        self.income_capitalist = Income(
            income_capitalist, "capitalist", "money", is_capital=False
        )
        self.income_worker = Income()

    def produce(self, surplus_value_rate):
        self.surplus_value.increase(self.variable_capital.value * surplus_value_rate)

    def __str__(self):
        return f"{self.name}\t{self.constant_capital.value:.2f}c\t{self.variable_capital.value:.2f}v\t{self.surplus_value.value:.2f}m"


def accumulate(
    dept_1: Department,
    dept_2: Department,
    m_accumulate_rate_of_dept_1: float,
):
    m_accumulated_of_dept_1: float = (
        dept_1.surplus_value.value * m_accumulate_rate_of_dept_1
    )

    m_reinvest_rate_to_c_of_dept_1: float = dept_1.constant_capital.value / (
        dept_1.constant_capital.value + dept_1.variable_capital.value
    )
    v_c_rate_of_dept_2: float = (
        dept_2.variable_capital.value / dept_2.constant_capital.value
    )

    # Accumulation of department 1:
    dept_1.surplus_value.decrease(m_accumulated_of_dept_1)
    dept_1.constant_capital.increase(
        m_accumulated_of_dept_1 * m_reinvest_rate_to_c_of_dept_1
    )
    dept_1.variable_capital.increase(
        m_accumulated_of_dept_1 * (1.0 - m_reinvest_rate_to_c_of_dept_1)
    )

    # Accumulation of department 2:
    m_accumulated_to_c_of_dept_2: float = (
        dept_1.variable_capital.value
        + dept_1.surplus_value.value
        - dept_2.constant_capital.value
    )
    dept_2.constant_capital.increase(m_accumulated_to_c_of_dept_2)

    m_accumulated_to_v_of_dept_2: float = (
        dept_2.constant_capital.value * v_c_rate_of_dept_2
        - dept_2.variable_capital.value
    )
    dept_2.variable_capital.increase(m_accumulated_to_v_of_dept_2)

    dept_2.surplus_value.decrease(
        m_accumulated_to_c_of_dept_2 + m_accumulated_to_v_of_dept_2
    )
