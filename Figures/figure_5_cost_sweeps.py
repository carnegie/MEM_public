# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 15:36:21 2021

@author: Kathleen
"""
##=======================================
# Figure 5: Cost Sensitivity Plots
##=======================================

from __future__ import division
import numpy as np
import os
import shutil

import pickle
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.ticker as ticker
import matplotlib.pylab as pylab

import datetime
from matplotlib.dates import drange
from matplotlib.ticker import FormatStrFormatter
import matplotlib.pylab as pylab

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

##====================================================
# Gather all files from MEM output into a folder for plotting
##====================================================
'''
file_path = 'C:/Users/Kathleen/Documents/GradSchool/Research/EnergyModeling/MEM-master/Output_Data/SweepNew'
target = r'C:/Users/Kathleen/Desktop/Temp/PGPSweepNew'

for root, dirs, files in os.walk(file_path):
    for file in files:
        if file.endswith(".pickle"):
            shutil.copy(os.path.join(root,file),target)

'''
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
        print(np.sum(results_time['lost_load dispatch'])/8760 * 100)
    except:
        lost_load_t = 0
      
        
    calc_sys_cost = wind_t + solar_t + batt_t + csp_t + tes_t + pgp_t + lost_load_t

    return wind_t, solar_t , batt_t, csp_t, tes_t, pgp_t, lost_load_t


##============================================================
# Slice plot 1 - CSP
##============================================================
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
parameter = np.linspace(0,1.5,13)
cases = os.listdir('C:/Users/Kathleen/Desktop/Temp/SensitivityCSP')
cases.sort()

for case in cases:
    pickle_in = open('C:/Users/Kathleen/Desktop/Temp/SensitivityCSP/' + case, 'rb')
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


data = [ solar_costs, wind_costs, csp_costs, tes_costs, batt_costs, 
        pgp_costs, lost_load_costs ]
labels = ['PV','Wind','CSP','TES','Battery','PGP']
colors = [solar_q, wind_q, csp_q, tes_q, batt_q, pgp_q]

##==============================================
# Make plot
##==============================================
params = {'legend.fontsize': 'large',
          'figure.figsize': (15, 10),
         'axes.labelsize': 'large',
         'axes.titlesize':'large',
         'xtick.labelsize':'large',
         'ytick.labelsize':'large'}
pylab.rcParams.update(params)

fig = plt.figure()
ax1 = plt.subplot2grid((2,2), (0, 0), colspan=1, rowspan=1)
ax1.stackplot(parameter, data, colors = colors, labels = labels)

ax1.axvline(1.326, c='r',label='SPT')
ax1.set_xlim(0,1.5)
ax1.set_ylim(0,0.12)
ax1.spines['right'].set_visible(False)
ax1.spines['top'].set_visible(False)
#ax1.set_title('System Sensitivity to CSP Generation Costs')
ax1.set_ylabel('System Cost ($/kWh)')
ax1.set_xlabel('CSP Cost (multiple of base case\ncost per unit power capacity)')

##==========================================================
# Slice plot 2 - TES
##==========================================================
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
cases = os.listdir('C:/Users/Kathleen/Desktop/Temp/SensitivityTES')
cases.sort()

for case in cases:
    pickle_in = open('C:/Users/Kathleen/Desktop/Temp/SensitivityTES/' + case, 'rb')
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


data = [ solar_costs, wind_costs, csp_costs, tes_costs, batt_costs, 
        pgp_costs, lost_load_costs ]

##==============================================
# Make plot
##==============================================

ax2 = plt.subplot2grid((2,2), (0, 1), colspan=1, rowspan=1)
ax2.stackplot(parameter, data, colors = colors, labels = labels)
ax2.axvline(0.355,c='r',label='SPT')
ax2.set_xlim(0,1.5)
ax2.set_ylim(0,0.12)
ax2.spines['right'].set_visible(False)
ax2.spines['top'].set_visible(False)
#ax2.set_title('System Sensitivity to TES Costs')
#ax2.set_ylabel('System Cost ($/kWh)')
ax2.set_xlabel('TES Cost (multiple of base case\ncost per unit energy capacity)')

ax2.legend(loc='upper center', bbox_to_anchor=(1.12, 1.03),frameon=False)

##============================================================
# Slice plot 3 - PV
##============================================================
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
cases = os.listdir('C:/Users/Kathleen/Desktop/Temp/SensitivityPV')
cases.sort()

for case in cases:
    pickle_in = open('C:/Users/Kathleen/Desktop/Temp/SensitivityPV/' + case, 'rb')
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
    #parameter.append(input_tech[][])


data = [ solar_costs, wind_costs, csp_costs, tes_costs, batt_costs, 
        pgp_costs, lost_load_costs ]
labels = ['PV','Wind','CSP','TES','Battery','PGP']
colors = [solar_q, wind_q, csp_q, tes_q, batt_q, pgp_q]

##==============================================
# Make plot
##=============================================

ax3 = plt.subplot2grid((2,2), (1, 0), colspan=1, rowspan=1)
ax3.stackplot(parameter, data, colors = colors, labels = labels)
ax3.set_xlim(0,1.5)
ax3.set_ylim(0,0.12)
ax3.spines['right'].set_visible(False)
ax3.spines['top'].set_visible(False)
#ax3.set_title('System Sensitivity to PV Costs')
ax3.set_ylabel('System Cost ($/kWh)')
ax3.set_xlabel('PV Cost (multiple of base case\ncost per unit power capacity)')

##============================================================
# Slice plot 4 - Batteries
##============================================================
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
cases = os.listdir('C:/Users/Kathleen/Desktop/Temp/SensitivityBatt')
cases.sort()

for case in cases:
    pickle_in = open('C:/Users/Kathleen/Desktop/Temp/SensitivityBatt/' + case, 'rb')
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


data = [ solar_costs, wind_costs, csp_costs, tes_costs, batt_costs, 
        pgp_costs, lost_load_costs ]
labels = ['PV','Wind','CSP','TES','Battery','PGP']
colors = [solar_q, wind_q, csp_q, tes_q, batt_q, pgp_q]

##==============================================
# Make plot
##==============================================

ax4 = plt.subplot2grid((2,2), (1, 1), colspan=1, rowspan=1)
ax4.stackplot(parameter, data, colors = colors, labels = labels)

ax4.set_xlim(0,1.5)
ax4.set_ylim(0,0.12)
ax4.spines['right'].set_visible(False)
ax4.spines['top'].set_visible(False)
#ax4.set_title('System Sensitivity to Battery Costs')
#ax4.set_ylabel('System Cost ($/kWh)')
ax4.set_xlabel('Battery Cost (multiple of base case\ncost per unit energy capacity)')

fig.text(0.01,0.94,'a)', size = 'x-large')
fig.text(0.46,0.94,'b)', size = 'x-large')
fig.text(0.01,0.45,'c)', size = 'x-large')
fig.text(0.46,0.45,'d)', size = 'x-large')

plt.tight_layout(pad=1.7)
plt.savefig('PaperFigures/figure_5_cost_sweeps.jpg', dpi=300, bbox_inches='tight')
plt.show()

