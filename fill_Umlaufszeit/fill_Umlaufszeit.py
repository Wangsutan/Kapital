import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


Arbeitsperiode = 9
Umlaufszeit = 3
other_Produktionsperiode = 0
turnover_time = Arbeitsperiode + other_Produktionsperiode + Umlaufszeit
num_circle = 8
flüssiges_Kapital_per_week = 100

# normal methods(add floating captial) to fill the Umlaufszeit
time_pointer = 0
production_situations = []

for i in range(1, num_circle + 1):
    print(i)

    Arbeit_begin = time_pointer
    Arbeit_end = Arbeit_begin + Arbeitsperiode

    time_pointer = Arbeit_end

    Umlauf_begin = Arbeit_end
    Umlauf_end = Umlauf_begin + Umlaufszeit

    production_situation = [Arbeit_begin, Arbeit_end, Umlauf_begin, Umlauf_end]
    print(production_situation)
    production_situations.append(production_situation)

data_df = pd.DataFrame(production_situations)
data_df.columns = ["Arbeit_begin", "Arbeit_end", "Umlauf_begin", "Umlauf_end"]
data_df.to_excel("turnover_data.xlsx")

plt.figure(figsize=(10, 8))
color = ["b", "g", "r", "y", "c", "m", "k"]

for i in range(len(production_situations)):
    for j in range(len(production_situations[0]) - 1):
        plt.barh(
            i + 1,
            production_situations[i][j + 1] - production_situations[i][j],
            left=production_situations[i][j],
            color=color[j],
        )
plt.title("Marx's reproduction no stagnant made by Umlaufszeit")

labels = ["Arbeit", "Umlauf"]
colors_select = ["b", "r"]
patches = [
    mpatches.Patch(
        color=colors_select[i],
        label=labels[i]
    ) for i in range(len(labels))
]
plt.legend(handles=patches, loc=4)

plt.xlabel("week")
plt.ylabel("circle")
xticks_right_edge = int(production_situations[-1][-1] + turnover_time)
plt.xticks(range(0, xticks_right_edge + 1, 2))
plt.grid(axis="x", linestyle="--", alpha=0.2)
plt.show()
