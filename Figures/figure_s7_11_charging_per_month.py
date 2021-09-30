# -*- coding: utf-8 -*-
"""
Created on Fri Mar  5 15:07:51 2021

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
# For base case
with open('C:/Users/Kathleen/Desktop/Temp/SimpleCombos/ZCombo5_all_20210302-142006.pickle', 'rb') as handle:
            [[input_case,  input_tech,  input_time],
             [results_case, results_tech,  results_time]] = pickle.load(handle)
'''
# For no LDS cases
with open('C:/Users/Kathleen/Desktop/Temp/SimpleCombos/ZCombo2_batt_20210302-134330.pickle', 'rb') as handle:
            [[input_case,  input_tech,  input_time],
             [results_case, results_tech,  results_time]] = pickle.load(handle)
'''
##=================================================
# Match up the dates, prep data
##=================================================
dates = np.arange('2017-01-01 00', '2018-01-01 00', dtype = 'datetime64[h]')
dates = dates - np.timedelta64(6,'h') # convert from UTC to CST
time_series = pd.DataFrame(results_time,index = dates)
time_series['Hour'] = time_series.index.hour
time_series['Month'] = time_series.index.month
colors = []
techs = []

# Convert kWht to kWhe for TES - multiply by turbine efficiency 
if 'CSP_TES dispatch' in time_series.columns:
    time_series['CSP_TES in dispatch'] = time_series['CSP_TES in dispatch'] * 0.3774
    time_series['CSP_TES dispatch'] = time_series['CSP_TES dispatch'] * 0.3774

hours = np.linspace(0,23,24)
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul',
                            'Aug', 'Sep', 'Oct','Nov','Dec']
##==========================================
# Group data by time period of interest and average
##==========================================

data_tes = time_series.groupby(['Month', 'Hour']).agg({'CSP_TES dispatch': ['mean']}).reset_index()
data_tesc = time_series.groupby(['Month', 'Hour']).agg({'CSP_TES in dispatch': ['mean']}).reset_index()
data_batt = time_series.groupby(['Month', 'Hour']).agg({'battery dispatch': ['mean']}).reset_index()
data_battc = time_series.groupby(['Month', 'Hour']).agg({'battery in dispatch': ['mean']}).reset_index()
try:
    data_pgp = time_series.groupby(['Month', 'Hour']).agg({'from_PGP dispatch': ['mean']}).reset_index()
    data_pgpc = time_series.groupby(['Month', 'Hour']).agg({'to_PGP dispatch': ['mean']}).reset_index()
except:
    print('No PGP')
##==========================================
# Plot the data
##==========================================
params = {'legend.fontsize': 'large',
         'axes.labelsize': 'x-large',
         'axes.titlesize':'x-large',
         'xtick.labelsize':'large',
         'ytick.labelsize':'large'}
pylab.rcParams.update(params)

fig = plt.figure(figsize = (15,10))

for m in data_tes['Month'].unique():
    ax = fig.add_subplot(3, 4, m)
    ax.plot(hours, data_tes[data_tes['Month']==m]['CSP_TES dispatch']['mean'], 
            marker = 's', ls = ':', lw = 3, c=tes_c, label = 'TES Discharging')
    ax.plot(hours, data_tesc[data_tesc['Month']==m]['CSP_TES in dispatch']['mean'], 
            marker = 's', ls = ':', lw = 3, c='tan', label = 'TES Charging')
    ax.set_title(months[m-1], y=0.9)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_ylim(0,0.058)
    if m == 4:
        ax.legend(bbox_to_anchor=(1, .85),frameon=False)

fig.text(-.01, 0.5, 'Average Charging/Discharging (kW)', va='center', rotation='vertical', size='x-large' )
fig.text(0.47,-0.01,'Hour of Day (CST)', size = 'x-large')
fig.suptitle('TES Charging and Discharging in TES/Batt Case', y=1.015, size ='15')
plt.tight_layout(True)
plt.savefig('PaperFigures/SI/figure_s6_monthly.jpg', dpi=300, bbox_inches='tight')
plt.show()

#=================================================

fig = plt.figure(figsize = (15,10))

for m in data_batt['Month'].unique():
    ax = fig.add_subplot(3, 4, m)
    ax.plot(hours, data_batt[data_batt['Month']==m]['battery dispatch']['mean'], 
            marker = 's', ls = ':', lw = 3, c=batt_c, label = 'Battery Discharging')
    ax.plot(hours, data_battc[data_battc['Month']==m]['battery in dispatch']['mean'], 
            marker = 's', ls = ':', lw = 3, c='tan', label = 'Battery Charging')
    ax.set_title(months[m-1], y=0.9)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_ylim(0,0.23)
    if m == 4:
        ax.legend(bbox_to_anchor=(1, .85),frameon=False)

fig.text(-.01, 0.5, 'Average Charging/Discharging (kW)', va='center', rotation='vertical', size='x-large' )
fig.text(0.47,-0.01,'Hour of Day (CST)', size = 'x-large')
fig.suptitle('Battery Charging and Discharging in TES/Batt Case', y=1.015, size ='15')
plt.tight_layout(True)
plt.savefig('PaperFigures/SI/figure_s7_monthly.jpg', dpi=300, bbox_inches='tight')
plt.show()

#=======================================

fig = plt.figure(figsize = (15,10))

for m in data_pgp['Month'].unique():
    ax = fig.add_subplot(3, 4, m)
    ax.plot(hours, data_pgp[data_pgp['Month']==m]['from_PGP dispatch']['mean'], 
            marker = 's', ls = ':', lw = 3, c=pgp_c, label = 'PGP Discharging')
    ax.plot(hours, data_pgpc[data_pgpc['Month']==m]['to_PGP dispatch']['mean'], 
            marker = 's', ls = ':', lw = 3, c='tan', label = 'PGP Discharging')
    ax.set_title(months[m-1],y=0.9)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_ylim(0,0.29)
    if m == 4:
        ax.legend(bbox_to_anchor=(1,.85),frameon=False)

fig.text(-.01, 0.5, 'Average Charging/Discharging (kW)', va='center', rotation='vertical', size='x-large' )
fig.text(0.47,-0.01,'Hour of Day (CST)', size = 'x-large')
fig.suptitle('PGP Charging and Discharging in TES/Batt/PGP Case', y=1.015, size ='15')
plt.tight_layout(True)
plt.savefig('PaperFigures/SI/figure_s8_monthly.jpg', dpi=300, bbox_inches='tight')
plt.show()
