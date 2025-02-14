import numpy as np
from matplotlib import pyplot as plt


fig = plt.figure(figsize=(8, 6))
ax = plt.axes(projection='3d')

productNum = np.arange(50, 150, 1)
capitalAdvanced = np.arange(40, 100, 1)
ProductNum, CapitalAdvanced = np.meshgrid(productNum, capitalAdvanced)

price = 1

ProfitRate = (price * ProductNum) / CapitalAdvanced - 1

plt.title("ProfitRate = (price * ProductNum) / CapitalAdvanced - 1")
ax.plot_surface(ProductNum, CapitalAdvanced, ProfitRate, rstride=1, cstride=1, cmap='jet')

plt.show()
