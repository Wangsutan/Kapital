市场价值可以根据加权平均数的方式进行计算，公式如下：

$$市场价值 = \frac{\sum_{i=1}^{n}商品数量_i \cdot 商品价值_i}{\sum_{i=1}^{n} 商品数量_i}$$

相应代码如下：

[[market_value_simple.py]]

```

```

在这份代码中，商品数量和商品价值分别存放在两个列表中，并且函数`calc_market_value`将这两个列表作为自己的参数进行计算。其中值得注意的是这行代码：

```
weighted_values_sum = sum(q * v for q, v in zip(good_quantities, good_values))
````

这行代码通过`zip`函数将`good_quantities`和`good_values`中的数量相等的元素打包成一个个元组`(q, v)`，然后通过一个生成器表达式，计算每个商品的价值乘以数量的结果，最后使用`sum`函数将这些结果进行加总，得到`weighted_values_sum`。

此后的代码逻辑比较简单。获取商品的总数量`good_quantity_total`之后，用商品的经过加权的总价值`weighted_values_sum`除以上述的总数量，可得商品的市场价值。

运行这份代码，结果如下：

```
Market Value: 13.62
```
