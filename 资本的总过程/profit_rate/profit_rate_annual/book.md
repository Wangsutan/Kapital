# 利润率关于剩余价值率和可变资本年度周转次数的函数关系

在其他条件不变的情况下，剩余价值率和可变资本年度周转次数决定利润率。根据这种原理，可以设计如下代码：

```
```

函数`calc_profit_rate`通过剩余价值率、可变资本年度周转次数以及不变资本量和可变资本量，来计算利润率。计算方式如下：

$$利润率 = \frac{可变资本年度周转次数 \times 剩余价值率 \times 可变资本}{不变资本 + 可变资本}.$$

在代码中，假设原初的不变资本和可变资本分别为80和20。

创建两个线性空间`surplus_value_rates`和`turnover_nums_of_variable_capital_annual`，分别表示剩余价值率和可变资本年度周转次数的变化。接着，使用`np.meshgrid`创建两个网格数组`surplus_value_rate_grid`和`turnover_nums_of_variable_capital_annual_grid`，用于在后面绘制3D图表。

调用`calc_profit_rate`函数来计算`profit_rates`。该数据对应3D图表中的z轴数据。

最后，根据`surplus_value_rate_grid`、`turnover_nums_of_variable_capital_annual_grid`和`profit_rates`，绘制一份3D图形。其中，x轴代表剩余价值率，y轴代表可变资本年度周转次数，z轴代表利润率。

所得图形如下：

![[价值转型/profit_rate/Figure_1.png]]
