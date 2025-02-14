import matplotlib.pyplot as plt
import matplotlib as mpl


def getSurplusLabourRate(work_time_sum, worker_num, necessary_labour_time):
    return (work_time_sum / (worker_num * necessary_labour_time)) - 1


work_time_sum = 900
necessary_labour_time = 6
worker_num_orig = 100

worker_num_list = list(range(worker_num_orig, int(worker_num_orig / 2), -1))
surplus_labour_rate_list = [
    getSurplusLabourRate(work_time_sum, worker_num, necessary_labour_time)
    for worker_num in worker_num_list
]

cmap = mpl.colors.ListedColormap(["DeepSkyBlue", "Coral", "Crimson", "#DCDCDC"])
norm = mpl.colors.BoundaryNorm([0.5, 0.8, 1.20, 1.5, 2.0], cmap.N)
colors = cmap(norm(surplus_labour_rate_list))

cmap.set_under("black")
cmap.set_over("grey")

plt.scatter(
    worker_num_list,
    surplus_labour_rate_list,
    c=colors,
    cmap=cmap,
    norm=norm,
)
plt.colorbar(mpl.cm.ScalarMappable(norm, cmap), extend="both")

plt.show()
