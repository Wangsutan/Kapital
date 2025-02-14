import sys
import pandas as pd
import matplotlib.pyplot as plt


profit_rate_general = float(sys.argv[1])
transform_rate_from_super_profit_to_rent = float(sys.argv[2])
excel_file_path = sys.argv[3]
excel_sheet_name = sys.argv[4]


df = pd.read_excel(
    excel_file_path,    # "series_1.xlsx",
    usecols=[
        "type", "area", "capitalAdvanced", "productNum"
    ],
    index_col=0,
    sheet_name=excel_sheet_name,    # "Ⅱ",
)

df["product_force"] = df.productNum / df.capitalAdvanced / df.area
df.sort_values(by="product_force", ascending=False)

df["capital_advanced_per_area"] = df.capitalAdvanced / df.area

df["product_num_per_area"] = df.productNum / df.area

product_cost_per_production_avg = df.iloc[0].capitalAdvanced / \
    df.iloc[0].productNum
product_price_per_production_avg = (
    1.0 + profit_rate_general) * product_cost_per_production_avg

df["product_cost_per_production"] = df.capitalAdvanced / df.productNum
df["product_price_per_production"] = (
    1.0 + profit_rate_general) * df.product_cost_per_production

df["product_value"] = df.productNum * product_price_per_production_avg

df["product_value_per_area"] = df.product_value / df.area

df["gross_profit_currency"] = df.product_value - df.capitalAdvanced
df["gross_profit_currency_per_area"] = df.gross_profit_currency / df.area

df["gross_profit_physical"] = df.gross_profit_currency / \
    product_price_per_production_avg
df["gross_profit_physical_per_area"] = df.gross_profit_physical / df.area

df["gross_super_profit_currency"] = df.gross_profit_currency - \
    df.capitalAdvanced * profit_rate_general
df["gross_super_profit_currency_per_area"] = df.gross_super_profit_currency / df.area

df["gross_super_profit_physical"] = df.gross_super_profit_currency / \
    product_price_per_production_avg
df["gross_super_profit_physical_per_area"] = df.gross_super_profit_physical / df.area

df["rent_currency"] = df.gross_super_profit_currency * \
    transform_rate_from_super_profit_to_rent
df["rent_currency_per_area"] = df.rent_currency / df.area

df["rent__physical"] = df.rent_currency / product_price_per_production_avg
df["rent__physical_per_area"] = df.rent__physical / df.area

df["gross_profit_rate"] = df.gross_profit_currency / df.capitalAdvanced
df["gross_profit_rate_per_area"] = df.gross_profit_rate / df.area

df["rent_rate"] = df.rent_currency / df.capitalAdvanced
df["rent_rate_per_area"] = df.rent_rate / df.area

df.to_excel("df_output_" + excel_file_path, sheet_name=excel_sheet_name)

df.product_force.plot.bar()
plt.show()

df.product_value.plot.bar()
plt.show()
