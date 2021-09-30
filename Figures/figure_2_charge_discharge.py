# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 09:45:26 2021

@author: Kathleen Kennedy
"""
##=========================================================
# Time of day and year when storage is charged/discharged
##=========================================================

import numpy as np
import pandas as pd
import pickle5 as pickle
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import datetime
import pylab

pgp_c = 'deeppink' 
batt_c = 'purple'
tes_c = 'cyan'
lost_load_c = 'gray'

##===========================================
# Read in pickle file
##===========================================

with open('C:/Users/Kathleen/Desktop/Temp/Combo_4_all_20210302-142006.pickle', 'rb') as handle:
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

if 'lost_load dispatch' in time_series.columns:
    lost_load_included = True
    colors.append(lost_load_c)
    techs.append('Lost Load')
else:
    lost_load_included = False
    
num_storage = tes_included + battery_included + pgp_included + lost_load_included

##==========================================
# Group data by time period of interest and average
##==========================================

hourly_series = time_series.groupby(by='Hour').mean()
monthly_series = time_series.groupby(by='Month').mean()
monthly_series['plot_m'] = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul',
                            'Aug', 'Sep', 'Oct','Nov','Dec']

##==========================================
# Plot the data
##==========================================
params = {'legend.fontsize': 'large',
         'axes.labelsize': 'x-large',
         'axes.titlesize':'x-large',
         'xtick.labelsize':'medium',
         'ytick.labelsize':'large'}
pylab.rcParams.update(params)


fig = plt.figure(figsize = (14,11)) #(17,12) when using lost load

ax1 = fig.add_subplot(num_storage, 2, 1)
ax1.plot(monthly_series.plot_m,monthly_series['CSP_TES in dispatch'], 
         marker = 's', ls = ':', lw = 3, c='tan')
plt.setp(ax1, ylabel = 'TES (kW)')
ax1.plot(monthly_series.plot_m,monthly_series['CSP_TES dispatch'],
         marker = '^', ls = ':', lw = 3, c=tes_c)
ax2 = fig.add_subplot(num_storage, 2, 2, sharey = ax1)
ax2.plot(hourly_series.index, hourly_series['CSP_TES in dispatch'], 
         marker = 's', ls = ':', lw = 3, c='tan', label = 'TES Charging')
ax2.plot(hourly_series.index, hourly_series['CSP_TES dispatch'], 
         marker = '^', ls = ':', lw = 3, c=tes_c, label = 'TES Discharging')

ax3 = fig.add_subplot(num_storage, 2, 3, sharey=ax1)
ax3.plot(monthly_series.plot_m,monthly_series['battery in dispatch'], 
         marker = 's', ls = ':', lw = 3, c='tan')
plt.setp(ax3, ylabel = 'Battery (kW)')
ax3.plot(monthly_series.plot_m,monthly_series['battery dispatch'], 
         marker = '^', ls = ':', lw = 3, c=batt_c)
ax4 = fig.add_subplot(num_storage, 2, 4,sharey = ax3)
ax4.plot(hourly_series.index, hourly_series['battery in dispatch'], 
         marker = 's', ls = ':', lw = 3, c='tan', label = 'Battery Charging')
ax4.plot(hourly_series.index, hourly_series['battery dispatch'], 
         marker = '^', ls = ':', lw = 3, c=batt_c, label = 'Battery Discharging')

ax5 = fig.add_subplot(num_storage, 2, 5)
ax5.plot(monthly_series.plot_m,monthly_series['to_PGP dispatch'], 
         marker = 's', ls = ':', lw = 3, c='tan')
plt.setp(ax5, ylabel = 'PGP (kW)')
ax5.plot(monthly_series.plot_m, monthly_series['from_PGP dispatch'], 
         marker = '^', ls = ':', lw = 3, c=pgp_c)
ax6 = fig.add_subplot(num_storage, 2, 6, sharey = ax5)
ax6.plot(hourly_series.index, hourly_series['to_PGP dispatch'], 
         marker = 's', ls = ':', lw = 3, c='tan', label = 'PGP Charging')
ax6.plot(hourly_series.index, hourly_series['from_PGP dispatch'], 
         marker = '^', ls = ':', lw = 3, c=pgp_c, label = 'PGP Discharging')
'''
ax7 = fig.add_subplot(num_storage, 2, 7)
ax7.plot(monthly_series.plot_m,monthly_series['lost_load dispatch'], 
         marker = '^', ls = ':', lw = 3, c=lost_load_c)
plt.setp(ax7, ylabel = 'Lost Load (kWh)')
ax8 = fig.add_subplot(num_storage, 2, 8, sharey = ax7)
ax8.plot(hourly_series.index,hourly_series['lost_load dispatch'], 
         marker = '^', ls = ':', lw = 3, c=lost_load_c, label = 'Lost Load')
'''
axes = [ax1,ax2,ax3,ax4,ax5,ax6]

for x in axes:
    x.spines['right'].set_visible(False)
    x.spines['top'].set_visible(False)

ax2.legend(loc='upper center', bbox_to_anchor=(1, .98),frameon = False, fontsize = 'x-large')
ax4.legend(loc='upper center', bbox_to_anchor=(1, .98),frameon = False, fontsize = 'x-large')
ax6.legend(loc='upper center', bbox_to_anchor=(1, .98),frameon = False, fontsize = 'x-large')
#ax8.legend(loc='upper center', bbox_to_anchor=(1.07, .98),frameon = False, fontsize = 'x-large')
fig.suptitle('Charging and Discharging per kW Mean US Demand', y=1.01, size ='xx-large')


fig.text(0.22,-0.01,'Month of Year', size = 'x-large')
fig.text(0.65,-0.01,'Hour of Day (CST)', size = 'x-large')

fig.text(0.02,0.96,'a)', size = 'x-large')
fig.text(0.46,0.96,'b)', size = 'x-large')
fig.text(0.02,0.64,'c)', size = 'x-large')
fig.text(0.46,0.64,'d)', size = 'x-large')
fig.text(0.02,0.335,'e)', size = 'x-large')
fig.text(0.46,0.335,'f)', size = 'x-large')
#fig.text(0.02,0.25,'g)', size = 'x-large')
#fig.text(0.46,0.25,'h)', size = 'x-large')

plt.tight_layout(pad = 1.5) 
plt.savefig('PaperFigures/figure_2_charge_discharge.jpg', dpi=300,bbox_inches='tight')
plt.show()
