代码如下：

```python3
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 18 23:18:32 2022

@author: abc
"""

category_1 = {"c": 4000.00, "v": 1000.00, "m": 1000.00}
category_2 = {"c": 2000.00, "v": 500.00, "m": 500.00}

print("Ⅰ:", category_1)
print("Ⅱ:", category_2)

if category_1["v"] + category_1["m"] == category_2["c"]:
    print("Ⅰv + Ⅰm = Ⅱc\n")

total_value = 0
for category in [category_1, category_2]:
    print("calculating:", category)
    for x in category.values():
        total_value += x
print("total value: %.2f" % total_value)

for category in [category_1, category_2]:
    print("calculating:", category)
    total_ctg = 0
    for x in category.values():
        total_ctg += x
    print("total_ctg: %.2f" % total_ctg)

cvm = list(category_1)
for item in cvm:
    total_item = category_1[item] + category_2[item]
    print("total %s: %.2f" % (item, total_item))
```

运行结果如下：

```text
Ⅰ: {'c': 4000.0, 'v': 1000.0, 'm': 1000.0}
Ⅱ: {'c': 2000.0, 'v': 500.0, 'm': 500.0}
Ⅰv + Ⅰm = Ⅱc

calculating: {'c': 4000.0, 'v': 1000.0, 'm': 1000.0}
calculating: {'c': 2000.0, 'v': 500.0, 'm': 500.0}
total value: 9000.00
calculating: {'c': 4000.0, 'v': 1000.0, 'm': 1000.0}
total_ctg: 6000.00
calculating: {'c': 2000.0, 'v': 500.0, 'm': 500.0}
total_ctg: 3000.00
total c: 6000.00
total v: 1500.00
total m: 1500.00
```

代码如下：

```python3
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 18 23:18:32 2022

@author: abc
"""

category_1 = {"c": 4000.00, "v": 1000.00, "m": 1000.00}
category_2 = {"c": 2000.00, "v": 500.00, "m": 500.00}

print("Ⅰ:", category_1)
print("Ⅱ:", category_2)

if category_1["v"] + category_1["m"] == category_2["c"]:
    print("Ⅰv + Ⅰm = Ⅱc\n")

total_value = 0
for category in [category_1, category_2]:
    print("calculating:", category)
    for x in category.values():
        total_value += x
print("total value: %.2f" % total_value)

for category in [category_1, category_2]:
    print("calculating:", category)
    total_ctg = 0
    for x in category.values():
        total_ctg += x
    print("total_ctg: %.2f" % total_ctg)

cvm = list(category_1)
for item in cvm:
    total_item = category_1[item] + category_2[item]
    print("total %s: %.2f" % (item, total_item))
```

运行结果如下：

```text
Ⅰ: {'c': 4000.0, 'v': 1000.0, 'm': 1000.0}
Ⅱ: {'c': 2000.0, 'v': 500.0, 'm': 500.0}
Ⅰv + Ⅰm = Ⅱc

calculating: {'c': 4000.0, 'v': 1000.0, 'm': 1000.0}
calculating: {'c': 2000.0, 'v': 500.0, 'm': 500.0}
total value: 9000.00
calculating: {'c': 4000.0, 'v': 1000.0, 'm': 1000.0}
total_ctg: 6000.00
calculating: {'c': 2000.0, 'v': 500.0, 'm': 500.0}
total_ctg: 3000.00
total c: 6000.00
total v: 1500.00
total m: 1500.00
```

发布于 2022-10-24 21:20

编辑于 2022-10-24 21:25
