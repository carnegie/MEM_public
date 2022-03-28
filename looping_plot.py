import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Check this is correct (not a leap year!)
n_time_steps = 8784


df = pd.read_csv('Looping_Gas_tmp_Mike_EV.csv')

### These might all already exist, this csv file is LARGE!
df['ev_load'] = df['demand_ev2 series'] + df['demand_ev1 series']
df['ev2_pct'] = df['demand_ev2 series'] / df['ev_load'] * 100
# ev2_pct has lots of rounding issues, will make them integers to align values
df['ev2_pct'] = df['ev2_pct'].round(0).astype('int32')
df['total load'] = df['demand series'] + df['ev_load']

# sort values
df = df.sort_values(['total load', 'ev2_pct'])
import matplotlib as mpl
mpl.rcParams['figure.dpi']= 1200

from matplotlib.ticker import FormatStrFormatter



fig_size = plt.rcParams["figure.figsize"] #set chart size (longer than taller)
fig_size[0] = 2
fig_size[1] = 3
plt.rcParams["figure.figsize"] = fig_size
plt.rcParams.update({'font.size': 7})
fig, ax = plt.subplots()

for ev2_pct in df['ev2_pct'].unique():
    print(ev2_pct)
    if ev2_pct not in [0, 10, 30, 60, 100]: continue
       # Get subset of csv file with this EV pct
    tmp = df[ df['ev2_pct'] == ev2_pct ]
    print(tmp['value'] / n_time_steps / tmp['total load'])
    #ax.plot(tmp['total load'], tmp['value'] / n_time_steps / tmp['total load'], label = f"{ev2_pct}% EV2")
    ax.plot(tmp['ev_load'] / tmp['demand series'], tmp['value'] / n_time_steps / tmp['total load'], label = f"{ev2_pct}% EV2")
ax.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
#create some data
#define grid of plots
# fig, axs = plt.subplots(nrows=1, ncols=5)

#add title
#add data to plots
#ax.set_ylim(ymin=0)
ax.set_ylim(0.032, 0.035)
ax.set_xlim(0, 1)
ax.yaxis.set_major_formatter(FormatStrFormatter('%.4f'))
ax.set_ylabel('System cost ($/kWh) / Total load (kW)', fontsize=10, fontname='Calibri')
#ax.set_xlabel('EV load (kW) / Main load (kW)')
ax.set_title('Natural Gas', fontweight="bold", fontsize=11, fontname='Calibri')

#ax.legend(fontsize=7)
plt.savefig('total_cost_per_total_kwh.png')
plt.show()
