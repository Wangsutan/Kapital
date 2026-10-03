#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 21:45:09 2022

@author: wst
"""
import numpy as np
import matplotlib.pyplot as plt


def get_C_current_0(C, T, t):
    """Version 0."""
    return C * (1 - t / T)


def get_C_current_1(C, T, t):
    """Version 1."""
    return C -get_c(C, T, t)


def get_c(C, T, t):
    return C / T * t


C = 100000
T = 5

t_list = np.arange(0, T, T / 100)
c_list = [get_c(C, T, t) for t in t_list]
C_current_list = [get_C_current_0(C, T, t) for t in t_list]

plt.plot(t_list, c_list, label="c")
plt.plot(t_list, C_current_list, label="C'")
plt.legend()
