import pandas as pd


columns = ["c", "v", "svr"]

p1 = [1, 1, 0.6]
p2 = [2, 1, 1.0]
p3 = [1, 1.5, 1.2]

p_list = [p1, p2, p3]
df = pd.DataFrame(p_list, columns=columns)

df["m"] = df.v * df.svr

df["value"] = df.c + df.v + df.m

m_total = df.m.sum()
print(f"m_total: {m_total}")

investment_total = df.c.sum() + df.v.sum()
print(f"investment_total: {investment_total}")

profit_rate = m_total / investment_total
print(f"profit_rate: {profit_rate}")

df["product_price"] = (df.c + df.v) * (1 + profit_rate)

df["value_product_price_diff"] = df.value - df.product_price

print(df)

print("\nvalue_product_price_diff > 0.0")
print(df[df["value_product_price_diff"] > 0.0])

profit_total = (df.c.sum() + df.v.sum()) * profit_rate
print(f"profit_total: {profit_total}")

if m_total == profit_total:
    print("m_total == profit_total\n")

value_total = df.value.sum()
print(f"value_total: {value_total}")

product_price_total = df.product_price.sum()
print(f"product_price_total: {product_price_total}")

if value_total == product_price_total:
    print("value_total == product_price_total\n")
