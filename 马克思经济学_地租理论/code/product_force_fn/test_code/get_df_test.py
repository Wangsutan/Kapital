#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 26 20:57:18 2023

@author: wst
"""

import pandas as pd


list_test = [
    ["A", 3, 5],
    ["B", 4, 7],
    ["C", 5, 10],
    ["D", 2, 5]
]

df_test = pd.DataFrame(
    list_test,
    columns=["type", "area", "investment"]
)

print(df_test)
