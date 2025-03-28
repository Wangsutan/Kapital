# 两个部类下的再生产

马克思在《资本论》第二卷第三篇，依据不变资本、可变资本、剩余价值之区分，特别是生产资料和消费资料之区分，提出了两个部类下的简单再生产和扩大再生产模型。

# 两个部类下的简单再生产

两个部类下的简单再生产模型的一个关键因素是一个恒等式：$Ⅰv + Ⅰm = Ⅱc.$

这个恒等式的意义是，在简单再生产条件下：

1. 第Ⅰ部类（生产资料部类）之不变资本部分，在该部类之内互相交换，得以实现；

2. 第Ⅰ部类（生产资料部类）之可变资本部分和剩余价值部分，需要从现有的生产资料形式，转换成消费资料形式，因而不能在该部类之内互相交换而得以实现，而是需要同第Ⅱ部类（消费资料部类）相交换。

3. 第Ⅱ部类（消费资料部类）之不变资本部分，需要从现有的消费资料形式，转换成生产资料形式，因而不能在该部类之内互相交换而得以实现，而是需要同第Ⅰ部类（消费资料部类）相交换。

4. 第Ⅱ部类（消费资料部类）之可变资本部分和剩余价值部分，在该部类之该部分之内互相交换，得以实现。

5. 因此，第Ⅰ部类（生产资料部类）之可变资本部分和剩余价值部分，需要同第Ⅱ部类（消费资料部类）之不变资本部分，互相交换，互相实现对方。

首先，我们用Python设计、实现马克思两个部类下的简单再生产的衡等式。

代码如下：

```
```

运行结果如下：

```
Ⅰv + Ⅰm = Ⅱc
Equilibrium of simple reproduction: True
```

我们给出两个部类的相应数据。这些数据以字典这种数据类型保存。c、v、m分别代表不变资本、可变资本、剩余价值。然后，我们验证**简单再生产下两部类间交换之恒等式**，$Ⅰv + Ⅰm = Ⅱc.$如果相等，就打印相应的恒等式。

# 两个部类下的扩大再生产

现在，在马克思两个部类下的简单再生产之程序模型的基础上，设计、实现马克思两个部类下的扩大再生产之程序模型。原素材可参阅《资本论》第二卷第二十一章第Ⅲ节第1小节。

为了增强可读性和实现模块化，我们设计实现了两个模块`basic_functions.py`和`basic_plots.py`，分别用来进行统计和绘图，然后把涉及核心运算的代码放在`increased_reproduction.py`中。

## 基本统计函数模块

我们可以对两大部类的诸数据，进行三种不同的统计：

1. 计算两个部类的总产品价值；

2. 分别计算两个部类的总产品价值；

3. 按不变资本、可变资本、剩余价值统计总产品价值，不分部类。

我们将这些统计方式制作成一个Python模块`basic_functions.py`，统计方式比较简单，请自行阅读相应代码来了解其具体的技术细节。在该模块中，还设计了一个展示两个部类数据的函数`print_departments`。

## 基本绘图函数模块

我们用三种方法来可视化`department_changes`里的数据，并且相关函数放到了Python模块`basic_plots.py`中。

第一种方法是，按每一年度，将两个部类的资本，包括不变资本和可变资本，统计在一起。这样，就可以逐年展示总资本之量。相关函数是`draw_total_capital`。可据此绘制图形如下，这是折线图：

![[Figure 2024-04-28 230741.png]]

第二种方法是，按每一年度，按不变资本和可变资本之区别，统计两个部类。就是说，每一年度中的资本要区分为不变资本和可变资本。我们可用堆叠柱状图来展示这些数据。相关函数是`draw_c_and_v`。图形如下：

![[Figure 2024-04-28 230748.png]]

在这个图形中，蓝色代表不变资本，橙色代表可变资本，每一个柱代表一个年度。

第三种方法是，按每一年度，按两个部类之区别，进行统计。就是说，每一年度中的资本要区分为第Ⅰ部类和第Ⅱ部类。我们可用堆叠柱状图来展示这些数据。相关函数是`draw_capital_in_department`。图形如下：

![[Figure 2024-04-28 230752.png]]

注意，横坐标上的数值有特殊的含义。比如，0指第0年末、第1年初，也就是通常意义上的最初状态。1指第1年末、第2年初。诸如此类。

## 关于核心运算的代码

代码如下：

```
```

我们从`basic_functions.py`模块导入`print_departments`函数，这个函数的作用是展示两个部类的数据。

我们从`basic_plots.py`模块导入三个绘图函数，这些函数的作用是用上文提到的三种方式绘制相关图形。

`produce`函数模拟生产过程，可以计算每个部类生产出来的剩余价值。计算剩余价值的相应公式是用可变资本乘以剩余价值率。

`accumulate`函数模拟涉及两个部类的积累过程。这个函数的参数包括第I部类和第II部类的相应数据，第I部类积累的剩余价值，第I部类中的剩余价值再投资到不变资本中的比例，以及第II部类可变资本与不变资本的比率。

先来了解第I部类的积累过程。在两个部类的积累中，第I部类的积累是先发的。第I部类的这种积累会影响第II部类的积累。

既然已知第I部类中积累的剩余价值的量，那么，就需要从该部类的剩余价值量中减去已经积累的剩余价值量。这个过程对应的语句是：

```
dept_1["m"] -= m_accumulated_of_dept_1
```

将第I部类积累的剩余价值，乘以第I部类中的剩余价值再投资到不变资本中的比例，可得第I部类中再投资到不变资本上的剩余价值的量，然后就可以将这个量增加到不变资本上。这个过程对应的语句是：

```
dept_1["c"] += m_accumulated_of_dept_1 * m_reinvest_rate_to_c_of_dept_1
```

用1减去第I部类中的剩余价值再投资到不变资本中的比例，可得第I部类中的剩余价值再投资到可变资本中的比例。将第I部类积累的剩余价值，乘以第I部类中的剩余价值再投资到可变资本中的比例，可得第I部类中再投资到可变资本上的剩余价值的量，然后就可以将这个量增加到可变资本上。这个过程对应的语句是：

```
dept_1["v"] += m_accumulated_of_dept_1 * (1.0 - m_reinvest_rate_to_c_of_dept_1)
```

至此，这一轮中的第I部类的积累过程宣告结束。

再来了解第II部类的积累过程。第II部类的积累受到第I部类的积累之影响，相比而言是后发的。

第I部类的可变资本和剩余价值，最初一方面体现为用于生产资料的商品，另一方面体现为工人和资本家手中的货币收入。但是，第I部类中的工人和资本家，不能将第I部类的生产资料，而需要将第II部类的消费资料，当作自己的消费资料。因此，第I部类的v和m需要同第II部类的c进行交换。在数量上，第I部类的v和m的总和，就构成了第II部类应该实现的积累了的c。第II部类这种积累了的c的量与原来的c的量的差额，就是第II部类的剩余价值应该积累到c上的量。这个过程对应的语句是：

```
m_accumulated_to_c_of_dept_2 = dept_1["v"] + dept_1["m"] - dept_2["c"]
```

第II部类的不变资本增加应该积累到其中的剩余价值量。这个过程对应的语句是：

```
dept_2["c"] += m_accumulated_to_c_of_dept_2
```

第II部类的不变资本和可变资本之间保持着一种比例，即变量`v_c_rate_of_dept_2`所代表的比例。第II部类的已经积累了的不变资本，通过变量`v_c_rate_of_dept_2`所代表的这种比例，决定了第II部类的可变资本应该达到的量。这种量减去第II部类的可变资本原有的量所得的差值，就决定了第II部类中的剩余价值应该再投资到可变资本中的量。这个过程对应的语句是：

```
m_accumulated_to_v_of_dept_2 = dept_2["c"] * v_c_rate_of_dept_2 - dept_2["v"]
```

第II部类的可变资本增加应该积累到其中的剩余价值量。这个过程对应的语句是：

```
dept_2["v"] += m_accumulated_to_v_of_dept_2
```

第II部类的剩余价值应该减去该部类中的剩余价值再投资到不变资本和可变资本中的量。这个过程对应的语句是：

```
dept_2["m"] -= (m_accumulated_to_c_of_dept_2 + m_accumulated_to_v_of_dept_2)
```

至此，这一轮中的第II部类的积累过程宣告结束。

知道了相应的生产函数和积累函数，我们再来系统地了解这个再生产模型的运行过程。

我们给出两个部类的数据。每个部类的数据采用字典的方式进行存储和管理。

现在，计算第Ⅰ部类积累不变资本和可变资本的比例，即`m_reinvest_rate_to_c_of_dept_1`。计算方法是，相应不变资本除以不变资本和可变资本之和。在函数`accumulate`中，根据已知的第Ⅰ部类积累不变资本的比例，可以计算出第Ⅰ部类积累可变资本的比例，计算方式就是：

```
1.0 - m_reinvest_rate_to_c_of_dept_1
```

不难理解，第Ⅰ部类中的剩余价值积累到不变资本和可变资本上的比例的和恒为100%。为了代码的简洁性，第Ⅰ部类积累可变资本的比例不是像第Ⅰ部类积累不变资本的比例那样体现为一个变量，而是直接放到函数`accumulate`中进行计算。

还要计算第Ⅱ部类可变资本与不变资本的比率`v_c_rate_of_dept_2`。函数`accumulate`使用这个比率来计算第II部类中的剩余价值应该再投资到可变资本中的量。

列表`department_changes`用来保存两个部类在不同阶段上的相应数据。目前，先将初始状态保存进去。

然后，我们设定要积累多少年，放入变量`year_reproduct`。如果这个变量的值是5，for循环就会执行5次，我们可以得到初始的两个部类的数据，以及此后5个年度的积累后的相应数据。

我们在每次循环中获取第I部类和第II部类的剩余价值率。比如，可以设置这两个剩余价值率都为1.00。

接下来调用生产函数`produce`，这个函数根据特定部类中的可变资本之数额和剩余价值率，来生产出剩余价值。

接下来就是最关键的积累过程。首先需要输入第I部类的剩余价值的积累率，比如0.5，意思是第I部类中的剩余价值的50%用于积累。然后根据这个积累率计算第I部类中用于积累的剩余价值的量。此后，就是根据相关参数运行积累函数。积累所得的两个部类的数据结果会代替这两个部类原有的数据。

积累完成后，我们通过剩余价值的消费过程，将两个部类的剩下的剩余价值归零。这个过程在经济学上的意思是，第II部类的资本家用这部分剩余价值对应的收入，来购买该部类所生产的相应价值的消费资料。也就是说，该模型假设第II部类的资本家不存在储蓄行为。

经过了一次循环之后，第I部类和第II部类的字典中存储的值已经被更新。在下一次循环中，这些已经被更新的值又作为生产和积累的前提而存在。我们把该次循环结束时两个部类中的数据，增添到列表`department_changes`中。这样，会形成一个三级的嵌套列表，最内部的列表分别是两个部类各自的数据形成的列表，然后是这样的一对列表形成一个嵌套列表，然后是这样的列表按照年度再并列起来。

在再生产过程结束之后，可以对嵌套列表`department_changes`中保存的各个阶段的数据进行可视化。

运行过程和结果如下（这里显示的是终端结果，不包含生成的图形）：

```
Year(s) of Reproduction: 5

Year 1:

Original Status:
I: {'c': 4000.0, 'v': 1000.0, 'm': 0.0}
II: {'c': 1500.0, 'v': 750.0, 'm': 0.0}

Production:
Surplus Value Rate of Dept1(1.00 for example): 1.0
Surplus Value Rate of Dept2(1.00 for example): 1.0
I: {'c': 4000.0, 'v': 1000.0, 'm': 1000.0}
II: {'c': 1500.0, 'v': 750.0, 'm': 750.0}

Accumulation:
Accumulate Rate of Surplus Value of Dept1(0.5 for example): 0.5
I: {'c': 4400.0, 'v': 1100.0, 'm': 500.0}
II: {'c': 1600.0, 'v': 800.0, 'm': 600.0}

Consumption of Surplus Value:
I: {'c': 4400.0, 'v': 1100.0, 'm': 0.0}
II: {'c': 1600.0, 'v': 800.0, 'm': 0.0}

Year 2:

Original Status:
I: {'c': 4400.0, 'v': 1100.0, 'm': 0.0}
II: {'c': 1600.0, 'v': 800.0, 'm': 0.0}

Production:
Surplus Value Rate of Dept1(1.00 for example): 1.0
Surplus Value Rate of Dept2(1.00 for example): 1.0
I: {'c': 4400.0, 'v': 1100.0, 'm': 1100.0}
II: {'c': 1600.0, 'v': 800.0, 'm': 800.0}

Accumulation:
Accumulate Rate of Surplus Value of Dept1(0.5 for example): 0.5
I: {'c': 4840.0, 'v': 1210.0, 'm': 550.0}
II: {'c': 1760.0, 'v': 880.0, 'm': 560.0}

Consumption of Surplus Value:
I: {'c': 4840.0, 'v': 1210.0, 'm': 0.0}
II: {'c': 1760.0, 'v': 880.0, 'm': 0.0}

Year 3:

Original Status:
I: {'c': 4840.0, 'v': 1210.0, 'm': 0.0}
II: {'c': 1760.0, 'v': 880.0, 'm': 0.0}

Production:
Surplus Value Rate of Dept1(1.00 for example): 1.0
Surplus Value Rate of Dept2(1.00 for example): 1.0
I: {'c': 4840.0, 'v': 1210.0, 'm': 1210.0}
II: {'c': 1760.0, 'v': 880.0, 'm': 880.0}

Accumulation:
Accumulate Rate of Surplus Value of Dept1(0.5 for example): 0.5
I: {'c': 5324.0, 'v': 1331.0, 'm': 605.0}
II: {'c': 1936.0, 'v': 968.0, 'm': 616.0}

Consumption of Surplus Value:
I: {'c': 5324.0, 'v': 1331.0, 'm': 0.0}
II: {'c': 1936.0, 'v': 968.0, 'm': 0.0}

Year 4:

Original Status:
I: {'c': 5324.0, 'v': 1331.0, 'm': 0.0}
II: {'c': 1936.0, 'v': 968.0, 'm': 0.0}

Production:
Surplus Value Rate of Dept1(1.00 for example): 1.0
Surplus Value Rate of Dept2(1.00 for example): 1.0
I: {'c': 5324.0, 'v': 1331.0, 'm': 1331.0}
II: {'c': 1936.0, 'v': 968.0, 'm': 968.0}

Accumulation:
Accumulate Rate of Surplus Value of Dept1(0.5 for example): 0.5
I: {'c': 5856.4, 'v': 1464.1, 'm': 665.5}
II: {'c': 2129.6, 'v': 1064.8, 'm': 677.6000000000001}

Consumption of Surplus Value:
I: {'c': 5856.4, 'v': 1464.1, 'm': 0.0}
II: {'c': 2129.6, 'v': 1064.8, 'm': 0.0}

Year 5:

Original Status:
I: {'c': 5856.4, 'v': 1464.1, 'm': 0.0}
II: {'c': 2129.6, 'v': 1064.8, 'm': 0.0}

Production:
Surplus Value Rate of Dept1(1.00 for example): 1.0
Surplus Value Rate of Dept2(1.00 for example): 1.0
I: {'c': 5856.4, 'v': 1464.1, 'm': 1464.1}
II: {'c': 2129.6, 'v': 1064.8, 'm': 1064.8}

Accumulation:
Accumulate Rate of Surplus Value of Dept1(0.5 for example): 0.5
I: {'c': 6442.04, 'v': 1610.5099999999998, 'm': 732.05}
II: {'c': 2342.5599999999995, 'v': 1171.2799999999997, 'm': 745.3600000000006}

Consumption of Surplus Value:
I: {'c': 6442.04, 'v': 1610.5099999999998, 'm': 0.0}
II: {'c': 2342.5599999999995, 'v': 1171.2799999999997, 'm': 0.0}

```

嵌套列表`department_changes`中的数据如下：

```
[[[4000.0, 1000.0, 0.0], [1500.0, 750.0, 0.0]],
 [[4400.0, 1100.0, 0.0], [1600.0, 800.0, 0.0]],
 [[4840.0, 1210.0, 0.0], [1760.0, 880.0, 0.0]],
 [[5324.0, 1331.0, 0.0], [1936.0, 968.0, 0.0]],
 [[5856.4, 1464.1, 0.0], [2129.6, 1064.8, 0.0]],
 [[6442.04, 1610.5099999999998, 0.0],
  [2342.5599999999995, 1171.2799999999997, 0.0]]]
```

生成的图形如下：

![[Figure 2024-04-30 095035.png]]

![[Figure 2024-04-30 095044.png]]

![[Figure 2024-04-30 095049.png]]

# 总结

借助马克思两个部类下的简单再生产程序模型，我们可以自动验证简单再生产所必需的恒等式是否满足。借助马克思两个部类下的扩大再生产程序模型，我们可以自动完成相应模型下的积累。不仅如此，我们还可将两个部类的数据变化进行可视化。
