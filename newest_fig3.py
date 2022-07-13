import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import OrderedDict
import matplotlib.ticker as ticker
import matplotlib as mpl
mpl.rcParams['figure.dpi']= 600

# Check this is correct (not a leap year!)
n_time_steps = 8784

# Added in order of the panels
cases = OrderedDict()
cases['Natural Gas'] = 'New_Looping_Gas_Mike_EV.csv'
cases['Natural Gas + Solar + Wind'] = 'New_Looping_Gas_Sol_Wnd_Mike_EV.csv'
cases['Solar + Battery'] = 'New_Looping_Sol_Bat_Mike_EV.csv'
cases['Wind + Battery'] = 'New_Looping_Wnd_Bat_Mike_EV.csv'
cases['Solar + Wind + Battery'] = 'New_Looping_Sol_Wnd_Bat_Mike_EV.csv'

dfs = {}
for case, f in cases.items():
    df = pd.read_csv(f)
    df = df.sort_values(['ev1 mean demand', 'ev2 mean demand'])
    

    ### These might all already exist, this csv file is LARGE!
    df['ev1_div_main'] = df['ev1 mean demand'] / df['demand series']
    df['ev2_div_main'] = df['ev2 mean demand'] / df['demand series']
    df['total_load'] = df['ev1 mean demand'] + df['ev2 mean demand'] + df['demand series']
    df['lcoe'] = df['value'] / df['total_load'] / n_time_steps 
    # ev2_pct has lots of rounding issues, will make them integers to align values
    for val in ['ev1_div_main', 'ev2_div_main']:
        df[val] = df[val].round(1)
    
    dfs[case] = df


fig, axs = plt.subplots(ncols=len(cases), figsize=(13, 3.5))

i = 0
MAX = 0.
MIN = 999
Ms = OrderedDict()
for case in cases.keys():

    print(case)
    df = dfs[case]

    # matrix
    M = []

    for ev2 in df['ev2_div_main'].unique():

        baseline = np.max(df['lcoe'])

        # Get subset of csv file with this EV pct
        tmp = df[ df['ev2_div_main'] == ev2 ]
        print(ev2, "len:", len(tmp.index))
        ys = tmp['lcoe'] / baseline * 100
        M.append(ys)

        if np.max(ys) > MAX:
            MAX = np.max(ys)
        if np.min(ys) < MIN:
            MIN = np.min(ys)

        # Plot line version
        if ev2 in [0, .2, .4, .6, .8, 1]:
            axs[i].plot(tmp['ev1_div_main'], ys, lw=2, label = f"{ev2}") # v2
        else:
            axs[i].plot(tmp['ev1_div_main'], ys, lw=1, color='gray', label = f"{ev2}") # v2
    Ms[case] = M
    #axs[i].set_ylim(0, MAX*1.2)
    #axs[i].set_xlim(0, 1.)
    axs[i].xaxis.set_major_locator(ticker.MultipleLocator(.2))
    axs[i].yaxis.set_major_formatter(ticker.PercentFormatter())
    axs[i].set_title(case, fontsize=11, fontname='Calibri')
    if i == 0:
        #axs[i].set_ylabel('Difference in average\nelectricity cost ($/kWh)') # v2
        #axs[i].set_ylabel('Electricity cost\n(percent of system with zero EVs)') # v2
        axs[i].set_ylabel('LCOE / LCOE of system with zero EVs ($/kWh)')#100% V1G minus LCOE of the system\nwith incremental V2G ($/kWh)',fontsize=10, fontname='Calibri') # v2
        #axs[i].legend(ncol=2, title="Percent V2G", title_fontproperties={'weight':'bold'})
        #axs[i].legend(title="Percent V2G", title_fontproperties={'weight':'bold'})
        axs[i].legend(title=f"V2G load (kW) /\nMain load (kW)", ncol=2, fontsize=10)
        #axs[i].legend(title=r"$\bf{Percent}$ $\bf{V2G}$", fontsize=10)
    if i == 2:
        axs[i].set_xlabel('V1G load (kW) / Main load (kW)',fontsize=10, fontname='Calibri')
    i += 1
#plt.tight_layout()
plt.subplots_adjust(left=0.09, bottom=0.146, top=0.91, right=0.97, wspace=0.494, hspace=0.2)
plt.savefig('maybe_final_fig3_line_version.png')
#plt.savefig('new_total_cost_per_total_kwh_ALL.pdf')
#plt.show()
plt.close()
#

for k, v in Ms.items():
    print(k, len(v), len(v[0]))

fig, axs = plt.subplots(ncols=len(cases), sharey=True, figsize=(13, 3))
cmap = mpl.cm.get_cmap('plasma', 512)

i = 0
ims = []
css = []
for case in cases.keys():

    print(case)
    im = axs[i].imshow(Ms[case], interpolation='none', origin='lower', vmin=0, vmax=100, cmap=cmap)
    ims.append(im)
    if i == 0:
        axs[i].set_ylabel("V2G load (kW) / Main load (kW)")
    if i == 2:
        axs[i].set_xlabel('V1G load (kW) / Main load (kW)')
    x_ticks, x_labs = [], []
    for x in range(11):
        if x%2!=0: continue
        x_ticks.append(x)
        x_labs.append(round(x * 0.1,1))
    axs[i].set_xticks(x_ticks, x_labs)
    axs[i].set_yticks(x_ticks, x_labs) # Symmetric labels
    axs[i].yaxis.set_major_locator(ticker.FixedLocator([0, 2, 4, 6, 8, 10]))
    axs[i].xaxis.set_major_locator(ticker.FixedLocator([0, 2, 4, 6, 8, 10]))
    #axs[i].yaxis.set_major_formatter(ticker.PercentFormatter(xmax=10, decimals=0))
    axs[i].set_title(case, fontsize=11, fontname='Calibri')

    n_levels = np.arange(0,100,10)
    c_fmt = '%1.0f'
    cs = axs[i].contour(Ms[case], n_levels, colors='k')
    css.append(cs)
    # inline labels
    axs[i].clabel(cs, inline=1, fontsize=9, fmt=c_fmt)

    i += 1

plt.subplots_adjust(left=0.06, bottom=0.06, top=0.92, right=0.87)
cbar_ax = fig.add_axes([0.9, 0.18, 0.02, 0.92 - 0.3])
cbar = fig.colorbar(ims[-1], cax=cbar_ax)
cbar.ax.set_ylabel('LCOE / LCOE of system\nwith zero EVs ($/kWh)') # v2
dec = 0
cbar.ax.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=100, decimals=dec))
plt.savefig('maybe_final_fig3_heatmap.png')



print(f"Min value from all simulations: {MIN:.1f}")
