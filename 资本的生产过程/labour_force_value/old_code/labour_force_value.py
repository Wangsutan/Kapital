#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 22:10:55 2024

@author: abc

受到《资本论》第15章的启发和激励，开发了一套Python代码，
根据劳动者年度消费的情况，计算劳动力的价值。
运算结果非常巧合，正好是整的。
"""

import pandas as pd


def calculate_goods_value(good_item_list, good_quantity_list, good_price_list):
    goods_value_total = 0
    for i in range(len(good_item_list)):
        good_item_value = good_quantity_list[i] * good_price_list[i]
        goods_value_total += good_item_value

    return goods_value_total


df = pd.read_excel('goods.xlsx')
print(df)

good_item_list = list(df["good"])
good_quantity_list = list(df["quantity"])
good_price_list = list(df["price"])

goods_value_total = calculate_goods_value(
    good_item_list, good_quantity_list, good_price_list)

labour_force_value_annual = goods_value_total
print("labour_force_value_annual:", labour_force_value_annual)
print("labour_force_value_monthly:", labour_force_value_annual / 12)
