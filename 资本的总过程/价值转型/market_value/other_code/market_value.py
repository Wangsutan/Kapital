import pandas as pd


excel_path = 'values.xlsx'
df = pd.read_excel(excel_path)

weighted_values = df['value'] * df['num']
total_weight = df['num'].sum()
market_value = weighted_values.sum() / total_weight

print(f"market_value: {market_value:.2f}")
