# Python：根据劳动者的年度消费情况计算劳动力价值

假设一个劳动者年度消费情况如下表所示：

```
good	quantity	price
rice	10000	1
bread	5000	3
vegetable	8000	4
fruit	2000	5
home	1	200
traffic	700	4
clothes	20	100
```

这当然是一个简化的实例，但对于这里的理论要求而言已经足够。

我们设计一个函数，来计算这些商品的总价格。代码如下：

```
def calculate_goods_value(good_item_list, good_quantity_list, good_price_list):
    goods_value_total = 0
    for i in range(len(good_item_list)):
        good_item_value = good_quantity_list[i] * good_price_list[i]
        goods_value_total += good_item_value

    return goods_value_total
```

在一个抽象的环节上，这个商品总价格可以对应为劳动力价值。

我们是把相关数据存放在一个表格中，并通过Pandas读取这个表格，然后进行相应的数据计算。

完整代码如下：

```
import pandas as pd


def calculate_goods_value(good_item_list, good_quantity_list, good_price_list):
    goods_value_total = 0
    for i in range(len(good_item_list)):
        good_item_value = good_quantity_list[i] * good_price_list[i]
        goods_value_total += good_item_value

    return goods_value_total


df = pd.read_excel('goods.xlsx')
print(df)

good_item_list = list(df["good"])
good_quantity_list = list(df["quantity"])
good_price_list = list(df["price"])

goods_value_total = calculate_goods_value(
    good_item_list, good_quantity_list, good_price_list)

labour_force_value_annual = goods_value_total
print("labour_force_value_annual:", labour_force_value_annual)
print("labour_force_value_monthly:", labour_force_value_annual / 12)

```

运行结果如下：

```
        good  quantity  price
0       rice     10000      1
1      bread      5000      3
2  vegetable      8000      4
3      fruit      2000      5
4       home         1    200
5    traffic       700      4
6    clothes        20    100
labour_force_value_annual: 72000
labour_force_value_monthly: 6000.0

```

运算结果比较凑巧，正好算出劳动者的月薪为6000.00元。
