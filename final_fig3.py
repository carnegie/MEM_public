import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import OrderedDict
import matplotlib.ticker as ticker
import matplotlib as mpl
import matplotlib.tri as tri
#mpl.rcParams['figure.dpi']= 1200

# Check this is correct (not a leap year!)
n_time_steps = 8784

# Added in order of the panels
cases = OrderedDict()
cases['Natural Gas'] = 'Ken_Looping_Gas_Mike_EV.csv'
cases['Natural Gas + Solar + Wind'] = 'Ken_Looping_Gas_Sol_Wnd_Mike_EV.csv'
cases['Solar + Battery'] = 'Ken_Looping_Sol_Bat_Mike_EV.csv'
cases['Wind + Battery'] = 'Ken_Looping_Wnd_Bat_Mike_EV.csv'
cases['Solar + Wind + Battery'] = 'Ken_Looping_Sol_Wnd_Bat_Mike_EV.csv'

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
        df[val] = df[val].round(3)
    
    dfs[case] = df



# Custom matplotlib contour percent formatter
# https://matplotlib.org/stable/gallery/images_contours_and_fields/contour_label_demo.html
# This custom formatter removes trailing zeros, e.g. "1.0" becomes "1", and
# then adds a percent sign.
def fmt(x):
    s = f"{x:.1f}"
    if s.endswith("0"):
        s = f"{x:.0f}"
    return rf"{s}\%" if plt.rcParams["text.usetex"] else f"{s}%"




fig, axs = plt.subplots(ncols=len(cases), sharey=True, figsize=(13, 3))
cmap = mpl.cm.get_cmap('plasma', 512)


i = 0
css = []
cntr2s = []
for case in cases.keys():

    df = dfs[case]

    x = df['ev1_div_main']
    y = df['ev2_div_main']
    z = df['lcoe']
    baseline = np.max(z)
    z = z/baseline*100
    
    # https://matplotlib.org/stable/gallery/images_contours_and_fields/irregulardatagrid.html
    # ----------
    # Tricontour
    # ----------
    levels = np.arange(0, 101, 5)
    axs[i].tricontour(x, y, z, levels=levels, linewidths=1, colors='k', vmin=0, vmax=100)
    cntr2 = axs[i].tricontourf(x, y, z, levels=levels, cmap="plasma")
    cntr2s.append(cntr2)
    axs[i].set(xlim=(0, 1), ylim=(0, 1))
    axs[i].yaxis.set_major_locator(ticker.MultipleLocator(.2))
    axs[i].xaxis.set_major_locator(ticker.MultipleLocator(.2))

    print(case)
    if i == 0:
        axs[i].set_ylabel("V2G load (kW) / Main load (kW)")
    if i == 2:
        axs[i].set_xlabel('V1G load (kW) / Main load (kW)')
    axs[i].set_title(case, fontsize=11, fontname='Calibri')

    i += 1

plt.subplots_adjust(left=0.045, bottom=0.15, top=0.9, right=0.9, wspace=.14)
cbar_ax = fig.add_axes([0.91, 0.15, 0.015, 0.90 - 0.15])
cbar = fig.colorbar(cntr2s[-1], cax=cbar_ax)
cbar.ax.set_ylabel('LCOE / LCOE of system\nwith zero EVs (%)') # v2
dec = 0
cbar.ax.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=100, decimals=dec))
cbar.ax.yaxis.set_major_locator(ticker.FixedLocator([0, 20, 40, 60, 80, 100]))
#plt.savefig('maybe_final_fig3_heatmap_new_EVs.png')
plt.savefig('maybe_final_fig3_heatmap_new_EVs.pdf')

### DERIVATIVES
# https://docs.scipy.org/doc/scipy/tutorial/interpolate.html#interpolation-scipy-interpolate

from scipy.interpolate import Rbf
from matplotlib import cm

plt.close()
fig, axs = plt.subplots(ncols=len(cases), nrows=2, sharex=True, sharey=True, figsize=(13, 6))

rng = np.random.default_rng()
edges = np.linspace(0, 1.01, 102)
centers = edges[:-1] + np.diff(edges[:2])[0] / 2.
XI, YI = np.meshgrid(centers, centers)
#lims = dict(cmap='RdBu_r', vmin=0, vmax=5)
lims = dict(cmap='plasma', vmin=0)
MAX = 0

cntr2s = []
for i, case in enumerate(cases.keys()):

    df = dfs[case]
    
    x = df['ev1_div_main']
    y = df['ev2_div_main']
    z = df['lcoe']
    baseline = np.max(z)
    z = z/baseline*100
    
    # use RBF
    rbf = Rbf(x, y, z)
    ZI = rbf(XI, YI)
    
    # plot the result
    #plt.subplot(1, 1, 1)
    X_edges, Y_edges = np.meshgrid(edges, edges)
    #pcm = axs[i][0].pcolormesh(X_edges, Y_edges, ZI, shading='flat', **lims)
    ZA = np.abs((np.roll(ZI, -1, axis=0) - ZI))
    ZB = np.abs((np.roll(ZI, -1, axis=1) - ZI))
    print(f"{case}: max A {np.max(ZA)} Max B {np.max(ZB)}")
    pcmV1G = axs[0][i].pcolormesh(X_edges, Y_edges, ZB, shading='flat', vmax=3, **lims)
    pcmV2G = axs[1][i].pcolormesh(X_edges, Y_edges, ZA, shading='flat', vmax=3, **lims)
    ##this_max = max( np.abs((np.roll(ZI, -1, axis=0) - ZI)),
    ##        np.abs((np.roll(ZI, -1, axis=1) - ZI)) )
    ##if this_max > MAX:
    ##    MAX = this_max
    #levels = np.arange(0, 10, .5)
    #axs[0][i].tricontour(X_edges.flatten(), Y_edges.flatten(), ZA.flatten(), levels=levels, linewidths=1, colors='k', vmin=0, vmax=4)
    #cntr2 = axs[0][i].tricontourf(x, y, ZA, levels=levels, cmap="plasma")
    #cntr2s.append(cntr2)
    #axs[1][i].tricontour(x, y, ZB, levels=levels, linewidths=1, colors='k', vmin=0, vmax=100)
    #cntr2 = axs[1][i].tricontourf(x, y, ZB, levels=levels, cmap="plasma")
    #cntr2s.append(cntr2)
    
    axs[0][i].set(xlim=(0, 1), ylim=(0, 1))
    axs[0][i].yaxis.set_major_locator(ticker.MultipleLocator(.2))
    axs[0][i].xaxis.set_major_locator(ticker.MultipleLocator(.2))
    axs[1][i].set(xlim=(0, 1), ylim=(0, 1))
    axs[1][i].yaxis.set_major_locator(ticker.MultipleLocator(.2))
    axs[1][i].xaxis.set_major_locator(ticker.MultipleLocator(.2))
    
    if i == 0:
        axs[0][i].set_ylabel("V2G load (kW) / Main load (kW)")
        axs[1][i].set_ylabel("V2G load (kW) / Main load (kW)")
    if i == 2:
        axs[1][i].set_xlabel('V1G load (kW) / Main load (kW)')
    axs[0][i].set_title(case, fontsize=11, fontname='Calibri')
    axs[0][i].set(xlim=(0, 1), ylim=(0, 1))
    axs[1][i].set(xlim=(0, 1), ylim=(0, 1))
    
    
    #print(ZI)
    #print('')
    #print(np.roll(ZI, -1, axis=0))
    #print('')
    #print(np.roll(ZI, -1, axis=0)- ZI)

plt.subplots_adjust(left=0.045, bottom=0.15, top=0.9, right=0.9, wspace=.14)
dec = 1
cbar_ax1 = fig.add_axes([0.91, 0.56, 0.015, 0.34])
cbar1 = fig.colorbar(pcmV1G, cax=cbar_ax1)
cbar1.ax.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=100, decimals=dec))
cbar1.ax.set_ylabel(r'$\partial$ LCOE / $\partial$ V1G'+'\n(% LCOE of system with zero EVs)') # v2
cbar1.ax.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=100, decimals=dec))
cbar1.ax.yaxis.set_major_locator(ticker.MultipleLocator(.5))

cbar_ax2 = fig.add_axes([0.91, 0.15, 0.015, 0.34])
cbar2 = fig.colorbar(pcmV2G, cax=cbar_ax2)
cbar2.ax.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=100, decimals=dec))
cbar2.ax.set_ylabel(r'$\partial$ LCOE / $\partial$ V2G'+'\n(% LCOE of system with zero EVs)') # v2
cbar2.ax.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=100, decimals=dec))
cbar2.ax.yaxis.set_major_locator(ticker.MultipleLocator(.5))
plt.savefig('diff.pdf')

