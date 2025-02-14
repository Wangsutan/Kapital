import pandas as pd

myColumns = [
    "Acres",
    "Price of Production Per Acre",
    "Price of Production Total",
    "Product",
    "Rent in Grain",
    "Rent in Money"
]

myIndex = ["A", "B", "C", "D"]

# # sheelⅠ
# df = pd.DataFrame(index=myIndex, columns=myColumns)
# df.loc["A"] = [1, 3, 3, 1, 0, 0]
# df.loc["B"] = [1, 3, 3, 2, 1, 3]
# df.loc["C"] = [1, 3, 3, 3, 2, 6]
# df.loc["D"] = [1, 3, 3, 4, 3, 9]

# sheelⅠa
df = pd.DataFrame(index=myIndex, columns=myColumns)
df.loc["A"] = [2, 3, 6, 2, 0, 0]
df.loc["B"] = [2, 3, 6, 4, 2, 6]
df.loc["C"] = [2, 3, 6, 6, 4, 12]
df.loc["D"] = [2, 3, 6, 8, 6, 18]


print(df["Acres"].sum())
print(df["Price of Production Total"].sum())
print(df["Product"].sum())
print(df["Rent in Grain"].sum())
print(df["Rent in Money"].sum())
