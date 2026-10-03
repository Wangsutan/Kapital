#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 18 19:19:29 2022

@author: wst
"""

import pandas as pd


def complete(complete_turnover):
    global labour_week, circulate_week
    turnover_times = len(complete_turnover)
    print("complete_turnover count:", turnover_times)
    labour_week += (ps[1] - ps[0]) * turnover_times
    circulate_week += (ps[3] - ps[2]) * turnover_times


def aligh(incomplete_turnover):
    global week_num, labour_week, circulate_week
    print("incomplete_turnover count:", len(incomplete_turnover))
    print("incomplete_turnover infos:\n", incomplete_turnover)
    for ps in incomplete_turnover:
        if week_num < ps[1]:
            labour_week += week_num - ps[0]
        if week_num > ps[2]:
            labour_week += ps[1] - ps[0]
            circulate_week += week_num - ps[2]


production_situations = pd.read_excel("turnover_data.xlsx", index_col=0).values.tolist()

week_num = 51

complete_turnover = []
incomplete_turnover = []
unnecessary_turnover = []

labour_week = 0
circulate_week = 0

for ps in production_situations:
    if week_num >= ps[3]:
        complete_turnover.append(ps)
    if ps[0] < week_num < ps[3]:
        incomplete_turnover.append(ps)
    if week_num <= ps[0]:
        unnecessary_turnover.append(ps)

complete(complete_turnover)
aligh(incomplete_turnover)

print("\nlabour_week:", labour_week, "\ncirculate_week:", circulate_week)
