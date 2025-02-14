# Python：求商品的价值与生产价格之差

近期，学习绝对地租相关理论，得知绝对地租若想成立，则土地产品的实际的市场价格需要满足以下条件：

$$价值 \geq 市场价格 > 生产价格$$

现在设计一份Python代码，自动计算商品的价值与生产价格的差。

代码如下：

```
```

运行结果如下：

```
m_total: 3.4
investment_total: 7.5
profit_rate: 0.4533333333333333
   c    v  svr    m  value  product_price  value_product_price_diff
0  1  1.0  0.6  0.6    2.6       2.906667                 -0.306667
1  2  1.0  1.0  1.0    4.0       4.360000                 -0.360000
2  1  1.5  1.2  1.8    4.3       3.633333                  0.666667

value_product_price_diff > 0.0
   c    v  svr    m  value  product_price  value_product_price_diff
2  1  1.5  1.2  1.8    4.3       3.633333                  0.666667
profit_total: 3.4
m_total == profit_total

value_total: 10.899999999999999
product_price_total: 10.9

```

注意，由于计算的精度问题，这里的`value_total`不等于`product_price_total`，但我们很容易看出来它们之间的误差极小。

---

另外，据了解（从徐禾的教材《政治经济学概论》），在农业生产的资本有机构成高于社会平均水平时，绝对地租是可以不存在的。