# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 15:15:26 2021

@author: Kathleen
"""
##==============================================
# Flexibility in the System
##==============================================
from __future__ import division
import numpy as np
import os
import shutil
import re

import pickle
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.ticker as ticker
import matplotlib.pylab as pylab

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
natgas_q = 'saddlebrown'

##====================================================
# Gather all files from MEM output into a folder for plotting
##====================================================
'''
file_path = 'C:/Users/Kathleen/Documents/GradSchool/Research/EnergyModeling/MEM-master/Output_Data/LLSweepFinal'
target = r'C:/Users/Kathleen/Desktop/Temp/LLSweep'

for root, dirs, files in os.walk(file_path):
    for file in files:
        if file.endswith(".pickle"):
            shutil.copy(os.path.join(root,file),target)
'''

##==========================================
# System Cost Calculations
##==========================================

def get_cost_contributions(base):
    input_case = base[0][0]
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
        dicn = next((sub for sub in input_tech if sub['tech_name'] == 'natgas'), None)
        natgas_t = (np.multiply(dicn['fixed_cost'], results_tech['natgas capacity']) +
                    (dicn['var_cost'] * np.sum(results_time['natgas dispatch'])/8760) +
                    (dicn['var_co2'] * np.sum(results_time['natgas dispatch'])/8760 * input_case['co2_price']))
    except:
        natgas_t = 0
    
    try:
        dicnc = next((sub for sub in input_tech if sub['tech_name'] == 'natgas_ccs'), None)
        natgas_ccs_t = (np.multiply(dicnc['fixed_cost'], results_tech['natgas_ccs capacity']) +
                    dicnc['var_cost'] * np.sum(results_time['natgas_ccs dispatch'])/8760 + 
                    dicnc['var_co2'] * np.sum(results_time['natgas_ccs dispatch'])/8760 * input_case['co2_price'])
    except:
        natgas_ccs_t = 0
        
    try:
        dicl = next((sub for sub in input_tech if sub['tech_name'] == 'lost_load'), None)
        lost_load_t = dicl["var_cost"] * np.sum(results_time['lost_load dispatch'])/8760
        #print(np.sum(results_time['lost_load dispatch'])/8760 * 100)
    except:
        lost_load_t = 0
      
        
    calc_sys_cost = (wind_t + solar_t + batt_t + csp_t + tes_t + pgp_t 
                     + lost_load_t + natgas_t + natgas_ccs_t)

    return wind_t, solar_t , batt_t, csp_t, tes_t, pgp_t, lost_load_t, natgas_t, natgas_ccs_t

#====================================================================
# Read lost load data from each pickle file
##===================================================================

sys_costs = []
wind_costs = []
solar_costs = []
pgp_costs = []
batt_costs = []
csp_costs = []
tes_costs = []
lost_load_costs = []
natgas_costs = []
natgas_ccs_costs = []
ll_prices = []

cases = os.listdir('C:/Users/Kathleen/Desktop/Temp/LLSweep')

for case in cases:
    pickle_in = open('C:/Users/Kathleen/Desktop/Temp/LLSweep/' + case, 'rb')
    base = pickle.load(pickle_in)
    input_tech = base[0][1]
    results_case = base[1][0]
    sys_costs.append(results_case['system_cost'])
    wind_c, solar_c , batt_c, csp_c, tes_c, pgp_c, lost_load_c, natgas_c, natgas_ccs_c = get_cost_contributions(base)
    wind_costs.append(wind_c)
    solar_costs.append(solar_c)
    pgp_costs.append(pgp_c)
    batt_costs.append(batt_c)
    csp_costs.append(csp_c)
    tes_costs.append(tes_c)
    lost_load_costs.append(lost_load_c)
    natgas_costs.append(natgas_c)
    natgas_ccs_costs.append(natgas_ccs_c)
    dicl = next((sub for sub in input_tech if sub['tech_name'] == 'lost_load'), None)
    ll_prices.append(dicl['var_cost'])

data = np.array([ ll_prices, solar_costs, wind_costs, csp_costs, tes_costs, 
                 batt_costs, pgp_costs, lost_load_costs ])
sortedData = data[ :, data[0].argsort()]
sortedData = np.delete(sortedData,0,0)

labels = ['PV','Wind','CSP','TES','Battery', 'PGP', 'Lost Load']
colors = [solar_q, wind_q, csp_q, tes_q, batt_q, pgp_q, lost_load_q]

ll_prices.sort()
##==============================================
# Make plot
##==============================================
params = {'legend.fontsize': 'large',
          'figure.figsize': (11, 10), 
         'axes.labelsize': 'x-large',
         'axes.titlesize':'x-large',
         'xtick.labelsize':'large',
         'ytick.labelsize':'large'}
pylab.rcParams.update(params)

fig = plt.figure()
ax = plt.subplot2grid((2, 1), (0, 0), colspan=1, rowspan=1)
ax.stackplot(ll_prices, sortedData, colors = colors, labels = labels)
#ax.axvline(10,c='r',label='Base Case Cost\nof Lost Load')
plt.legend(loc='upper center', bbox_to_anchor=(1.09, 1.03),frameon=False)

ax.set_xlim(0,20)
ax.set_ylim(0,.11)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.set_ylabel('System Cost ($/kWh)')
ax.set_xlabel('Cost of Unmet Demand ($/kWh)')

#====================================================================
# Read percent renewable data from each pickle file
##===================================================================

sys_costs = []
wind_costs = []
solar_costs = []
pgp_costs = []
batt_costs = []
csp_costs = []
tes_costs = []
lost_load_costs = []
natgas_costs = []
natgas_ccs_costs = []
percents = []

cases = os.listdir('C:/Users/Kathleen/Desktop/Temp/CO2Const')

for case in cases:
    pickle_in = open('C:/Users/Kathleen/Desktop/Temp/CO2Const/' + case, 'rb')
    base = pickle.load(pickle_in)
    results_case = base[1][0]
    results_time = base[1][2]
    sys_costs.append(results_case['system_cost'])
    wind_c, solar_c , batt_c, csp_c, tes_c, pgp_c, lost_load_c, natgas_c, natgas_ccs_c = get_cost_contributions(base)
    wind_costs.append(wind_c)
    solar_costs.append(solar_c)
    pgp_costs.append(pgp_c)
    batt_costs.append(batt_c)
    csp_costs.append(csp_c)
    tes_costs.append(tes_c)
    lost_load_costs.append(lost_load_c)
    natgas_costs.append(natgas_c)
    natgas_ccs_costs.append(natgas_ccs_c)
    natgas_disp = np.sum(results_time['natgas dispatch'])
    dem = np.sum(results_time['demand potential'])
    percents.append(natgas_disp/dem*100)
    #print(case)
    #print(results_case['system_cost'])
    #print(100 - natgas_disp/dem*100)

data = np.array([ percents, solar_costs, wind_costs, csp_costs, tes_costs, 
                 batt_costs, pgp_costs, natgas_costs ])
sortedData = data[ :, data[0].argsort()]
sortedData = np.delete(sortedData,0,0)

labels = ['PV','Wind','CSP','TES','Battery', 'PGP', 'Natural Gas']
colors = [solar_q, wind_q, csp_q, tes_q, batt_q, pgp_q, natgas_q]

percents.sort()

##==============================================
# Make plot
##==============================================

ax2 = plt.subplot2grid((2, 1), (1, 0), colspan=1, rowspan=1)
tot = np.zeros(len(percents))
ax2.stackplot(percents, sortedData, colors = colors, labels = labels)
'''
for i in range(len(sortedData)-1):
    ax2.fill_between(percents, tot, tot+sortedData[i], color=colors[i], linewidth=0, label=labels[i])
    tot += sortedData[i]
ax2.scatter(percents,sortedData[-1])
'''
plt.legend(loc='upper center', bbox_to_anchor=(1.1, 1.03),frameon=False)

exp = lambda x: 0.9**(x)
log = lambda x: np.log(x)

# Set y scale to exponential
ax2.set_xscale('function', functions=(exp, log))
ax2.set_xlim(0,100)
ax2.set_ylim(0,.11)
ax2.set_xticks([0,1,5,10,20, 100])
ax2.spines['right'].set_visible(False)
ax2.spines['top'].set_visible(False)
ax2.set_ylabel('System Cost ($/kWh)')
ax2.set_xlabel('% Demand Met by Natural Gas')


fig.text(0.01, 0.95, 'a)', size = 'large')
fig.text(0.01, 0.48, 'b)', size = 'large')

plt.tight_layout(True)
plt.savefig('PaperFigures/figure_3_flexibility.jpg', dpi = 300, bbox_inches='tight')
plt.show()