#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 26 15:38:59 2023

@author: wst
"""

import numpy as np
import matplotlib.pyplot as plt


def product_force_simple(investment):
    product_num = np.log(investment)
    return product_num


investments = np.arange(0, 1000, 20)
areas = np.arange(0, 100, 2)
Investments, Areas = np.meshgrid(investments, areas)

fig1 = plt.figure(figsize=(20, 10))

ax1 = fig1.add_subplot(121, projection="3d")
theme = "Product_num"
plt.title(theme)
ax1.set_xlabel("Investments")
ax1.set_ylabel("Areas")
ax1.set_zlabel(theme)

Product_num = product_force_simple(Investments / Areas)
ax1.plot_surface(Investments, Areas, Product_num,
                 rstride=1, cstride=1, cmap="jet")

ax2 = fig1.add_subplot(122, projection="3d")
theme = "Product_num_sum"
plt.title(theme)
ax2.set_xlabel("Investments")
ax2.set_ylabel("Areas")
ax2.set_zlabel(theme)

Product_num_sum = product_force_simple(Investments / Areas) * Areas
ax2.plot_surface(Investments, Areas, Product_num_sum,
                 rstride=1, cstride=1, cmap="jet")

contour_0 = np.full_like(Product_num_sum, 0)
ax2.plot_surface(Investments, Areas, contour_0, rstride=1,
                 cstride=1, linestyle='--', color='black', alpha=0.2)

contour_x = np.full_like(Product_num_sum, 100)
ax2.plot_surface(Investments, Areas, contour_x, rstride=1,
                 cstride=1, linestyle='--', color='green', alpha=0.2)

fig2 = plt.figure(figsize=(20, 10))

product_price = 100
ax3 = fig2.add_subplot(121, projection="3d")
theme = "gross_profit"
plt.title(theme)
ax3.set_xlabel("Investments")
ax3.set_ylabel("Areas")
ax3.set_zlabel(theme)

Gross_profit = product_force_simple(
    Investments / Areas) * Areas * product_price - Investments
ax3.plot_surface(Investments, Areas, Gross_profit,
                 rstride=1, cstride=1, cmap="jet")

profit_rate_avg = 0.2000
ax4 = fig2.add_subplot(122, projection="3d")
theme = "Super_profit"
plt.title(theme)
ax4.set_xlabel("Investments")
ax4.set_ylabel("Areas")
ax4.set_zlabel(theme)

Super_profit = product_force_simple(
    Investments / Areas) * Areas * product_price - Investments * (1.0 + profit_rate_avg)
ax4.plot_surface(Investments, Areas, Super_profit,
                 rstride=1, cstride=1, cmap="jet")

fig3 = plt.figure(figsize=(20, 10))

ax5 = fig3.add_subplot(121, projection="3d")
theme = "Gross_profit_rate"
plt.title(theme)
ax5.set_xlabel("Investments")
ax5.set_ylabel("Areas")
ax5.set_zlabel(theme)

Gross_profit_rate = Gross_profit / Investments
ax5.plot_surface(Investments, Areas, Gross_profit_rate,
                 rstride=1, cstride=1, cmap="jet")

ax6 = fig3.add_subplot(122, projection="3d")
theme = "Super_profit_rate"
plt.title(theme)
ax6.set_xlabel("Investments")
ax6.set_ylabel("Areas")
ax6.set_zlabel(theme)

Super_profit_rate = Super_profit / Investments
ax6.plot_surface(Investments, Areas, Super_profit_rate,
                 rstride=1, cstride=1, cmap="jet")

# plt.savefig('product_force_fn.png',dpi=300)
plt.show()
