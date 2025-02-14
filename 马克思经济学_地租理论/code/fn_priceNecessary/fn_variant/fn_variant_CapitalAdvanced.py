import numpy as np
from matplotlib import pyplot as plt


fig = plt.figure(figsize=(8, 6))
ax = plt.axes(projection='3d')

price = np.arange(50, 150, 0.1)
profitRate = np.arange(0, 1.0, 0.1)
Price, ProfitRate = np.meshgrid(price, profitRate)

ProductNum = 1

CapitalAdvanced = (Price * ProductNum) / (1 + ProfitRate)

plt.title("CapitalAdvanced = (Price * ProductNum) / (1 + ProfitRate)")
ax.plot_surface(Price, ProfitRate, CapitalAdvanced, rstride=1, cstride=1, cmap='jet')

plt.show()
