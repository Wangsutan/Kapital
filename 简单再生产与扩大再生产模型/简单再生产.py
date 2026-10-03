#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 18 23:18:32 2022

@author: abc
"""

department_1 = {"c": 4000.00, "v": 1000.00, "m": 1000.00}    # 第Ⅰ部类之数据
department_2 = {"c": 2000.00, "v": 500.00, "m": 500.00}    # 第Ⅱ部类之数据

print("Ⅰ:", department_1)
print("Ⅱ:", department_2)

# 测试简单再生产之恒等式
if department_1["v"] + department_1["m"] == department_2["c"]:
    print("Ⅰv + Ⅰm = Ⅱc\n")

# 计算两个部类的总产品价值
total_value = 0
for department in [department_1, department_2]:
    print("calculating:", department)
    for x in department.values():
        total_value += x
print("total value: %.2f" % total_value)

# 分别计算两个部类的总产品价值
for department in [department_1, department_2]:
    print("calculating:", department)
    total_dept = 0
    for x in department.values():
        total_dept += x
    print("total_dept: %.2f" % total_dept)

# 按不变资本、可变资本、剩余价值统计总产品价值，不分部类
cvm = list(department_1)
for item in cvm:
    total_item = department_1[item] + department_2[item]
    print("total %s: %.2f" % (item, total_item))
