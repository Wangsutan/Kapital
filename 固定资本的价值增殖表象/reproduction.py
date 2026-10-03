#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 27 10:44:57 2022

@author: wst
"""

import matplotlib.pyplot as plt


def get_capital_total(capital_constant, capital_variable, surplus_value):
    return capital_constant + capital_variable + surplus_value


def get_surplus_value(capital_variable, surplus_value_rate):
    return capital_variable * surplus_value_rate


def get_reinvest_capital(surplus_value, rate_reinvest_capital):
    return surplus_value * rate_reinvest_capital


surplus_value_rate = 0.50
surplus_value_rate_reinvest = 0.45  # decide if it is expand reproduction
rate_reinvest_variable = 0.45
rate_reinvest_constant = 1.00 - rate_reinvest_variable

print(
    "\nsurplus_value_rate:",
    surplus_value_rate,
    "\nsurplus_value_rate_reinvest:",
    surplus_value_rate_reinvest,
    "\nrate_reinvest_variable:",
    rate_reinvest_variable,
    "\nrate_reinvest_constant:",
    rate_reinvest_constant,
)

capital_constant = 30000
capital_variable = 20000
surplus_value = 0
production_period = 10
total_capitals = [get_capital_total(capital_constant, capital_variable, surplus_value)]

for period in range(1, production_period + 1):
    print("\nperiod:", period)
    # in the viewpoint of this new production but not reproduction, there is no surplus value now.
    surplus_value = 0
    capital_orig = get_capital_total(capital_constant, capital_variable, surplus_value)
    print("capital_orig:", capital_orig)

    surplus_value_gross = get_surplus_value(capital_variable, surplus_value_rate)
    print("surplus_value_gross:", surplus_value_gross)
    rate_profit = surplus_value_gross / capital_orig
    print("rate_profit:", rate_profit)

    print("\ncapital_constant:", capital_constant)
    surplus_value_gross_capital_constant_shared = surplus_value_gross * (
        capital_constant / capital_orig
    )
    print(
        "surplus_value_gross_capital_constant_shared:",
        surplus_value_gross_capital_constant_shared,
    )
    surplus_value_gross_rate_capital_constant_shared = (
        surplus_value_gross_capital_constant_shared / capital_constant
    )
    print(
        "surplus_value_gross_rate_capital_constant_shared:",
        surplus_value_gross_rate_capital_constant_shared,
    )

    income_capitalist = surplus_value_gross * (1.00 - surplus_value_rate_reinvest)
    surplus_value = surplus_value_gross - income_capitalist
    print("surplus_value:", surplus_value)

    capital_now = get_capital_total(capital_constant, capital_variable, surplus_value)
    print("capital_now:", capital_now)
    total_capitals.append(capital_now)

    reinvest_variable = get_reinvest_capital(surplus_value, rate_reinvest_variable)
    capital_variable = capital_variable + reinvest_variable
    reinvest_constant = get_reinvest_capital(surplus_value, rate_reinvest_constant)
    capital_constant = capital_constant + reinvest_constant

plt.plot(range(0, production_period + 1), total_capitals)
