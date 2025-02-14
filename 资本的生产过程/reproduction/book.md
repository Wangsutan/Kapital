《资本论》第一卷这个环节上的再生产，是把积累作为再生产之中的一个内在过程来对待的，而积累的具体方式等问题就完全不在考虑范围之内。由于缺少了必要的中介和更具体的规定性，这个环节上的再生产当然只是一种空洞的、无概念的东西。这种再生产模型主要是用于初步地观察再生产，以此来熟悉一些最基础的规律。这样的观察当然是非常粗糙的。在《资本论》第二卷的资本的流通过程这一环节上，两大部类的区别呈现在再生产的视野中的时候，再生产才具有一种更加具体的内容。可是这种更具体的再生产不是这里的主题。

在这种空洞的再生产中，每一年度所得到的剩余价值，可以按一定比例重新投入到下一年度的再生产过程中。而且投入再生产的剩余价值还会按特定的比例分配在不变资本和可变资本上。

现在我们用程序的方式来考察这种无概念的再生产。代码如下：

```
```

我们在终端中输入最初投入的固定资本、可变资本的量，并且由此可得最初的预付资本量。

我们还准备了关于剩余价值和总资本量的两个列表，用来存放相关数据。再生产的时间需要先确定，比如3年或5年之类，之后就进入`for`循环。

通过这个`for`循环，可以计算在第1年的年末到第`year_reproduct`年的年末，固定资本、可变资本、剩余价值和总资本的量。主要过程如下。

通过索引确定当年是哪一年。人工确定当年的年剩余价值率。根据可变资本量和年剩余价值率计算剩余价值的量，并将剩余价值量和总资本量存储到相应列表中。显示该年年末时固定资本、可变资本、剩余价值和总资本等各项数据。

如果循环没有到达最后一年年末，就人工确定当年年末生产的剩余价值中有多少比率投入了再生产，以及作为可变资本投入再生产的剩余价值在所投入的总的剩余价值中的比率。通过`reinvest`函数，根据这两个值以及其他相关数据，来计算下一年度的年初时固定资本和可变资本的量。

然后，下一年度开始时，就以新的不变资本量和可变资本量作为基础进行再生产。到达最后一年年末后，就不需要再准备下一年的再生产所需的相关数据。

在以上所述的过程中，一般来说，如果变量`pct_of_surplus_value_in_reproduction`的值为0，就意味着不从上一年末的剩余价值中取出资金来投入新一年度的再生产，因此新一年度的再生产就是简单再生产。反之，只要这个变量不为0，新一年度的预付资本的量就总是比上一年度更大，因此就属于扩大再生产。

当若干年的再生产结束后，可以计算最终的总资本量与最初的预付资本量之间的差额，这个差额就在一定意义上表示生产的扩大。此外，还可以计算所有剩余价值的总和。

通过列表`capital_total_list`中的总资本的值，可以将总资本随着每年度生产而形成的变动进行可视化。

运行过程和结果如下：

```
constant capital： 80
variable capital： 20
years of reproduct: 3
surplus value rate annual: 1.00

After 1 year(s):
Constant Capital (c): 80.00
Variable Capital (v): 20.00
Surplus Value (m): 20.00
Capital Total: 120.00

percent of surplus value in reproduction: 0.5
percent of surplus value as variable_capital: 0.3
surplus value rate annual: 1.00

After 2 year(s):
Constant Capital (c): 87.00
Variable Capital (v): 23.00
Surplus Value (m): 23.00
Capital Total: 133.00

percent of surplus value in reproduction: 0.6
percent of surplus value as variable_capital: 0.3
surplus value rate annual: 1.00

After 3 year(s):
Constant Capital (c): 96.66
Variable Capital (v): 27.14
Surplus Value (m): 27.14
Capital Total: 150.94

Final capital - Advanced capital = 50.94
Total surplus value: 70.14
```

![[资本的生产过程/reproduction/Figure_1.png]]
