# -*- coding: utf-8 -*-
"""
Created on Mon Sep 27 11:33:26 2021

@author: Kathleen
"""
##=========================================
# Figure S16: price of electricity over time
##=========================================

import copy
import numpy as np

import pickle
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.pylab as pylab

import datetime
from matplotlib.dates import HourLocator, AutoDateLocator, DateFormatter, drange


##===========================================
#Read in pickle file
##===========================================

with open('C:/Users/Kathleen/Desktop/Temp/Combo_4_all_20210302-142006.pickle', 'rb') as handle:
            [[input_case,  input_tech,  input_time],
             [results_case, results_tech,  results_time]] = pickle.load(handle)

##===========================================
#Supporting Functions
##===========================================
def func_time_conversion (input_data, window_size, operation_type = 'mean'):
    
    # NOTE: THIS FUNCTION HAS ONLY BEEN VERIFIED FOR PROPER WRAP-AROUND BEHAVIOR
    #       FOR 'mean'
    # For odd windows sizes, easy. For even need to consider ends where you have half hour of data.

    N_periods = len(input_data)
    input_data_x3 = np.concatenate((input_data,input_data,input_data))
    
    half_size = window_size / 2.
    half_size_full = int(half_size) # number of full things for the mean

    output_data = np.zeros(len(input_data))
    
    for ii in range(len(output_data)):
        if half_size != float (half_size_full): # odd number, easy
            if (operation_type == 'mean'):
                output_data[ii] = np.sum(input_data_x3[N_periods + ii - half_size_full : N_periods + ii + half_size_full + 1 ])/ float(window_size)
            elif(operation_type == 'min'):
                output_data[ii] = np.min(input_data_x3[N_periods + ii - half_size_full : N_periods + ii + half_size_full + 1 ])
            elif(operation_type == 'max'):
                output_data[ii] = np.max(input_data_x3[N_periods + ii - half_size_full : N_periods + ii + half_size_full  + 1])
            elif(operation_type == 'sum'):
                output_data[ii] = np.sum(input_data_x3[N_periods + ii - half_size_full : N_periods + ii + half_size_full  + 1])
        else: # even number need to include half of last ones
            if (operation_type == 'mean'):
                output_data[ii] = ( np.sum(input_data_x3[N_periods + ii - half_size_full : N_periods + ii + half_size_full ])  \
                        + input_data_x3[N_periods + ii - half_size_full -1 ] *0.5 +  input_data_x3[N_periods + ii + half_size_full + 1 ] *0.5) / window_size
            elif(operation_type == 'min'):
                output_data[ii] = np.min(input_data_x3[N_periods + ii - half_size_full -1 : N_periods + ii + half_size_full + 1 ])
            elif(operation_type == 'max'):
                output_data[ii] = np.max(input_data_x3[N_periods + ii - half_size_full -1 : N_periods + ii + half_size_full + 1 ])
            elif(operation_type == 'sum'):
                output_data[ii] = (
                        np.sum(input_data_x3[N_periods + ii - half_size_full : N_periods + ii + half_size_full ]) 
                        + input_data_x3[N_periods + ii - half_size_full -1 ] *0.5 +  input_data_x3[N_periods + ii + half_size_full + 1 ] *0.5
                        ) 
        
    return output_data

#=========================================================
# Try this with 5 day averaging and then without
#=========================================================
# 5-day averaging
hours_to_avg = 5*24
e_price = func_time_conversion(results_time['main_node price'], hours_to_avg)

# Look at one month
date1 = datetime.datetime(input_case['year_start'], 7, 1, 0)
date2 = datetime.datetime(input_case['year_start'], 8, 1, 0)
delta = datetime.timedelta(hours=1)
dates = drange(date1, date2, delta)

# July starts h=4344, Aug starts 5088
e_price_july = results_time['main_node price'][4344:5088]

#=========================================================
# Plot price of electricity year round
#=========================================================
params = {'legend.fontsize': 'large',
          'figure.figsize': (14, 12), 
          'axes.labelsize': 'x-large',
          'axes.titlesize': 'x-large',
          'xtick.labelsize': 'x-large',
          'ytick.labelsize': 'x-large'}
pylab.rcParams.update(params)

date1 = datetime.datetime(input_case['year_start'], input_case['month_start'], 
                          input_case['day_start'], input_case['hour_start'] -1)
date2 = datetime.datetime(input_case['year_end'], input_case['month_end'], 
                          input_case['day_end'], input_case['hour_end'] -1)
delta = datetime.timedelta(hours=1)
quick_dates = drange(date1, date2, delta)
x = quick_dates

fig = plt.figure() 
plt.plot(x, e_price)
ax = plt.gca()
ax.set_ylabel('Spot price of electricity ($/kW)')
ax.set_xlim(quick_dates[0], quick_dates[-1])
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.xaxis.set_major_locator(AutoDateLocator())
ax.xaxis.set_major_formatter(DateFormatter('%b'))
ax.xaxis.set_tick_params(direction='out', which='both')
ax.yaxis.set_tick_params(direction='out', which='both')
ax.yaxis.set_major_locator(ticker.MultipleLocator(1))
plt.tight_layout(True)
plt.savefig('PaperFigures/SI/figure_s16_electricity_price.jpg', dpi=300)
plt.show()
