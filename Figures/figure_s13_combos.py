# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 15:01:45 2020

@author: Kathleen
"""
##=======================================
# Figure 1
##=======================================

from __future__ import division
import numpy as np
from os import listdir

import pickle
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.ticker as ticker

import datetime
from matplotlib.dates import drange
from matplotlib.ticker import FormatStrFormatter
import matplotlib.pylab as pylab


solar_q = 'orange'
wind_q = 'blue'
pgp_q = 'pink'
batt_q = 'purple'
csp_q = 'yellow'
tes_q = 'cyan'
lost_load_q = 'gray'


date1 = datetime.datetime(2017, 1, 1, 0)
date2 = datetime.datetime(2018, 1, 1, 0)
delta = datetime.timedelta(hours=1)
dates = drange(date1, date2, delta)
print(len(dates))

###=========================================
#System Cost Calculations
##=========================================
##===========================================
def get_cost_contributions(base):
    input_tech = base[0][1] # list of dictionaries
    results_case = base[1][0]
    results_tech = base[1][1]
    
    # Nameplate costs
    try:
        dicw = next((sub for sub in input_tech if sub['tech_name'] == 'wind'), None)
        wind_t = (np.multiply(dicw["fixed_cost"], results_tech["wind capacity"]))
    except:
        wind_t = 0
    
    try:
        dics = next((sub for sub in input_tech if sub['tech_name'] == 'PV'), None)
        solar_t = (np.multiply(dics["fixed_cost"], results_tech["PV capacity"]))
    except:
        solar_t = 0
    
    try:
        dicb = next((sub for sub in input_tech if sub['tech_name'] == 'battery'), None)
        batt_t = (np.multiply(dicb["fixed_cost"], results_tech["battery capacity"]))
    except:
        batt_t = 0
    
    try:
        dic1 = next((sub for sub in input_tech if sub['tech_name'] == 'CSP_generation'), None)
        dic2 = next((sub for sub in input_tech if sub['tech_name'] == 'CSP_turbine'), None)
        csp_t = ((np.multiply(dic1["fixed_cost"], results_tech["CSP_generation capacity"])) +
                 (np.multiply(dic2["fixed_cost"], results_tech["CSP_turbine capacity"])))
    except:
        csp_t = 0
    
    try:
        dicth = next((sub for sub in input_tech if sub['tech_name'] == 'CSP_TES'), None)
        tes_t = (np.multiply(dicth["fixed_cost"], results_tech["CSP_TES capacity"]))
    except:
        tes_t = 0
    
    try:
        dic4 = next((sub for sub in input_tech if sub['tech_name'] == 'to_PGP'), None)
        dic5 = next((sub for sub in input_tech if sub['tech_name'] == 'PGP_storage'), None)
        dic6 = next((sub for sub in input_tech if sub['tech_name'] == 'from_PGP'), None)
        pgp_t = ((np.multiply(dic4["fixed_cost"], results_tech["to_PGP capacity"])) +
                 (np.multiply(dic5["fixed_cost"], results_tech["PGP_storage capacity"])) +
                 (np.multiply(dic6["fixed_cost"], results_tech["from_PGP capacity"])))
    except:
        pgp_t = 0
        
    try:
        dicl = next((sub for sub in input_tech if sub['tech_name'] == 'lost_load'), None)
        lost_load_t = dicl["var_cost"] * np.sum(results_time['lost_load dispatch'])/8760
    except:
        lost_load_t = 0
   
    #print('System Cost Contributions =')
    #print(results_case['system_cost'])
    #print('My calcs =')
    #calc_sys_cost = wind_t + solar_t + batt_t + csp_t + tes_t + pgp_t
    #print(calc_sys_cost)
    return wind_t, solar_t , batt_t, csp_t, tes_t, pgp_t, lost_load_t

#====================================================================
# Get what you need from each pickle file for all tech combos
##===================================================================

sys_costs = []
wind_costs = []
solar_costs = []
pgp_costs = []
batt_costs = []
csp_costs = []
tes_costs = []
cases = listdir('C:/Users/Kathleen/Desktop/Temp/SimpleCombos')

for case in cases:
    pickle_in = open('C:/Users/Kathleen/Desktop/Temp/SimpleCombos/' + case, 'rb')
    base = pickle.load(pickle_in)
    input_case = base[0][0]
    input_tech = base[0][1]
    input_time = base[0][2]
    results_case = base[1][0]
    results_tech = base[1][1]
    results_time = base[1][2]
    sys_costs.append(results_case['system_cost'])
    wind_c, solar_c , batt_c, csp_c, tes_c, pgp_c, lost_load_c = get_cost_contributions(base)
    wind_costs.append(wind_c)
    solar_costs.append(solar_c)
    pgp_costs.append(pgp_c)
    batt_costs.append(batt_c)
    csp_costs.append(csp_c)
    tes_costs.append(tes_c)


#Prep for plotting, add blank spaces between each category
data = ( solar_costs, wind_costs, csp_costs, tes_costs, batt_costs, pgp_costs ) 
newdata = []

for i in data:
    insert1 = np.insert(i, 4, 0)
    newlist = np.insert(insert1, 8, 0)
    newlist = np.insert(newlist, 13, 0)
    newlist = np.insert(newlist, 17, 0)
    newlist = np.insert(newlist, 22, 0)
    newlist = np.insert(newlist, 26, 0)
    newdata.append(newlist)
    
N = 32
ind = np.arange(N)    # the x locations for the groups
width = 0.7       # the width of the bars: can also be len(x) sequence

dataset1 = np.array(newdata[0]) #solar
dataset2 = np.array(newdata[1]) #wind
dataset3 = np.array(newdata[2]) #csp
dataset4 = np.array(newdata[3]) #tes
dataset5 = np.array(newdata[4]) #batt
dataset6 = np.array(newdata[5]) #pgp

##======================================================================================================
# Bar graph - tech combos 
##======================================================================================================

params = {'legend.fontsize': 'medium',
          'figure.figsize': (13, 10),
          'axes.labelsize': 'large',
          'axes.titlesize':'x-large',
          'xtick.labelsize':'medium',
          'ytick.labelsize':'large'}
pylab.rcParams.update(params)

fig = plt.figure()
ax = plt.subplot2grid((4,6), (0, 0), colspan=6, rowspan=2)

p1 = plt.bar(ind, dataset1, width, color=solar_q)
p2 = plt.bar(ind, dataset2, width, bottom=dataset1, color=wind_q)
p3 = plt.bar(ind, dataset3, width, bottom=dataset1+dataset2, color=csp_q)
p4 = plt.bar(ind, dataset4, width, bottom=dataset1+dataset2+dataset3, color=tes_q)
p5 = plt.bar(ind, dataset5, width, bottom=dataset1+dataset2+dataset3+dataset4, color=batt_q)
p6 = plt.bar(ind, dataset6, width, bottom=dataset1+dataset2+dataset3+dataset4+dataset5, color=pgp_q)

plt.ylabel('System cost ($/kWh) ')
plt.xticks(rotation=45, ha='right')

ax = plt.gca() 
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
#plt.grid(True, which = 'major', axis = 'y', c = 'lightgray')

ax.set_ylim(0, 0.37)
ax.yaxis.set_major_locator(ticker.MultipleLocator(0.05))
ax.yaxis.set_minor_locator(ticker.MultipleLocator(0.01))
ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))

plt.xticks(ind, ('TES only', 'TES + Battery', 'TES + PGP', 'All', '',
                 'Battery only', 'PGP only', 'Battery + PGP', '',
                 'TES only','TES + Battery', 'TES + PGP', 'All', '',
                 'Battery only', 'PGP only', 'Battery + PGP', '',
                 'TES only','TES + Battery', 'TES + PGP', 'All', '',
                 'Battery only', 'PGP only', 'Battery + PGP', '',
                 'TES only', 'TES + Battery', 'TES + PGP','Battery + PGP',
                 'All'))


plt.legend((p1[0], p2[0], p3[0], p4[0], p5[0], p6[0]) , 
           ('PV', 'Wind', 'CSP', 'TES' , 'Battery', 'PGP' ),
           loc='upper center', bbox_to_anchor=(.99, 0.95),frameon=False)

xlocs=[0,1,2,3,5,6,7,9,10,11,12,14,15,16,18,19,20,21,23,24,25,27,28,29,30,31]
for i, v in enumerate(sys_costs):
    plt.text(xlocs[i] - 0.42, v + 0.01, format(v, '.2f'))

fig.text(.14, 0.98, 'CSP', size='large')
fig.text(.25, 0.98, 'PV', size = 'large')
fig.text(.36, 0.98, 'CSP+PV', size='large')
fig.text(.48, 0.98, 'Wind', size ='large')
fig.text(.58, 0.98, 'CSP+Wind', size='large')
fig.text(.70, 0.98, 'PV+Wind', size ='large')
fig.text(.81, 0.98, 'CSP+PV+Wind', size = 'large')

#====================================================================
# Read data from each pickle file for load lost combos
##===================================================================

sys_costs = []
wind_costs = []
solar_costs = []
pgp_costs = []
batt_costs = []
csp_costs = []
tes_costs = []
lost_load_costs = []
cases = listdir('C:/Users/Kathleen/Desktop/Temp/LLCombos')

for case in cases:
    pickle_in = open('C:/Users/Kathleen/Desktop/Temp/LLCombos/' + case, 'rb')
    base = pickle.load(pickle_in)
    input_case = base[0][0]
    input_tech = base[0][1]
    input_time = base[0][2]
    results_case = base[1][0]
    results_tech = base[1][1]
    results_time = base[1][2]
    sys_costs.append(results_case['system_cost'])
    wind_c, solar_c , batt_c, csp_c, tes_c, pgp_c, lost_load_c = get_cost_contributions(base)
    wind_costs.append(wind_c)
    solar_costs.append(solar_c)
    pgp_costs.append(pgp_c)
    batt_costs.append(batt_c)
    csp_costs.append(csp_c)
    tes_costs.append(tes_c)
    lost_load_costs.append(lost_load_c)


#Prep for plotting, add blank spaces between each category
data = ( solar_costs, wind_costs, csp_costs, tes_costs, batt_costs, 
        pgp_costs, lost_load_costs ) 
newdata = []

for i in data:
    insert1 = np.insert(i, 3, 0)
    newlist = np.insert(insert1, 7, 0)
    newlist = np.insert(newlist, 12, 0)
    newlist = np.insert(newlist, 17, 0)
    newlist = np.insert(newlist, 23, 0)
    newdata.append(newlist)
    
N = 29
ind = np.arange(N)    # the x locations for the groups
width = 0.7       # the width of the bars: can also be len(x) sequence

dataset1 = np.array(newdata[0]) #solar
dataset2 = np.array(newdata[1]) #wind
dataset3 = np.array(newdata[2]) #csp
dataset4 = np.array(newdata[3]) #tes
dataset5 = np.array(newdata[4]) #batt
dataset6 = np.array(newdata[5]) #pgp
dataset7 = np.array(newdata[6]) # load lost

##========================================================================
# Make bar graph for load lost combos
##========================================================================


ax2 = plt.subplot2grid((4, 6), (2, 0), colspan=6, rowspan=2)

p1 = plt.bar(ind, dataset1, width, color=solar_q)
p2 = plt.bar(ind, dataset2, width, bottom=dataset1, color=wind_q)
p3 = plt.bar(ind, dataset3, width, bottom=dataset1+dataset2, color=csp_q)
p4 = plt.bar(ind, dataset4, width, bottom=dataset1+dataset2+dataset3, color=tes_q)
p5 = plt.bar(ind, dataset5, width, bottom=dataset1+dataset2+dataset3+dataset4, color=batt_q)
p6 = plt.bar(ind, dataset6, width, bottom=dataset1+dataset2+dataset3+dataset4+dataset5, color=pgp_q)
p7 = plt.bar(ind, dataset7, width, bottom=dataset1+dataset2+dataset3+dataset4+dataset5+dataset6, color = lost_load_q)

plt.ylabel('System cost ($/kWh) ')
plt.xticks(rotation=45, ha='right')


ax2.spines['right'].set_visible(False)
ax2.spines['top'].set_visible(False)
#plt.grid(True, which = 'major', axis = 'y', c = 'lightgray')

ax2.set_ylim(0, 0.37)
ax2.yaxis.set_major_locator(ticker.MultipleLocator(0.05))
ax2.yaxis.set_minor_locator(ticker.MultipleLocator(0.01))
ax2.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))

plt.xticks(ind, ('Battery only','PGP only','Battery+PGP','',
                 'Battery only','PGP only','Battery+PGP','',
                 'TES only','TES + Battery','TES + PGP','All', '',
                 'TES only','TES + Battery','TES + PGP','All', '',
                 'TES only','TES + Battery','TES + PGP','Battery+PGP','All', '',
                 'TES only','TES + Battery','TES + PGP','Battery+PGP','All'))


plt.legend((p1[0], p2[0], p3[0], p4[0], p5[0], p6[0], p7[0]) , 
           ('PV', 'Wind', 'CSP', 'TES' , 'Battery', 'PGP', 'Lost Load' ),
           loc='upper center', bbox_to_anchor=(.99, 0.95), frameon=False)

xlocs=[0,1,2,4,5,6,8,9,10,11,13,14,15,16,18,19,20,21,22,24,25,26,27,28]
for i, v in enumerate(sys_costs):
    plt.text(xlocs[i] - 0.42, v + 0.01, format(v, '.2f'))


fig.text(.13, 0.46, 'PV', size = 'large')
fig.text(.22, 0.44, ' PV with\nLost Load', size = 'large')
fig.text(.36, 0.46, 'CSP+PV', size='large')
fig.text(.49, 0.44, 'CSP+PV with \n  Lost Load', size='large')
fig.text(.63, 0.46, 'CSP+PV+Wind', size = 'large')
fig.text(.795, 0.44, 'CSP+PV+Wind\nwith Lost Load', size = 'large')


fig.text(0.01,.93, 'a)', size = 'x-large')
fig.text(0.01,0.44, 'b)', size = 'x-large')

plt.tight_layout(True)
plt.savefig('PaperFigures/SI/figure_s12_combos.jpg', dpi=300, bbox_inches='tight')
plt.show()


