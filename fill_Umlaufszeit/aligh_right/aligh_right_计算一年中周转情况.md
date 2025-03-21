# Python与《资本论》：根据年度周转期间之原始数据，计算周转相关情况

我们可以通过“再生产甘特图”相关代码，获取特定假设下的年度周转期间之原始数据。

对此原始数据，我们可以展开更深入的分析。

代码如下：

```

```

设定了一个年度周数，以此为依据，判断特定的周转是否属于本年度，是否已完成。

根据已完成、未完成等区别，统计以下数据：

- 本年度已完成周转数；

- 本年度未完成周转数；

- 本年度未完成周转情况；

- 本年度劳动周数和流通周数。

运行结果如下：

```
complete_turnover count: 10
incomplete_turnover count: 2
incomplete_turnover infos:
 [[45.0, 49.5, 49.5, 54.0], [49.5, 54.0, 54.0, 58.5]]

labour_week: 51.0 
circulate_week: 46.5
```

此前的数据处理代码生成了一份表格文件，里面存放了相关的原始周转数据。这份代码又读取了这个表格文件，进一步处理。

---

另外，我当时又想到一个问题，如果是截取中间的某段时间，该如何计算。

我本来是设想也处理左边的特殊情况。可用编程上的分治法。在头脑中预演了一下，虽然十分麻烦，但可以做出来。

后来我想到，这个问题还可用一个更简便的算法。就是根据两个时间节点，算出二者相对于起点的相应数据，再对两个时间节点所形成的对应数据做减法，马上结果就出来了。这个算法的实现比较简单，就是细节上要做一点工作。我暂时就不实现了。
