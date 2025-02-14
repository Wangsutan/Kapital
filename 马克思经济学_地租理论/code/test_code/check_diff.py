#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  8 23:27:25 2023

@author: wst
"""

def get_rent_per_area(soils):
    rentPerArea = 0
    areaSum = 0
    for item in soils:
        rentPerArea += item[0] * (item[1] - soils[0][1]) * item[2]
        areaSum += item[2]

    rentPerArea = rentPerArea / areaSum
    print(rentPerArea)
    return rentPerArea


# productPrice_i, productPerAcre_i, Acres_i
soilA = [3, 1, 1]
soilB = [3, 2, 3]
soilC = [3, 3, 5]
soilD = [3, 4, 7]

soils0 = [soilA, soilB, soilC, soilD]
rentPerAcreAvg0 = get_rent_per_area(soils0)


soilA_prime = [3, 1, 2]
soilB_prime = [3, 2, 6]
soilC_prime = [3, 3, 10]
soilD_prime = [3, 4, 14]

soils1 = [soilA_prime, soilB_prime, soilC_prime, soilD_prime]
rentPerAcreAvg1 = get_rent_per_area(soils1)

if rentPerAcreAvg0 == rentPerAcreAvg1:
    print("True")
