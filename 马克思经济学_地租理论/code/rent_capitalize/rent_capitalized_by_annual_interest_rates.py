#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 20:36:56 2023

@author: wst
"""
# 年度利息率决定的资本化地租
import numpy as np
from matplotlib import pyplot as plt


def getCapitalImage(income_annual, interest_rate_annual):
    capital_image = income_annual / interest_rate_annual
    return capital_image


interest_rates_annual = np.linspace(0.0300, 0.0550, 100)

# rent_annual = float(input("Input annual rent: "))
rent_annual = 200

land_value = getCapitalImage(rent_annual, interest_rates_annual)

plt.plot(
    interest_rates_annual,
    land_value,
    label=f"rent annual: {rent_annual}"
)

plt.title("rents capitalized\nby various annual interest rates")
plt.xlabel("interest_rates_annual")
plt.ylabel("land_value")
plt.legend()
plt.show()
