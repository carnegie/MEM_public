import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import OrderedDict
import matplotlib.ticker as ticker
import matplotlib as mpl
mpl.rcParams['figure.dpi']= 1200

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
#plt.subplots_adjust(left=0.09, bottom=0.146, top=0.91, right=0.97, wspace=0.494, hspace=0.2)
#plt.savefig('maybe_final_fig3_line_version.png')
#plt.savefig('new_total_cost_per_total_kwh_ALL.pdf')
#plt.show()
plt.close()
#


# Custom matplotlib contour percent formatter
# https://matplotlib.org/stable/gallery/images_contours_and_fields/contour_label_demo.html
# This custom formatter removes trailing zeros, e.g. "1.0" becomes "1", and
# then adds a percent sign.
def fmt(x):
    s = f"{x:.1f}"
    if s.endswith("0"):
        s = f"{x:.0f}"
    return rf"{s}\%" if plt.rcParams["text.usetex"] else f"{s}%"




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
    axs[i].set_xlim(0, 10)
    axs[i].set_ylim(0, 10)
    axs[i].yaxis.set_major_locator(ticker.FixedLocator([0, 2, 4, 6, 8, 10]))
    axs[i].xaxis.set_major_locator(ticker.FixedLocator([0, 2, 4, 6, 8, 10]))
    #axs[i].yaxis.set_major_formatter(ticker.PercentFormatter(xmax=10, decimals=0))
    axs[i].set_title(case, fontsize=11, fontname='Calibri')

    n_levels = np.arange(0,100,10)
    cs = axs[i].contour(Ms[case], n_levels, colors='k', linewidths=1)
    css.append(cs)
    # inline labels
    #axs[i].clabel(cs, inline=1, fontsize=9, fmt=fmt)
    axs[i].clabel(cs, inline=True, fontsize=9, fmt=fmt, inline_spacing=15)

    i += 1

plt.subplots_adjust(left=0.06, bottom=0.06, top=0.92, right=0.87)
cbar_ax = fig.add_axes([0.9, 0.18, 0.02, 0.92 - 0.3])
cbar = fig.colorbar(ims[-1], cax=cbar_ax)
cbar.ax.set_ylabel('LCOE / LCOE of system\nwith zero EVs (%)') # v2
dec = 0
cbar.ax.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=100, decimals=dec))
plt.savefig('maybe_final_fig3_heatmap3.png')
plt.savefig('maybe_final_fig3_heatmap3.pdf')



print(f"Min value from all simulations: {MIN:.1f}")



# Calc the partial derivatives
Ms_dy = OrderedDict()
Ms_dx = OrderedDict()
dfs = OrderedDict()
MAX = 0
for k, M in Ms.items():
    dic = {}
    # .1 is the spacing of the simulations
    for j, row in enumerate(M):
        dic[f"{j * .1:0.1f}"] = row.values
    df = pd.DataFrame(dic)
    #print(df)
    df1 = (df - df.shift(periods=-1))
    #print(df1)
    Ms_dy[k] = df1.values.T
    df2 = (df - df.shift(periods=-1, axis="columns"))
    Ms_dx[k] = df2.values.T
    max1 = np.nanmax(df1)
    max2 = np.nanmax(df2)
    max3 = max(max1, max2)
    if max3 > MAX:
        MAX = max3




fig, axs = plt.subplots(ncols=len(cases), nrows=2, sharey=True, figsize=(13, 5.4))
cmapBig = mpl.cm.get_cmap('plasma', 512)
bottom = 0.25
cmapShort = mpl.colors.ListedColormap(cmapBig(np.linspace(bottom, 1.0, int(512*(1 - bottom)))))

i = 0
ims = [[],[]]
css = [[],[]]
for case in cases.keys():

    print(case)
    #print(Ms_dx[case])
    im = axs[0][i].imshow(Ms_dy[case], interpolation='none', origin='lower', vmin=0, vmax=MAX, cmap=cmapShort)
    ims[0].append(im)
    if i == 0:
        axs[0][i].set_ylabel("V2G load (kW) / Main load (kW)")
    x_ticks, x_labs = [], []
    for x in range(11):
        if x%2!=0: continue
        x_ticks.append(x)
        x_labs.append(round(x * 0.1,1))
    axs[0][i].set_xticks(x_ticks, x_labs)
    axs[0][i].set_yticks(x_ticks, x_labs) # Symmetric labels
    axs[0][i].set_xlim(0, 10)
    axs[0][i].set_ylim(0, 10)
    axs[0][i].yaxis.set_major_locator(ticker.FixedLocator([0, 2, 4, 6, 8, 10]))
    axs[0][i].xaxis.set_major_locator(ticker.FixedLocator([0, 2, 4, 6, 8, 10]))
    #axs[0][i].yaxis.set_major_formatter(ticker.PercentFormatter(xmax=10, decimals=0))
    axs[0][i].set_title(case, fontsize=11, fontname='Calibri')

    #n_levels = np.arange(0,60,3)
    n_levels = [1,2,3,5,10,15,20,25,30,40]
    cs = axs[0][i].contour(Ms_dy[case], n_levels, colors='k', linewidths=1)
    css[0].append(cs)
    # inline labels
    #axs[0][i].clabel(cs, inline=1, fontsize=9, fmt=fmt)
    axs[0][i].clabel(cs, inline=True, fontsize=9, fmt=fmt, inline_spacing=15)

    im = axs[1][i].imshow(Ms_dx[case], interpolation='none', origin='lower', vmin=0, vmax=MAX, cmap=cmapShort)
    ims[1].append(im)
    if i == 0:
        axs[1][i].set_ylabel("V2G load (kW) / Main load (kW)")
    if i == 2:
        axs[1][i].set_xlabel('V1G load (kW) / Main load (kW)')
    x_ticks, x_labs = [], []
    for x in range(11):
        if x%2!=0: continue
        x_ticks.append(x)
        x_labs.append(round(x * 0.1,1))
    axs[1][i].set_xticks(x_ticks, x_labs)
    axs[1][i].set_yticks(x_ticks, x_labs) # Symmetric labels
    axs[1][i].set_xlim(0, 10)
    axs[1][i].set_ylim(0, 10)
    axs[1][i].yaxis.set_major_locator(ticker.FixedLocator([0, 2, 4, 6, 8, 10]))
    axs[1][i].xaxis.set_major_locator(ticker.FixedLocator([0, 2, 4, 6, 8, 10]))
    #axs[1][i].yaxis.set_major_formatter(ticker.PercentFormatter(xmax=10, decimals=0))

    #n_levels = np.arange(0,60,3)
    cs = axs[1][i].contour(Ms_dx[case], n_levels, colors='k', linewidths=1)
    css[1].append(cs)
    # inline labels
    #axs[1][i].clabel(cs, inline=1, fontsize=9, fmt=fmt)
    axs[1][i].clabel(cs, inline=True, fontsize=9, fmt=fmt, inline_spacing=15)

    i += 1

plt.subplots_adjust(left=0.06, bottom=0.06, top=0.92, right=0.87, hspace=0.04)
# CBar 1
cbar_ax1 = fig.add_axes([0.9, 0.54, 0.02, 0.34])
cbar1 = fig.colorbar(ims[0][-1], cax=cbar_ax1)
cbar1.ax.set_ylabel(r'$\partial LCOE$ / $\partial V1G$'+'\n(% LCOE of zero EV syst)') # v2
###cbar1.ax.set_ylabel(r'$\frac{\partial LCOE}{\partial V1G}$'+'\n(% LCOE zero EV syst)') # v2
dec = 0
cbar1.ax.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=100, decimals=dec))

# CBar 2
cbar_ax2 = fig.add_axes([0.9, 0.1, 0.02, 0.34])
cbar2 = fig.colorbar(ims[1][-1], cax=cbar_ax2)
###cbar2.ax.set_ylabel(r'$\frac{\partial LCOE}{\partial V2G}$'+'\n(% LCOE zero EV syst)') # v2
cbar2.ax.set_ylabel(r'$\partial LCOE$ / $\partial V2G$'+'\n(% LCOE of zero EV syst)') # v2
cbar2.ax.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=100, decimals=dec))
###plt.savefig('maybe_final_fig3_heatmap3x.png')
plt.savefig('maybe_final_fig3_heatmap3y.png')



print(f"Min value from all simulations: {MIN:.1f}")
