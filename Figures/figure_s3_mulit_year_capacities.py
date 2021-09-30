# -*- coding: utf-8 -*-
"""
Created on Wed Feb 10 16:05:15 2021

@author: Kathleen
"""
##==============================================
# System capacities across years
##==============================================
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab

##=============================================
# Put data into dataframe
##=============================================
y2016 = [1.174227874,2.391016672,0.007130369,0.63907164,0.081870904,
         1.282669276,0.124075867,0.494094069]
y2017 = [0.936989885,2.856592398,0.059883746,1.376781838,0.11187187,
         0.780924888,0.11177265,0.422418846]
y2018 = [1.006056047,2.779067264,0.021333756,1.402456807,0.083249058,
         0.783214421,0.142140667,0.535222867]
y2019 = [1.169273823,2.580844637,0.024884151,3.205145101,0.211781128,
         0.72410727,0.093937186,0.325696993]
idx = ['PV','Wind','CSP Generation','TES','CSP Turbine','Battery',
       'Electrolyzer','Fuel Cell']

df = pd.DataFrame({'2016':y2016,'2017':y2017,'2018':y2018,'2019':y2019},
                  index=idx)

p2016 = [208.9329185]
p2017 = [197.524495]
p2018 = [213.8333223]
p2019 = [136.7811877]
ind = ['PGP Storage']

df2 = pd.DataFrame({'2016':p2016,'2017':p2017,'2018':p2018,'2019':p2019},
                   index = ind)

##==============================================
# Make plots
##==============================================
params = {'legend.fontsize': 'medium',
          'figure.figsize': (10, 6),
          'axes.labelsize': 'large',
          'axes.titlesize':'x-large',
          'xtick.labelsize':'medium',
          'ytick.labelsize':'large'}
pylab.rcParams.update(params)

fig = plt.figure()
ax = plt.subplot2grid((1, 5), (0, 0), colspan=4, rowspan=1)
df.plot.bar(ax=ax,colormap='jet',legend=False)
plt.xticks(rotation=45, ha='right')
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.set_ylabel('Capacity normalized to US Demand (kW$_e$)')

ax2 = plt.subplot2grid((1,5), (0,4), colspan=1, rowspan=1)
df2.plot.bar(ax=ax2,colormap='jet',legend=False)
plt.xticks(rotation=45, ha='right')
ax2.spines['right'].set_visible(False)
ax2.spines['top'].set_visible(False)

plt.legend(loc='upper center', bbox_to_anchor=(1.3, 0.98),frameon=False)
fig.text(0,.96, 'a)', size = 'large')
fig.text(0.73,.96, 'b)', size = 'large')

plt.tight_layout(True)
plt.savefig('PaperFigures/SI/figure_s2_multi_years.jpg', dpi=300, bbox_inches='tight')
plt.show()