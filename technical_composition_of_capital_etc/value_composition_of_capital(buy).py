#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  9 18:58:07 2022

@author: wst
"""

import matplotlib.pyplot as plt


def get_value(x, y):
    return x * p1 + y * p2


def get_max_value(m_before, m_max):
    if m_before > m_max:
        m_max = m_before
    return m_max

def get_value_rate(x, xp, y, yp):
    return (x * xp) / (y * yp)


# M = float(input("Money:"))
M = 865.63

p1 = 0.63
p2 = 11.73
print("salary of worker:", p1, "\nprice of machine:", p2)
x_max = int(M // p1)
y_max = int(M // p2)

result_x = []
result_y = []
max_points = []
m_max = 0
for y in range(0, y_max + 1):
    for x in range(0, x_max + 1):
        if get_value(x, y) > M:
            x_before = x - 1
            result_x.append(x_before)
            result_y.append(y)
            m_before = get_value(x_before, y)
            m_max = get_max_value(m_before, m_max)
            break
print("all money:", M)
print("used money:", m_max)
print("number of max points:", len(result_x))

plt.scatter(result_x, result_y)

value_composition_of_capital = 12
diff = float("inf")
nearest_point = []
for k in range(len(result_x)):
    if result_x[k] == 0:
        break
    value_rate = get_value_rate(result_x[k], p1, result_y[k], p2)
    diff_now = abs(value_rate - value_composition_of_capital)
    if diff_now <= diff:
        diff = diff_now
        nearest_point.clear()
        nearest_point.append([result_x[k], result_y[k]])
        nearest_value_rate = get_value_rate(result_x[k], p1, result_y[k], p2)
print("value composition of capital:", value_composition_of_capital)
print("nearest point for it(workers: machines):", nearest_point)
print("nearest value rate:", nearest_value_rate)


for i in range(len(nearest_point)):
    plt.scatter(nearest_point[i][0], nearest_point[i][1], s=80, c="red")
    plt.text(
        nearest_point[i][0],
        nearest_point[i][1],
        "nearest point:",
        verticalalignment="bottom",
    )
