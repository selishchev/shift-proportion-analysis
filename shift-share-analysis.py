import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

sfo_stat_t = pd.read_excel('C:\\Users\Polzovatel\Desktop\SFO_stat.xlsx')
sfo_stat_0 = pd.read_excel('C:\\Users\Polzovatel\Desktop\SFO_stat.xlsx', sheet_name=1)
main_sfo_stat_0 = sfo_stat_0.iloc[0:2]
main_sfo_stat_t = sfo_stat_t.iloc[0:2]
stats_rf_0 = []
stats_sfo_0 = []

for i in range(1, len(sfo_stat_t.columns)):
    stats_rf_0.append(main_sfo_stat_0.iat[0, i])

for i in range(1, len(sfo_stat_t.columns)):
    stats_sfo_0.append(main_sfo_stat_0.iat[1, i])

stats_rf_t = []
stats_sfo_t = []

for i in range(1, len(sfo_stat_t.columns)):
    stats_rf_t.append(main_sfo_stat_t.iat[0, i])

for i in range(1, len(sfo_stat_t.columns)):
    stats_sfo_t.append(main_sfo_stat_t.iat[1, i])

growth_sfo = []
for i, j in zip(stats_sfo_0, stats_sfo_t):
    growth_sfo.append(j/i)
growth_sfo = list(np.around(growth_sfo, decimals=3))

growth_rf = []
for i, j in zip(stats_rf_0, stats_rf_t):
    growth_rf.append(j/i)
growth_rf = list(np.around(growth_rf, decimals=3))

forecast_nat_industries = []
for i, j in zip(growth_rf, stats_sfo_0):
    forecast_nat_industries.append(i*j)
forecast_nat_industries = list(np.around(forecast_nat_industries, decimals=3))

differential_shift = []
for i, j in zip(stats_sfo_t, forecast_nat_industries):
    differential_shift.append(i-j)
differential_shift = list(np.around(differential_shift, decimals=3))

forecast_nat_economy = []
for i in stats_sfo_0:
    forecast_nat_economy.append(sum(stats_rf_t)/sum(stats_rf_0)*i)
forecast_nat_economy = list(np.around(forecast_nat_economy, decimals=3))

proportional_shift = []
for i, j in zip(forecast_nat_industries, forecast_nat_economy):
    proportional_shift.append(i-j)
proportional_shift = list(np.around(proportional_shift, decimals=3))

sum_differential_shift = sum(differential_shift)
sum_proportional_shift = sum(proportional_shift)
real_shift = float(np.around(sum_differential_shift + sum_proportional_shift, decimals=3))
relative_real_shift = float(np.around(real_shift / sum(stats_sfo_0), decimals=4))
relative_differential_shift = float(np.around(sum_differential_shift / sum(stats_sfo_0), decimals=4))
relative_proportional_shift = float(np.around(sum_proportional_shift / sum(stats_sfo_0), decimals=4))

Y_sfo = float(np.around((sum(stats_sfo_t) / sum(stats_sfo_0) - 1) * 100, decimals=2))
Y_rf = float(np.around((sum(stats_rf_t) / sum(stats_rf_0) - 1) * 100, decimals=2))
S_a = float(np.around(relative_real_shift * 100, decimals=2))

rate_of_increase_sfo = []
rate_of_increase_rf = []
for i in growth_sfo:
    rate_of_increase_sfo.append(float(np.around((i-1)*100, decimals=2)))
for i in growth_rf:
    rate_of_increase_rf.append(float(np.around((i-1)*100, decimals=2)))

industries = [str(x) for x in sfo_stat_t.columns]

x = np.linspace(-70, 70, 50)
y = np.linspace(-70, 70, 50)
x1 = [Y_rf for i in y]
y1 = [Y_sfo for i in x]
fig, ax = plt.subplots(figsize=(12, 8))
ax.set_title("Графический анализ структурных сдвигов", fontsize=16)
ax.set_xlabel("Темп роста национальной отрасли", fontsize=14)
ax.set_ylabel("Темп роста отрасли в регионе", fontsize=14)
ax.grid(which="major", linewidth=1.2)
ax.grid(which="minor", linestyle="--", color="gray", linewidth=0.5)
ax.plot(x, y)
ax.plot(x1, y, c='blue', label='Темп прироста нац. экономики')
ax.plot(x, y1, c='red', label="Темп прироста рег. экономики")
ax.plot(x, x1, 'b--', label='Темп прироста нац. экономики')
k = 1
while k != len(sfo_stat_t.columns):
    for i, j in zip(rate_of_increase_rf, rate_of_increase_sfo):
        ax.scatter(i, j, label=industries[k][:35])
        k += 1
ax.legend(fontsize='x-small')
plt.show()


def classification_of_Boudeville(rel_prop_shift, rel_diff_shift):
    if rel_prop_shift > 0:
        if rel_diff_shift > 0:
            if abs(rel_prop_shift) > abs(rel_diff_shift):
                return '1'
            else:
                return '2'
        else:
            if abs(rel_prop_shift) > abs(rel_diff_shift):
                return '4'
            else:
                return '5'
    else:
        if rel_diff_shift > 0:
            if abs(rel_prop_shift) > abs(rel_diff_shift):
                return '6'
            else:
                return '3'
        else:
            if abs(rel_prop_shift) > abs(rel_diff_shift):
                return '8'
            else:
                return '7'


print(classification_of_Boudeville(relative_proportional_shift, relative_differential_shift))
