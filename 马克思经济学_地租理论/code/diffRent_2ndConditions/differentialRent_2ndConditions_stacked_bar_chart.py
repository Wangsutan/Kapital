import pandas as pd
import matplotlib.pyplot as plt


plt.style.use("fivethirtyeight")

df = pd.read_excel(
    "differentialRent_2ndConditions.xlsx",
   	usecols=[
            "type", "capitalAdvanced", "profitValue", "rentValue"
        ],
    index_col=0
)

df.profitValue = df.profitValue - df.rentValue

plt.bar(
    df.index,
    df.capitalAdvanced,
    label="capitalAdvanced"
)

plt.bar(
    df.index,
    df.profitValue,
    bottom=df.capitalAdvanced,
    label="profitValue"
)

plt.bar(
    df.index,
    df.rentValue,
    bottom=df.capitalAdvanced + df.profitValue,
    label="rentValue"
)

plt.xlabel("type of soil")
plt.ylabel("type of value")
plt.legend()
plt.title("allocation of values include differential rents")

plt.show()
