import numpy as np


capital_num = np.array([80000, 20000])
capital_time = np.array([10, 1 / 5])

result = capital_num / capital_time
print(np.sum(result))
