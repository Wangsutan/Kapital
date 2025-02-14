import pandas as pd
import matplotlib.pyplot as plt


plt.rcParams['font.family'] = ['Source Han Sans CN']

df = pd.read_excel("goods_instant.xlsx")
df["price_total"] = df.quantity * df.price

good_price_sum = df.price_total.sum()
labour_force_value = good_price_sum
print(f"labour_force_value_annual: {labour_force_value:.2f}")
print(f"labour_force_value_monthly: {labour_force_value / 12:.2f}\n")

data_grouped = df.groupby(['class_lv1']).agg(
    {'price_total': 'sum'}).reset_index()

data_grouped_sorted = data_grouped.sort_values(
    by='price_total', ascending=False)

plt.pie(
    data_grouped_sorted["price_total"],
    labels=data_grouped_sorted['class_lv1'],
    autopct='%1.2f%%',
)

plt.title("分类别消费数据")
plt.axis('equal')
plt.tight_layout()

plt.show()
