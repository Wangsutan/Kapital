import pandas as pd


filePath = '茶叶蛋生产要素表_简单.xlsx'
df = pd.read_excel(filePath, index_col='生产要素')

value = df['数量'].dot(df['单价'])
print(f"value: {value:.2f}")
