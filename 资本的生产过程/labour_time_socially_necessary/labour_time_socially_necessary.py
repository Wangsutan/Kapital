import numpy as np


data_num = 100
labor_times = np.random.normal(50, 5, data_num)

labor_time_avg = np.mean(labor_times)
print(f"labor_time_avg:\n{labor_time_avg:.2f}\n")

labor_times_diff = labor_times - labor_time_avg

while True:
    try:
        idx = int(input(f"Input your index in range of (0, {data_num}): "))
        if 0 <= idx < data_num:
            break
        else:
            print("Index out of range. Please try again.")
    except ValueError:
        print("Invalid input. Please enter an integer.")

print(f"For example: {labor_times[idx]:.2f}")
if labor_times_diff[idx] > 0:
    print(f"They waste: {labor_times_diff[idx]:.2f}")
elif labor_times_diff[idx] < 0:
    print(f"They save: {-labor_times_diff[idx]:.2f}")
else:
    print("No waste and no save!")
