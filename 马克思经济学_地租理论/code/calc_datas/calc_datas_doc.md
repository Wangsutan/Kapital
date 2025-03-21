# Python：根据特定级别土地的总投资和总产量，计算其他若干种数值

马克思在研究级差地租时，经常给出各种表格。这些表格看起来非常繁琐无聊，而且可读性差。

现在，我已经将若干数值的计算方法摸清，并据此设计出一份Python代码。

相关经济学关系如以下公式所示：

```

```

实际上，该份代码只需要知道社会平均利润率，以及各级土地的类型、总投资和总产量，就可以计算出很多种数值。十分方便。

代码如下：

```

```

原表格中的数据如下：

![截图_选择区域_20230824212447.jpg](/home/wst/Desktop/rant_theory/soils_instants/截图_选择区域_20230824212447.jpg)

Ipython终端里的命令如下：

```
%run calc.py 0.20 series_1.xlsx Ⅲ
```

运行所得的变量表如下：

![截图_选择区域_20230824211647.jpg](/home/wst/Desktop/rant_theory/soils_instants/截图_选择区域_20230824211647.jpg)

运行得到并导出的表格如下：

![截图_选择区域_20230824213046.jpg](/home/wst/Desktop/rant_theory/soils_instants/截图_选择区域_20230824213046.jpg)

经对比，所得的结果与马克思的相应计算结果是一致的。
