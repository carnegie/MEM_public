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

Ms = {}
for case in cases.keys():
    Ms[case] = []
i = 0
MIN = 999
for case in cases.keys():

    print(case)
    df = dfs[case]

    # Get version with 100% EV2
    ev2_100 = df[ df['ev2_pct'] == 100 ]
    ev2_0 = df[ df['ev2_pct'] == 0 ]
    baseline = ev2_0.iloc[0]['value'] / ev2_0.iloc[0]['total load'] / n_time_steps
    print(ev2_0)
    print(baseline)
    
    print(len(ev2_100.index))
    
    MAX = 0.
    for ev2_pct in df['ev2_pct'].unique():
        #print(ev2_pct)
        #if ev2_pct not in [0, 10, 30, 60, 100]: continue
        if ev2_pct in [0,]: continue
        # Get subset of csv file with this EV pct
        tmp = df[ df['ev2_pct'] == ev2_pct ]
        print(ev2_pct, "len:", len(tmp.index))
        #print(tmp['ev_load'])
        #ys = ((tmp['value'].values / tmp['total load'].values)) / n_time_steps / baseline * 100 # v2
        ys = ((ev2_0['value'].values / ev2_0['total load'].values) - (tmp['value'].values / tmp['total load'].values)) / n_time_steps # v2
        Ms[case].append(ys)
        if np.min(ys) < MIN:
            MIN = np.min(ys)
        if ev2_pct in [0, 20, 40, 60, 80, 100]:
            axs[i].plot(tmp['ev_load'] / tmp['demand series'], ys, lw=2, label = f"{ev2_pct}%") # v2
        else:
            axs[i].plot(tmp['ev_load'] / tmp['demand series'], ys, lw=1, color='gray', label = f"{ev2_pct}%") # v2
        if np.max(ys) > MAX:
            MAX = np.max(ys)
    #axs[i].set_ylim(0, MAX*1.2)
    axs[i].set_xlim(0, 1.)
    axs[i].xaxis.set_major_locator(ticker.MultipleLocator(0.2))
    #axs[i].yaxis.set_major_formatter(ticker.PercentFormatter())
    axs[i].set_title(case, fontweight="bold")
    if i == 0:
        #axs[i].set_ylabel('Difference in average\nelectricity cost ($/kWh)') # v2
        #axs[i].set_ylabel('Electricity cost\n(percent of system with zero EVs)') # v2
        axs[i].set_ylabel('LCOE 100% V1G minus LCOE of the system\nwith incremental V2G ($/kWh)') # v2
        #axs[i].legend(ncol=2, title="Percent EV2", title_fontproperties={'weight':'bold'})
        axs[i].legend(title="Percent V2G", title_fontproperties={'weight':'bold'})
    if i == 2:
        axs[i].set_xlabel('Total EV load (kW) / Main load (kW)')
    i += 1
#plt.tight_layout()
plt.subplots_adjust(left=0.09, bottom=0.146, top=0.91, right=0.97, wspace=0.494, hspace=0.2)
plt.savefig('total_cost_per_total_kwh_ALL.png')
plt.savefig('total_cost_per_total_kwh_ALL.pdf')
plt.show()
plt.close()
#

#for k, v in Ms.items():
#    print(k, len(v))
#
#
#fig, axs = plt.subplots(ncols=len(cases), sharey=True, figsize=(16, 4))
#
#i = 0
#ims = []
#for case in cases.keys():
#
#    print(case)
#    im = axs[i].imshow(Ms[case], interpolation='none', origin='lower', vmin=MIN, vmax=100)
#    ims.append(im)
#    if i == 0:
#        axs[i].set_ylabel("EV2 as percent of total EVs")
#    if i == 2:
#        axs[i].set_xlabel('Total EV load (kW) / Main load (kW)')
#    x_ticks, x_labs = [], []
#    for x in range(11):
#        if x%2!=0: continue
#        x_ticks.append(x)
#        x_labs.append(round(x * 0.1,1))
#    axs[i].set_xticks(x_ticks, x_labs)
#    axs[i].yaxis.set_major_locator(ticker.FixedLocator([0, 2, 4, 6, 8, 10]))
#    axs[i].yaxis.set_major_formatter(ticker.PercentFormatter(xmax=10, decimals=0))
#    axs[i].set_title(case, fontweight="bold")
#    i += 1
#
#cbar_ax = fig.add_axes([0.92, 0.14, 0.02, 0.9 - 0.24])
#cbar = fig.colorbar(ims[-1], cax=cbar_ax)
#cbar.ax.set_ylabel('Electricity cost\n(percent of system with zero EVs)') # v2
#dec = 0
#cbar.ax.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=100, decimals=dec))
#plt.savefig('total_cost_per_total_kwh_ALL_heatmap.png')
#plt.savefig('total_cost_per_total_kwh_ALL_heatmap.pdf')
#plt.show()
