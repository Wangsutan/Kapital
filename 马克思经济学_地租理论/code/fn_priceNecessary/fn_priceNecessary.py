import numpy as np
from matplotlib import pyplot as plt


fig = plt.figure(figsize=(8, 6))
ax = plt.axes(projection='3d')

capitalAdvanced = np.arange(0, 50, 0.2)
productNum = np.arange(0, 4, 0.2)
CapitalAdvanced, ProductNum = np.meshgrid(capitalAdvanced, productNum)

profitRate1 = 0.20
profitRate2 = 0.50
profitRate3 = 1.00

PriceNecessary1 = (1 + profitRate1) * CapitalAdvanced / ProductNum
PriceNecessary2 = (1 + profitRate2) * CapitalAdvanced / ProductNum
PriceNecessary3 = (1 + profitRate3) * CapitalAdvanced / ProductNum

plt.title("PriceNecessary = (1 + profitRate) * CapitalAdvanced / ProductNum\n( profitRate = %.2f%%, %.2f%% and %.2f%%)" % (profitRate1 * 100, profitRate2 * 100, profitRate3 * 100))
ax.plot_surface(CapitalAdvanced, ProductNum, PriceNecessary1, rstride=1, cstride=1, cmap='jet')
ax.plot_surface(CapitalAdvanced, ProductNum, PriceNecessary2, rstride=1, cstride=1, cmap='jet')
ax.plot_surface(CapitalAdvanced, ProductNum, PriceNecessary3, rstride=1, cstride=1, cmap='jet')
ax.set_xlabel("CapitalAdvanced")
ax.set_ylabel("ProductNum")
ax.set_zlabel("PriceNecessary")
# plt.savefig('1.png',dpi=300)
plt.show()
