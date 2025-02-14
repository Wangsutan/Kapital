import numpy as np
from matplotlib import pyplot as plt


fig = plt.figure(figsize=(8, 6))
ax = plt.axes(projection='3d')

price = np.arange(50, 150, 1)
capitalAdvanced = np.arange(0, 50, 0.5)
CapitalAdvanced, Price = np.meshgrid(capitalAdvanced, price)

profitRate = 0.20

ProductNum = (1 + profitRate) * CapitalAdvanced / Price
plt.title("(1 + profitRate) * CapitalAdvanced / Price")
ax.plot_surface(CapitalAdvanced, Price, ProductNum, rstride=1, cstride=1, cmap='jet')
ax.set_xlabel("CapitalAdvanced")
ax.set_ylabel("Price")
ax.set_zlabel("ProductNum")

plt.show()
