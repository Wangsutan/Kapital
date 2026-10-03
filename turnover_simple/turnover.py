#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 20:45:23 2022

@author: wst
"""

import numpy as np
import matplotlib.pyplot as plt


x_list = np.linspace(0, 24, num=121)
y_list = [12 / x for x in x_list]

plt.xlabel("turnover duration(months)")
plt.ylabel("turnover frequency(annual)")

plt.plot(x_list, y_list)
