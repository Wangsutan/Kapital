import matplotlib.pyplot as plt


turnover_times = list(range(1, 13))
annual_used_variable_capital = 5000
advance_capitals = [annual_used_variable_capital / tt for tt in turnover_times]

for i in range(len(turnover_times)):
    print(turnover_times[i], advance_capitals[i])

plt.title("same annual used variable capital")
plt.plot(turnover_times, advance_capitals, label="advance capital")
plt.xlabel("turnover times")
plt.legend()
plt.show()
plt.clf()

advance_capital = 500
annual_used_variable_capitals = [advance_capital * tt for tt in turnover_times]

for i in range(len(turnover_times)):
    print(turnover_times[i], annual_used_variable_capitals[i])

plt.title("same advance capital")
plt.plot(turnover_times, annual_used_variable_capitals, label="annual used variable capital")
plt.xlabel("turnover times")
plt.legend()
plt.show()
