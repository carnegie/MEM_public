# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 13:32:27 2021

@author: Kathleen
"""
##=========================================================
# Time of day and year when storage is charged/discharged
##=========================================================

import numpy as np
import pandas as pd
import pickle
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import datetime
import pylab

pgp_c = 'deeppink' 
batt_c = 'purple'
tes_c = 'cyan'

##===========================================
# Read in pickle file
##===========================================

with open('C:/Users/Kathleen/Desktop/Temp/SimpleCombos/ZCombo4_batt_pgp_20210302-144151.pickle', 'rb') as handle:
            [[input_case,  input_tech,  input_time],
             [results_case, results_tech,  results_time]] = pickle.load(handle)

##=================================================
# Match up the dates, convert kWht to kWhe for TES
# Check which storage technologies were included
##=================================================
dates = np.arange('2017-01-01 00', '2018-01-01 00', dtype = 'datetime64[h]')
dates = dates - np.timedelta64(6,'h') # convert from UTC to CST
time_series = pd.DataFrame(results_time,index = dates)
time_series['Hour'] = time_series.index.hour
time_series['Month'] = time_series.index.month
colors = []
techs = []

if 'CSP_TES dispatch' in time_series.columns:
    time_series['CSP_TES in dispatch'] = time_series['CSP_TES in dispatch'] * 0.3774
    time_series['CSP_TES dispatch'] = time_series['CSP_TES dispatch'] * 0.3774
    tes_included = True
    colors.append(tes_c)
    techs.append('TES')
else:
    tes_included = False
    
if 'battery dispatch' in time_series.columns:
    battery_included = True
    colors.append(batt_c)
    techs.append('Battery')
else:
    battery_included = False
    
if 'from_PGP dispatch' in time_series.columns:
    pgp_included = True
    colors.append(pgp_c)
    techs.append('PGP')
else:
    pgp_included = False
    
num_storage = tes_included + battery_included + pgp_included

##==========================================
# Group data by time period of interest and sum
##==========================================

hourly_series = time_series.groupby(by='Hour').mean()
monthly_series = time_series.groupby(by='Month').mean()
monthly_series['plot_m'] = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul',
                            'Aug', 'Sep', 'Oct','Nov','Dec']
cols = []

if tes_included:
    cols.append('CSP_TES in dispatch')
    cols.append('CSP_TES dispatch')
    cols.append('CSP_TES in dispatch')
    cols. append('CSP_TES dispatch')
if battery_included:
    cols.append('battery in dispatch')
    cols.append('battery dispatch')
    cols.append('battery in dispatch')
    cols.append('battery dispatch')
if pgp_included:
    cols.append('to_PGP dispatch')
    cols.append('from_PGP dispatch')
    cols.append('to_PGP dispatch')
    cols.append('from_PGP dispatch')

##==========================================
# Plot the data
##==========================================
params = {'legend.fontsize': 'large',
         'axes.labelsize': 'large',
         'axes.titlesize':'large',
         'xtick.labelsize':'medium',
         'ytick.labelsize':'large'}
pylab.rcParams.update(params)


fig = plt.figure(figsize = (14,7.5)) 

ax3 = fig.add_subplot(num_storage, 2, 1)
ax3.plot(monthly_series.plot_m,monthly_series['battery in dispatch'], 
         marker = 's', ls = ':', lw = 3, c='tan')
plt.setp(ax3, ylabel = 'Battery (kW)')
ax3.plot(monthly_series.plot_m,monthly_series['battery dispatch'], 
         marker = '^', ls = ':', lw = 3, c=batt_c)
ax4 = fig.add_subplot(num_storage, 2, 2,sharey = ax3)
ax4.plot(hourly_series.index, hourly_series['battery in dispatch'], 
         marker = 's', ls = ':', lw = 3, c='tan', label = 'Battery Charging')
ax4.plot(hourly_series.index, hourly_series['battery dispatch'], 
         marker = '^', ls = ':', lw = 3, c=batt_c, label = 'Battery Discharging')

ax5 = fig.add_subplot(num_storage, 2, 3)
ax5.plot(monthly_series.plot_m,monthly_series['to_PGP dispatch'], 
         marker = 's', ls = ':', lw = 3, c='tan')
plt.setp(ax5, ylabel = 'PGP (kW)')
ax5.plot(monthly_series.plot_m, monthly_series['from_PGP dispatch'], 
         marker = '^', ls = ':', lw = 3, c=pgp_c)
ax6 = fig.add_subplot(num_storage, 2, 4, sharey = ax5)
ax6.plot(hourly_series.index, hourly_series['to_PGP dispatch'], 
         marker = 's', ls = ':', lw = 3, c='tan', label = 'PGP Charging')
ax6.plot(hourly_series.index, hourly_series['from_PGP dispatch'], 
         marker = '^', ls = ':', lw = 3, c=pgp_c, label = 'PGP Discharging')

axes = [ax3,ax4,ax5,ax6]

for x in axes:
    x.spines['right'].set_visible(False)
    x.spines['top'].set_visible(False)

ax4.legend(loc='upper center', bbox_to_anchor=(1, .98),frameon = False, fontsize = 'x-large')
ax6.legend(loc='upper center', bbox_to_anchor=(1, .98),frameon = False, fontsize = 'x-large')
fig.suptitle('Charging and Discharging per kW Mean US Demand', y=1.02, size ='xx-large')

fig.tight_layout(pad = 1.5)
fig.text(0.22,-0.01,'Month of Year', size = 'x-large')
fig.text(0.67,-0.01,'Hour of Day (CST)', size = 'x-large')

fig.text(0.01,0.94,'a)', size = 'x-large')
fig.text(0.45,0.94,'b)', size = 'x-large')
fig.text(0.01,0.44,'c)', size = 'x-large')
fig.text(0.45,0.44,'d)', size = 'x-large')

plt.tight_layout(True)
plt.savefig('PaperFigures/SI/figure_s3_charge_discharge.jpg', dpi=300, bbox_inches='tight')
plt.show()
