import numpy as np
import matplotlib.pyplot as plt


def product_force_simple(investment):
    product_num = 10 * np.log(investment)
    product_num = np.where(product_num < 0, 0, product_num)

    return product_num


investments = np.linspace(0.0, 1000.0, 100)
areas = np.linspace(0.0, 100.0, 100)
Investments, Areas = np.meshgrid(investments, areas)

fig1 = plt.figure()

ax1 = fig1.add_subplot(projection="3d")
theme = "Product_num_sum"
plt.title(theme)
ax1.set_xlabel("Investments")
ax1.set_ylabel("Areas")
ax1.set_zlabel(theme)

Product_num_sum = product_force_simple(Investments / Areas) * Areas
ax1.plot_surface(Investments, Areas, Product_num_sum,
                rstride=1, cstride=1, cmap="jet")

iso_value = 1000.0
Iso_quant = np.full_like(Product_num_sum, iso_value)
Iso_quant_zero_diff = Product_num_sum - Iso_quant
Iso_quant_idx = np.argwhere(
    (Iso_quant_zero_diff > -5) & (Iso_quant_zero_diff < 5))

iso_x, iso_y = Iso_quant_idx[:, 0], Iso_quant_idx[:, 1]

ax1.plot(investments[iso_x], areas[iso_y], iso_value,
        linewidth=2, linestyle="--", color='b')

# draw iso_quant independently
fig2 = plt.figure()
ax2 = fig2.add_subplot()

ax2.plot(investments[iso_x], areas[iso_y], linestyle="-.")

plt.title("iso_quant")
ax2.set_xlabel("Investments")
ax2.set_ylabel("Areas")
plt.show()
