import pandas as pd


excel_file_path = "datas.xlsx"
df = pd.read_excel(excel_file_path, index_col=None)

df["surplusValue"] = df["variableCapital"] * df["surplusValueRate"]
df["profitRate"] = df["surplusValue"] / (df["constantCapital"] + df["variableCapital"])
df["costPrice"] = df["constantCapitalUsed"] + df["variableCapital"]
df["value"] = df["constantCapitalUsed"] + df["variableCapital"] + df["surplusValue"]

profitRateGeneral = df["surplusValue"].sum() / (
    df["constantCapital"].sum() + df["variableCapital"].sum()
)
print(f"General Profit Rate: {profitRateGeneral}")

df["priceOfProduction"] = (
    df["costPrice"]
    + (df["constantCapital"] + df["variableCapital"]) * profitRateGeneral
)

df["diffOfPriceOfProductionAndValue"] = df["priceOfProduction"] - df["value"]

print(df[["costPrice", "value", "priceOfProduction", "diffOfPriceOfProductionAndValue"]])
