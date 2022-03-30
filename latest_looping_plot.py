import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import OrderedDict
import matplotlib.ticker as ticker

# Check this is correct (not a leap year!)
n_time_steps = 8760

# Added in order of the panels
cases = OrderedDict()
cases['Natural Gas'] = 'Looping_Gas_tmp_Mike_EV.csv'
cases['Natural Gas + Solar + Wind'] = 'Looping_Gas_Sol_Wnd_tmp_Mike_EV.csv'
cases['Solar + Battery'] = 'Looping_Sol_Bat_tmp_Mike_EV_v2.csv'
cases['Wind + Battery'] = 'Looping_Wnd_Bat_tmp_Mike_EV.csv'
cases['Solar + Wind + Battery'] = 'Looping_Sol_Wnd_Bat_tmp_Mike_EV.csv'

dfs = {}
for case, f in cases.items():
    df = pd.read_csv(f)

    ### These might all already exist, this csv file is LARGE!
    df['ev_load'] = df['demand_ev2 series'] + df['demand_ev1 series']
    df['ev2_pct'] = df['demand_ev2 series'] / df['ev_load'] * 100
    # ev2_pct has lots of rounding issues, will make them integers to align values
    df['ev2_pct'] = df['ev2_pct'].round(0).astype('int32')
    df['total load'] = df['demand series'] + df['ev_load']
    
    # sort values
    df = df.sort_values(['total load', 'ev2_pct'])

    dfs[case] = df


fig, axs = plt.subplots(ncols=len(cases), figsize=(12, 4))

i = 0
for case in cases.keys():

    df = dfs[case]

    # Get version with 100% EV2
    ev2_100 = df[ df['ev2_pct'] == 100 ]
    
    print(len(ev2_100.index))
    
    MAX = 0.
    for ev2_pct in df['ev2_pct'].unique():
        #print(ev2_pct)
        if ev2_pct not in [0, 10, 30, 60, 100]: continue
        # Get subset of csv file with this EV pct
        tmp = df[ df['ev2_pct'] == ev2_pct ]
        print(ev2_pct, "len:", len(tmp.index))
        #print(tmp['ev_load'])
        ys = ((tmp['value'].values / tmp['total load'].values) - (ev2_100['value'].values / ev2_100['total load'].values)) / n_time_steps # v2
        axs[i].plot(tmp['ev_load'] / tmp['demand series'], ys, label = f"{ev2_pct}% EV2") # v2
        if np.max(ys) > MAX:
            MAX = np.max(ys)
        #axs[i].plot(tmp['ev_load'] / tmp['demand series'], tmp['value'].values / tmp['total load'].values / n_time_steps, label = f"{ev2_pct}% EV2") # v2
        #axs[i].plot(tmp['ev_load'] / tmp['demand series'], ((tmp['value'].values / tmp['total load'].values) - (ev2_100['value'].values / ev2_100['total load'].values)) / n_time_steps, label = f"{ev2_pct}% EV2") # v2
        #axs[i].plot(tmp['ev_load'] / tmp['demand series'], ((tmp['value'].values / tmp['total load'].values) / (ev2_100['value'].values / ev2_100['total load'].values)) - 1., label = f"{ev2_pct}% EV2") # v3
    #axs[i].set_ylabel('Scenario / 100% EV2 - 1 ($/kWh)') # v3
    axs[i].set_ylim(0, MAX*1.2)
    axs[i].set_xlim(0, 1.)
    axs[i].xaxis.set_major_locator(ticker.MultipleLocator(0.2))
    axs[i].set_title(case, fontweight="bold")
    if i == 0:
        axs[i].set_ylabel('Difference in average\nelectricity cost ($/kWh)') # v2
        axs[i].legend()
    if i == 2:
        axs[i].set_xlabel('Total EV load (kW) / Main load (kW)')
    i += 1
#plt.tight_layout()
plt.subplots_adjust(left=0.09, bottom=0.146, top=0.91, right=0.97, wspace=0.494, hspace=0.2)
plt.savefig('total_cost_per_total_kwh_ALL.png')
plt.show()
#
