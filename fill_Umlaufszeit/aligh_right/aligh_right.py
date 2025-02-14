import pandas as pd


def complete(labour_week, circulate_week, complete_turnover):
    turnover_times = len(complete_turnover)
    print("Complete Turnover Count:", turnover_times)
    labour_week += (ps[1] - ps[0]) * turnover_times
    circulate_week += (ps[3] - ps[2]) * turnover_times

    return labour_week, circulate_week


def aligh(labour_week, circulate_week, week_num, incomplete_turnover):
    print("Incomplete Turnover Count:", len(incomplete_turnover))
    print("Incomplete Turnover Infos:\n", incomplete_turnover)
    for ps in incomplete_turnover:
        if week_num < ps[1]:
            labour_week += week_num - ps[0]
        if week_num > ps[2]:
            labour_week += ps[1] - ps[0]
            circulate_week += week_num - ps[2]

    return labour_week, circulate_week


production_situations = pd.read_excel("turnover_data.xlsx", index_col=0).values.tolist()

week_num = 51

complete_turnover = []
incomplete_turnover = []
unnecessary_turnover = []

labour_week = 0
circulate_week = 0

for ps in production_situations:
    if week_num >= ps[3]:
        complete_turnover.append(ps)
    if ps[0] < week_num < ps[3]:
        incomplete_turnover.append(ps)
    if week_num <= ps[0]:
        unnecessary_turnover.append(ps)

labour_week, circulate_week = complete(labour_week, circulate_week, complete_turnover)
labour_week, circulate_week = aligh(
    labour_week, circulate_week, week_num, incomplete_turnover
)

print(f"\nLabour Week: {labour_week}\nCirculate Week: {circulate_week}")
