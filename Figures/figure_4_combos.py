# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 13:12:00 2020

@author: Kathleen
"""
##===========================================
# Figure 4 - Tech Combos
##===========================================

from __future__ import division
import numpy as np
from os import listdir

import pickle
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
import matplotlib.gridspec as gridspec
import matplotlib.ticker as ticker

import datetime
from matplotlib.dates import drange
from matplotlib.ticker import FormatStrFormatter


##==========================================
# Tech colors
##==========================================

solar_q = 'orange'
wind_q = 'blue'
pgp_q = 'pink'
batt_q = 'purple'
csp_q = 'yellow'
tes_q = 'cyan'
lost_load_q = 'gray'

##==========================================
# System Cost Calculations
##==========================================

def get_cost_contributions(base):
    input_tech = base[0][1] # list of dictionaries
    results_case = base[1][0]
    results_tech = base[1][1]
    results_time = base[1][2]
    
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
        #print(np.sum(results_time['lost_load dispatch'])/8760 * 100)
    except:
        lost_load_t = 0
      

    calc_sys_cost = wind_t + solar_t + batt_t + csp_t + tes_t + pgp_t + lost_load_t

    return wind_t, solar_t , batt_t, csp_t, tes_t, pgp_t, lost_load_t

#====================================================================
# Read data from each pickle file
##===================================================================

sys_costs = []
wind_costs = []
solar_costs = []
pgp_costs = []
batt_costs = []
csp_costs = []
tes_costs = []
lost_load_costs = []
cases = listdir('C:/Users/Kathleen/Desktop/Temp/Combos/All_reliable')

for case in cases:
    pickle_in = open('C:/Users/Kathleen/Desktop/Temp/Combos/All_reliable/' + case, 'rb')
    base = pickle.load(pickle_in)
    results_case = base[1][0]
    sys_costs.append(results_case['system_cost'])
    wind_c, solar_c , batt_c, csp_c, tes_c, pgp_c, lost_load_c = get_cost_contributions(base)
    wind_costs.append(wind_c)
    solar_costs.append(solar_c)
    pgp_costs.append(pgp_c)
    batt_costs.append(batt_c)
    csp_costs.append(csp_c)
    tes_costs.append(tes_c)
    lost_load_costs.append(lost_load_c)


#Prep for plotting    
N = 6
ind = np.arange(N)    # the x locations for the groups
width = 0.7       # the width of the bars: can also be len(x) sequence

data1 = np.array(solar_costs) #pv
data2 = np.array(wind_costs) #wind
data3 = np.array(csp_costs) #csp
data4 = np.array(tes_costs) #tes
data5 = np.array(batt_costs) #batt
data6 = np.array(pgp_costs) #pgp
data7 = np.array(lost_load_costs) #lost load

##======================================================================================================
# Make bar graph
##======================================================================================================

params = {'legend.fontsize': 'medium',
         'axes.labelsize': 'large',
         'axes.titlesize':'x-large',
         'xtick.labelsize':'medium',
         'ytick.labelsize':'large'}
pylab.rcParams.update(params)

fig = plt.figure(figsize=(8,10))
ax1 = plt.subplot2grid((2, 2), (0, 0), colspan=1, rowspan=1)
p1 = ax1.bar(ind, data1, width, color=solar_q)
p2 = ax1.bar(ind, data2, width, bottom=data1, color=wind_q)
p3 = ax1.bar(ind, data3, width, bottom=data1+data2, color=csp_q)
p4 = ax1.bar(ind, data4, width, bottom=data1+data2+data3, color=tes_q)
p5 = ax1.bar(ind, data5, width, bottom=data1+data2+data3+data4, color=batt_q)
p6 = ax1.bar(ind, data6, width, bottom=data1+data2+data3+data4+data5, color=pgp_q)
p7 = ax1.bar(ind, data7, width, bottom=data1+data2+data3+data4+data5+data6, color = lost_load_q)

plt.ylabel('System cost ($/kWh) ')
plt.xticks(rotation=45, ha='right')

ax = plt.gca() 
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
#plt.grid(True, which = 'major', axis = 'y', c = 'lightgray')

ax.set_ylim(0, 0.32)
ax.yaxis.set_major_locator(ticker.MultipleLocator(0.05))
ax.yaxis.set_minor_locator(ticker.MultipleLocator(0.01))
ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
ax.set_title('CSP+PV+Wind', y=0.9)

plt.xticks(ind, ('Base Case - All','Battery + PGP','TES + PGP',
                 'TES + Battery','TES only','Battery Only'))

xlocs=[0,1,2,3,4,5]
for i, v in enumerate(sys_costs):
    plt.text(xlocs[i] - 0.35, v + 0.01, format(v, '.2f'))

#====================================================================
# Read data from each pickle file
##===================================================================

sys_costs = []
wind_costs = []
solar_costs = []
pgp_costs = []
batt_costs = []
csp_costs = []
tes_costs = []
lost_load_costs = []
cases = listdir('C:/Users/Kathleen/Desktop/Temp/Combos/All_LL')

for case in cases:
    pickle_in = open('C:/Users/Kathleen/Desktop/Temp/Combos/All_LL/' + case, 'rb')
    base = pickle.load(pickle_in)
    results_case = base[1][0]
    sys_costs.append(results_case['system_cost'])
    wind_c, solar_c , batt_c, csp_c, tes_c, pgp_c, lost_load_c = get_cost_contributions(base)
    wind_costs.append(wind_c)
    solar_costs.append(solar_c)
    pgp_costs.append(pgp_c)
    batt_costs.append(batt_c)
    csp_costs.append(csp_c)
    tes_costs.append(tes_c)
    lost_load_costs.append(lost_load_c)


#Prep for plotting    
N = 6
ind = np.arange(N)    # the x locations for the groups
width = 0.7       # the width of the bars: can also be len(x) sequence

data1 = np.array(solar_costs) #pv
data2 = np.array(wind_costs) #wind
data3 = np.array(csp_costs) #csp
data4 = np.array(tes_costs) #tes
data5 = np.array(batt_costs) #batt
data6 = np.array(pgp_costs) #pgp
data7 = np.array(lost_load_costs) #lost load

##=================================================================================
# Make bar graph
##=================================================================================

ax2 = plt.subplot2grid((2, 2), (0, 1), colspan=1, rowspan=1)

p1 = ax2.bar(ind, data1, width, color=solar_q)
p2 = ax2.bar(ind, data2, width, bottom=data1, color=wind_q)
p3 = ax2.bar(ind, data3, width, bottom=data1+data2, color=csp_q)
p4 = ax2.bar(ind, data4, width, bottom=data1+data2+data3, color=tes_q)
p5 = ax2.bar(ind, data5, width, bottom=data1+data2+data3+data4, color=batt_q)
p6 = ax2.bar(ind, data6, width, bottom=data1+data2+data3+data4+data5, color=pgp_q)
p7 = ax2.bar(ind, data7, width, bottom=data1+data2+data3+data4+data5+data6, color = lost_load_q)

plt.ylabel('System cost ($/kWh) ')
plt.xticks(rotation=45, ha='right')

ax2.spines['right'].set_visible(False)
ax2.spines['top'].set_visible(False)
ax2.spines['left'].set_visible(False)
#plt.grid(True, which = 'major', axis = 'y', c = 'lightgray')

ax2.set_ylim(0, 0.32)
ax2.yaxis.set_major_locator(ticker.MultipleLocator(0.05))
ax2.yaxis.set_minor_locator(ticker.MultipleLocator(0.01))
ax2.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
ax2.yaxis.set_visible(False)
ax2.set_title('CSP+PV+Wind\nwith Lost Load', y=0.84)

plt.xticks(ind, ('All','Battery + PGP','TES + PGP','TES + Battery','TES only','Battery Only'))

plt.legend((p1[0], p2[0], p3[0], p4[0], p5[0], p6[0], p7[0]) , 
           ('PV', 'Wind', 'CSP', 'TES' , 'Battery', 'PGP', 'Lost Load' ),
           loc='upper center', bbox_to_anchor=(1.08, 0.96),frameon=False)

xlocs=[0,1,2,3,4,5]
for i, v in enumerate(sys_costs):
    plt.text(xlocs[i] - 0.35, v + 0.01, format(v, '.2f'))
    
#====================================================================
# Read data from each pickle file
##===================================================================

sys_costs = []
wind_costs = []
solar_costs = []
pgp_costs = []
batt_costs = []
csp_costs = []
tes_costs = []
lost_load_costs = []
cases = listdir('C:/Users/Kathleen/Desktop/Temp/Combos/CSP_PV')

for case in cases:
    pickle_in = open('C:/Users/Kathleen/Desktop/Temp/Combos/CSP_PV/' + case, 'rb')
    base = pickle.load(pickle_in)
    results_case = base[1][0]
    sys_costs.append(results_case['system_cost'])
    wind_c, solar_c , batt_c, csp_c, tes_c, pgp_c, lost_load_c = get_cost_contributions(base)
    wind_costs.append(wind_c)
    solar_costs.append(solar_c)
    pgp_costs.append(pgp_c)
    batt_costs.append(batt_c)
    csp_costs.append(csp_c)
    tes_costs.append(tes_c)
    lost_load_costs.append(lost_load_c)


#Prep for plotting
N = 5
ind = np.arange(N)    # the x locations for the groups
width = 0.6       # the width of the bars: can also be len(x) sequence

data1 = np.array(solar_costs) #pv
data2 = np.array(wind_costs) #wind
data3 = np.array(csp_costs) #csp
data4 = np.array(tes_costs) #tes
data5 = np.array(batt_costs) #batt
data6 = np.array(pgp_costs) #pgp
data7 = np.array(lost_load_costs) #lost load

##=============================================================================
# Make bar graph
##=============================================================================

ax3 = plt.subplot2grid((2, 2), (1, 0), colspan=1, rowspan=1)

p1 = ax3.bar(ind, data1, width, color=solar_q)
p2 = ax3.bar(ind, data2, width, bottom=data1, color=wind_q)
p3 = ax3.bar(ind, data3, width, bottom=data1+data2, color=csp_q)
p4 = ax3.bar(ind, data4, width, bottom=data1+data2+data3, color=tes_q)
p5 = ax3.bar(ind, data5, width, bottom=data1+data2+data3+data4, color=batt_q)
p6 = ax3.bar(ind, data6, width, bottom=data1+data2+data3+data4+data5, color=pgp_q)
p7 = ax3.bar(ind, data7, width, bottom=data1+data2+data3+data4+data5+data6, color = lost_load_q)

plt.ylabel('System cost ($/kWh) ')
plt.xticks(rotation=45, ha='right')

ax = plt.gca() 
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
#plt.grid(True, which = 'major', axis = 'y', c = 'lightgray')

ax.set_ylim(0, 0.32)
ax.yaxis.set_major_locator(ticker.MultipleLocator(0.05))
ax.yaxis.set_minor_locator(ticker.MultipleLocator(0.01))
ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
ax.set_title('CSP+PV', y=0.94)

plt.xticks(ind, ('All','TES + PGP', 'TES + Battery', 'TES only','Battery Only'))

xlocs=[0,1,2,3,4]
for i, v in enumerate(sys_costs):
    plt.text(xlocs[i] - 0.3, v + 0.01, format(v, '.2f'))
    
#====================================================================
# Read data from each pickle file
##===================================================================

sys_costs = []
wind_costs = []
solar_costs = []
pgp_costs = []
batt_costs = []
csp_costs = []
tes_costs = []
lost_load_costs = []
cases = listdir('C:/Users/Kathleen/Desktop/Temp/Combos/PV')

for case in cases:
    pickle_in = open('C:/Users/Kathleen/Desktop/Temp/Combos/PV/' + case, 'rb')
    base = pickle.load(pickle_in)
    results_case = base[1][0]
    sys_costs.append(results_case['system_cost'])
    wind_c, solar_c , batt_c, csp_c, tes_c, pgp_c, lost_load_c = get_cost_contributions(base)
    wind_costs.append(wind_c)
    solar_costs.append(solar_c)
    pgp_costs.append(pgp_c)
    batt_costs.append(batt_c)
    csp_costs.append(csp_c)
    tes_costs.append(tes_c)
    lost_load_costs.append(lost_load_c)


#Prep for plotting
N = 3
ind = np.arange(N)    # the x locations for the groups
width = 0.4       # the width of the bars: can also be len(x) sequence

data1 = np.array(solar_costs) #pv
data2 = np.array(wind_costs) #wind
data3 = np.array(csp_costs) #csp
data4 = np.array(tes_costs) #tes
data5 = np.array(batt_costs) #batt
data6 = np.array(pgp_costs) #pgp
data7 = np.array(lost_load_costs) #lost load

##======================================================================================================
# Make bar graph
##======================================================================================================

ax3 = plt.subplot2grid((2, 2), (1, 1), colspan=1, rowspan=1)

p1 = ax3.bar(ind, data1, width, color=solar_q)
p2 = ax3.bar(ind, data2, width, bottom=data1, color=wind_q)
p3 = ax3.bar(ind, data3, width, bottom=data1+data2, color=csp_q)
p4 = ax3.bar(ind, data4, width, bottom=data1+data2+data3, color=tes_q)
p5 = ax3.bar(ind, data5, width, bottom=data1+data2+data3+data4, color=batt_q)
p6 = ax3.bar(ind, data6, width, bottom=data1+data2+data3+data4+data5, color=pgp_q)
p7 = ax3.bar(ind, data7, width, bottom=data1+data2+data3+data4+data5+data6, color = lost_load_q)

plt.ylabel('System cost ($/kWh) ')
plt.xticks(rotation=45, ha='right')

ax = plt.gca() 
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['left'].set_visible(False)
#plt.grid(True, which = 'major', axis = 'y', c = 'lightgray')

ax.set_ylim(0, 0.32)
ax.yaxis.set_major_locator(ticker.MultipleLocator(0.05))
ax.yaxis.set_minor_locator(ticker.MultipleLocator(0.01))
ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
ax.yaxis.set_visible(False)
ax.set_title('PV', y=0.94)

plt.xticks(ind, ('Battery+PGP', 'PGP Only', 'Battery Only'))

xlocs=[0,1,2]
for i, v in enumerate(sys_costs):
    plt.text(xlocs[i] - 0.14, v + 0.01, format(v, '.2f'))

fig.text(0.02, 0.96, 'a)', size = 'x-large')
fig.text(0.5, 0.96, 'b)', size = 'x-large')
fig.text(0.02, 0.48, 'c)', size = 'x-large')
fig.text(0.5, 0.48, 'd)', size = 'x-large')


plt.tight_layout(True)
plt.savefig('PaperFigures/figure_4_combos.jpg', dpi = 300, bbox_inches='tight')
plt.show()
