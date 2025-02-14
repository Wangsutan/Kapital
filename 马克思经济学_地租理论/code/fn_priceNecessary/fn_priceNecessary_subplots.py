import numpy as np
from matplotlib import pyplot as plt


fig = plt.figure(figsize=(20, 20))

ax1 = fig.add_subplot(221, projection="3d")
plt.title("PriceNecessary = (1 + profitRate) * CapitalAdvanced / ProductNum)")
ax1.set_xlabel("CapitalAdvanced")
ax1.set_ylabel("ProductNum")
ax1.set_zlabel("PriceNecessary")

profitRate = 0.20
capitalAdvanced = np.arange(50, 100, 1)
productNum = np.arange(1, 5, 0.2)
CapitalAdvanced, ProductNum = np.meshgrid(capitalAdvanced, productNum)
PriceNecessary = (1 + profitRate) * CapitalAdvanced / ProductNum

ax1.plot_surface(
    CapitalAdvanced, ProductNum, PriceNecessary, rstride=1, cstride=1, cmap="jet"
)

ax2 = fig.add_subplot(222, projection="3d")
plt.title("ProductNum = (1 + profitRate) * CapitalAdvanced / PriceNecessary")
ax2.set_xlabel("CapitalAdvanced")
ax2.set_ylabel("PriceNecessary")
ax2.set_zlabel("ProductNum")

profitRate = 0.20
capitalAdvanced = np.arange(50, 100, 1)
priceNecessary = np.arange(10, 120, 1)
CapitalAdvanced, PriceNecessary = np.meshgrid(capitalAdvanced, priceNecessary)
ProductNum = (1 + profitRate) * CapitalAdvanced / PriceNecessary

ax2.plot_surface(
    CapitalAdvanced, PriceNecessary, ProductNum, rstride=1, cstride=1, cmap="jet"
)

ax3 = fig.add_subplot(223, projection="3d")
plt.title("CapitalAdvanced = (Price * productNum) / (1 + ProfitRate)")
ax3.set_xlabel("Price")
ax3.set_ylabel("ProfitRate")
ax3.set_zlabel("CapitalAdvanced")

productNum = 2
price = np.arange(10, 120, 1)
profitRate = np.arange(0, 1.0, 0.1)
Price, ProfitRate = np.meshgrid(price, profitRate)
CapitalAdvanced = (Price * productNum) / (1 + ProfitRate)

ax3.plot_surface(Price, ProfitRate, CapitalAdvanced, rstride=1, cstride=1, cmap="jet")

ax4 = fig.add_subplot(224, projection="3d")
plt.title("ProfitRate = (price * ProductNum) / CapitalAdvanced - 1")
ax4.set_xlabel("ProductNum")
ax4.set_ylabel("CapitalAdvanced")
ax4.set_zlabel("ProfitRate")

price = 25
productNum = np.arange(1, 5, 0.2)
capitalAdvanced = np.arange(50, 100, 1)
ProductNum, CapitalAdvanced = np.meshgrid(productNum, capitalAdvanced)
ProfitRate = (price * ProductNum) / CapitalAdvanced - 1

ax4.plot_surface(
    ProductNum, CapitalAdvanced, ProfitRate, rstride=1, cstride=1, cmap="jet"
)

plt.show()
