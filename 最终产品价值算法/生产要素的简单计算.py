import pandas as pd


filePath = '茶叶蛋生产要素表_简单.xlsx'
df = pd.read_excel(filePath, index_col='生产要素')

values = pd.DataFrame(df['数量'] * df['单价'], columns=['总价'])
print("values:", values)

value = df['数量'].dot(df['单价'])
print("\nvalue:", value)
