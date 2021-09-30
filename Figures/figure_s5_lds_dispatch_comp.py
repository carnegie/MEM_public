# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 18:47:44 2020

@author: Kathleen
"""
##=========================================
# Figure 2: Dispatch curves and times
##=========================================

import copy
import numpy as np

import pickle
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.pylab as pylab

import datetime
from matplotlib.dates import HourLocator, AutoDateLocator, DateFormatter, drange

PV_c = 'orange' 
wind_c = 'blue' 
pgp_c = 'pink' 
batt_c = 'purple'
dem_c = 'black'
csp_c = 'yellow'
tes_c = 'cyan'
lost_load_c = 'gray'

##===========================================
#Read in pickle file
##===========================================

with open('C:/Users/Kathleen/Desktop/Temp/SimpleCombos/ZCombo2_batt_20210302-134330.pickle', 'rb') as handle:
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

##===========================================
def func_find_period (input_data):
    
    window_size = input_data['window_size']
    eff_window_size = copy.deepcopy(window_size) # If even go up to next odd number
    if eff_window_size == 2 * int (eff_window_size /2 ):  # check if even
        eff_window_size = eff_window_size + 1             # if so, add 1
    data = input_data['data']
    search_option = input_data['search_option']
    print_option = input_data['print_option']
    
    # -------------------------------------------------------------------------
    
    # Get the down-scaled data
    data_in_window = func_time_conversion(data, eff_window_size, 'mean')
    
    # -------------------------------------------------------------------------
    
    if search_option == 'max':
        
        center_index = int(np.argmax(data_in_window))
        value = np.max(data_in_window)
        
    elif search_option == 'min':

        center_index = int(np.argmin(data_in_window))
        value = np.min(data_in_window)

    # -------------------------------------------------------------------------
    # If interval would go over boundary, then move inteval
    if center_index < int(eff_window_size/2):
        center_index = int(eff_window_size/2)
    if center_index > len(data)- int(eff_window_size/2) - 1:
        center_index = len(data) - 1 - int(eff_window_size/2)

    # The same algorithm as in func_time_conversion()

    left_index = center_index - int(eff_window_size/2)
    right_index = center_index + int(eff_window_size/2)

    # -------------------------------------------------------------------------

    # output
    if print_option == 1:
        
        print ( 'center index = {}, value = {}'.format(center_index, value))
        print ( 'left index = {}, right index = {}'.format(left_index, right_index))

    output = {
        'value':        value,
        'left_index':   left_index,
        'right_index':  right_index,
        'center_index': center_index,
        }

    return output

##========================================================
def convert_start_end (start_hour, end_hour):
    start_m = -1
    start_h = -1
    start_d = -1
    hours_remaining_in_month = -1
    for i, month in enumerate(months):
        if start_hour < month:
            start_m = i
            hours_remaining_in_month = start_hour - months[i-1]
            break
    
    if hours_remaining_in_month > 0:
        start_d = hours_remaining_in_month // 24 + 1
        start_h = hours_remaining_in_month % 24
    else:
        print("Error")

    end_m = -1
    end_h = -1
    end_d = -1
    hours_remaining_in_month = -1
    for i, month in enumerate(months):
        if end_hour < month:
            end_m = i
            hours_remaining_in_month = end_hour - months[i-1]
            break
    
    if hours_remaining_in_month > 0:
        end_d = hours_remaining_in_month // 24 + 1
        end_h = hours_remaining_in_month % 24
    else:
        print("Error")
    
    return start_m, start_d, start_h, end_m, end_d, end_h


##===========================================================================================================
# Define Sources and Sinks
##============================================================================================================

# 5-day averaging
hours_to_avg = 5*24
sources = []
sinks = []
pal1 = []
pal2 = []
labels1 = []

demand_source = func_time_conversion(results_time['demand potential'], hours_to_avg)

try:
    wind_source = func_time_conversion(results_time['wind potential'], hours_to_avg)
    sources.append(wind_source)
    pal1.append(wind_c)
    labels1.append('Wind')
    wind_included = True
except: 
    print('No wind')
    wind_included = False

try:
    PV_source = func_time_conversion(results_time['PV potential'], hours_to_avg)
    sources.append(PV_source)
    pal1.append(PV_c)
    labels1.append('PV')
    PV_included = True
except: 
    print('No PV')
    PV_included = False

try:
    tes_source = func_time_conversion(results_time['CSP_TES dispatch'], hours_to_avg) * 0.3774
    sources.append(tes_source)
    pal1.append(tes_c)
    labels1.append('TES')
    tes_included = True
except: 
    print('No TES')
    tes_included = False


try:
    csp_source = func_time_conversion(results_time['CSP_turbine dispatch'], hours_to_avg)
    csp_included = True
    if tes_included:
        csp_source = csp_source - tes_source
        sources.insert(-1, csp_source)
        pal1.insert(-1, csp_c)
        labels1.insert(-1, 'CSP')
    else:
        sources.append(csp_source)
        pal1.append(csp_c)
        labels1.append('CSP')
except: 
    print('No CSP')
    csp_included = False

try:
    batt_source = func_time_conversion(results_time['battery dispatch'], hours_to_avg)
    sources.append(batt_source)
    pal1.append(batt_c)
    labels1.append('Battery')
    batt_included = True
except: 
    print('No Batteries')
    batt_included = False

try:
    pgp_source = func_time_conversion(results_time['from_PGP dispatch'], hours_to_avg)
    sources.append(pgp_source)
    pal1.append(pgp_c)
    labels1.append('PGP')
    pgp_included = True
except: 
    print('No PGP')
    pgp_included = False
    
try:
    lost_load = func_time_conversion(results_time['lost_load dispatch'], hours_to_avg)
    sources.append(lost_load)
    pal1.append(lost_load_c)
    labels1.append('Lost Load')
    lost_load_included = True
except:
    print('No Lost Load')
    lost_load_included = False

demand_sink = np.multiply(func_time_conversion(results_time['demand potential'], hours_to_avg), -1)
sinks.append(demand_sink)
pal2.append(dem_c)

try:
    tes_sink = np.multiply(func_time_conversion(results_time['CSP_TES in dispatch'], hours_to_avg), -1) * 0.3774
    sinks.append(tes_sink)
    pal2.append(tes_c)
except: print('No TES')

try:
    batt_sink = np.multiply(func_time_conversion(results_time['battery in dispatch'], hours_to_avg), -1)
    sinks.append(batt_sink)
    pal2.append(batt_c)
except: print('No Batteries')

try:
    pgp_sink = np.multiply(func_time_conversion(results_time['to_PGP dispatch'], hours_to_avg), -1)
    sinks.append(pgp_sink)
    pal2.append(pgp_c)
except: print('No PGP')

num_storage = tes_included + batt_included + pgp_included
#num_cols = num_storage + 3
num_cols = 6

#=======================================================
# Plot dispatch curve
#=======================================================

params = {'legend.fontsize': 'large',
          'figure.figsize': (17, 15), 
          'axes.labelsize': 'x-large',
          'axes.titlesize': 'x-large',
          'xtick.labelsize': 'large',
          'ytick.labelsize': 'large'}
pylab.rcParams.update(params)

date1 = datetime.datetime(2017, 1, 1, 0)
date2 = datetime.datetime(2017, 12, 31, 23)
delta = datetime.timedelta(hours=1)
quick_dates = drange(date1, date2, delta)
x = quick_dates


y1 = np.vstack(sources)
y2 = np.vstack(sinks)
labels2 = ["Demand"]


fig = plt.figure() #constrained_layout=True
ax3 = plt.subplot2grid((4, num_cols), (0, 0), colspan=3, rowspan=2)
ax3.stackplot(x, y1, colors=pal1, labels=labels1)
ax3.stackplot(x, y2, colors=pal2, labels=labels2)
ax3.plot(x, demand_source, '-', color=dem_c, linewidth=1.2)
ax3.set_xlim(quick_dates[0], quick_dates[-1])
ax3.set_ylim(-2,3.5)
ax3.spines['top'].set_visible(False)
ax3.spines['right'].set_visible(False)
ax3.xaxis.set_major_locator(AutoDateLocator())
ax3.xaxis.set_major_formatter(DateFormatter('%b'))
ax3.xaxis.set_tick_params(direction='out', which='both')
ax3.yaxis.set_tick_params(direction='out', which='both')
ax3.yaxis.set_major_locator(ticker.MultipleLocator(1))


##=====================================================
# Define sources and Sinks for Panels
##=====================================================
demand_source = results_time['demand potential']
if wind_included:
    wind_source = results_time['wind potential']
if PV_included:
    pv_source = results_time['PV potential']
if batt_included:
    batt_source = results_time['battery dispatch']
if tes_included:
    tes_source = results_time['CSP_TES dispatch'] * 0.3774
if csp_included:
    csp_source = results_time['CSP_turbine dispatch'] 
    if tes_included:
        csp_source = csp_source - tes_source
if pgp_included:
    pgp_source = results_time['from_PGP dispatch']
if lost_load_included:
    ll_source = results_time['lost_load dispatch']

demand_sink = results_time['demand potential']
if batt_included:
    batt_sink = results_time['battery in dispatch']
if tes_included:
    tes_sink = results_time['CSP_TES in dispatch'] * 0.3774
if pgp_included:
    pgp_sink = results_time['to_PGP dispatch']

start_hours = []
end_hours = []
if tes_included:
    study_variable_dict_1 = {
        'window_size':      4*24,
        'data':             results_time['CSP_TES dispatch'], 
        'print_option':     0,
        'search_option':    'max'
        }
    study_output_1 = func_find_period(study_variable_dict_1)
    start_hours.append(study_output_1['left_index'])
    end_hours.append(study_output_1['right_index'])

if batt_included:
    study_variable_dict_2 = {
        'window_size':      4*24,
        'data':             results_time['battery dispatch'], 
        'print_option':     0,
        'search_option':    'max'
        }
    study_output_2 = func_find_period(study_variable_dict_2)
    start_hours.append(study_output_2['left_index'])
    end_hours.append(study_output_2['right_index'])

if pgp_included:
    study_variable_dict_3 = {
        'window_size':      4*24,
        'data':             results_time['from_PGP dispatch'], 
        'print_option':     0,
        'search_option':    'max'
        }
    study_output_3 = func_find_period(study_variable_dict_3)
    start_hours.append(study_output_3['left_index'])
    end_hours.append(study_output_3['right_index'])

##=================================================
# Convert hours to datetime units for plotting
##=================================================

months = [0]
months.append(months[0] + 31*24)
months.append(months[1] + 28*24)
months.append(months[2] + 31*24)
months.append(months[3] + 30*24) 
months.append(months[4] + 31*24)
months.append(months[5] + 30*24)
months.append(months[6] + 31*24) 
months.append(months[7] + 31*24) 
months.append(months[8] + 30*24) 
months.append(months[9] + 31*24)  
months.append(months[10] + 30*24)   
months.append(months[11] + 31*24)   

##=================================================
# Loop to plot panels of max storage dispatch
##=================================================

for i in range(num_storage):
    start_hour = start_hours[i]
    end_hour = end_hours[i]
    times = convert_start_end(start_hour - 6, end_hour - 6) # -6 converts UTC to CST
    
    date1 = datetime.datetime(2017, times[0], times[1], times[2])
    date2 = datetime.datetime(2017, times[3], times[4], times[5])

    delta = datetime.timedelta(hours=1)
    dates = drange(date1, date2, delta)

    x = dates
    
    sources = []
    demand_source1 = demand_source[start_hour:end_hour]
    
    demand_sink1 = np.multiply(demand_sink[start_hour:end_hour],-1)
    sinks = [demand_sink1]
    
    if wind_included:
        wind_source1 = wind_source[start_hour:end_hour]
        sources.append(wind_source1)
    if PV_included:
        pv_source1 = pv_source[start_hour:end_hour]
        sources.append(pv_source1)
    if csp_included:
        csp_source1 = csp_source[start_hour:end_hour]
        sources.append(csp_source1)
    if tes_included:
        tes_source1 = tes_source[start_hour:end_hour]
        sources.append(tes_source1)
        tes_sink1 = np.multiply(tes_sink[start_hour:end_hour],-1)
        sinks.append(tes_sink1)
    if batt_included:
        batt_source1 = batt_source[start_hour:end_hour]
        sources.append(batt_source1)
        batt_sink1 = np.multiply(batt_sink[start_hour:end_hour],-1)
        sinks.append(batt_sink1)
    if pgp_included:
        pgp_source1 = pgp_source[start_hour:end_hour]
        sources.append(pgp_source1)
        pgp_sink1 = np.multiply(pgp_sink[start_hour:end_hour],-1)
        sinks.append(pgp_sink1)
    if lost_load_included:
        ll_source1 = ll_source[start_hour:end_hour]
        sources.append(ll_source1)

    y1 = np.vstack(sources)
    y2 = np.vstack(sinks)
    
    ax = plt.subplot2grid((4, num_cols), (0, 3+i), colspan=1, rowspan=2)
    ax.stackplot(x, y1, colors=pal1, labels=labels1)
    ax.stackplot(x, y2, colors=pal2, labels=labels2)
    ax.plot(x, demand_source1, '-', color=dem_c, linewidth=1.2)

    ax.set_xlim(dates[0], dates[-1])
    ax.set_ylim(-2,3.5)
    
    ax.xaxis.set_major_locator(HourLocator(byhour=range(24),interval=24))
    ax.xaxis.set_major_formatter(DateFormatter('%b %d')) #This is CST!!! 7am
    plt.setp(ax.get_yticklabels(), visible=False)
    ax.yaxis.set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    ax.yaxis.set_major_locator(ticker.MultipleLocator(1))
    plt.xticks(rotation=30, ha='right')
    ax.xaxis.set_tick_params(direction='out', which='both')
    ax.yaxis.set_tick_params(direction='out', which='both')
 
ax.legend(loc='upper center', bbox_to_anchor=(1.36, 1.02),frameon=False)

##===========================================
#Read in pickle file
##===========================================

with open('C:/Users/Kathleen/Desktop/Temp/SimpleCombos/ZCombo5_all_20210302-142006.pickle', 'rb') as handle:
            [[input_case,  input_tech,  input_time],
             [results_case, results_tech,  results_time]] = pickle.load(handle)

##===========================================================================================================
# Define Sources and Sinks
##============================================================================================================

sources = []
sinks = []
pal1 = []
pal2 = []
labels1 = []

demand_source = func_time_conversion(results_time['demand potential'], hours_to_avg)

try:
    wind_source = func_time_conversion(results_time['wind potential'], hours_to_avg)
    sources.append(wind_source)
    pal1.append(wind_c)
    labels1.append('Wind')
    wind_included = True
except: 
    print('No wind')
    wind_included = False

try:
    PV_source = func_time_conversion(results_time['PV potential'], hours_to_avg)
    sources.append(PV_source)
    pal1.append(PV_c)
    labels1.append('PV')
    PV_included = True
except: 
    print('No PV')
    PV_included = False

try:
    tes_source = func_time_conversion(results_time['CSP_TES dispatch'], hours_to_avg) * 0.3774
    sources.append(tes_source)
    pal1.append(tes_c)
    labels1.append('TES')
    tes_included = True
except: 
    print('No TES')
    tes_included = False


try:
    csp_source = func_time_conversion(results_time['CSP_turbine dispatch'], hours_to_avg)
    csp_included = True
    if tes_included:
        csp_source = csp_source - tes_source
        sources.insert(-1, csp_source)
        pal1.insert(-1, csp_c)
        labels1.insert(-1, 'CSP')
    else:
        sources.append(csp_source)
        pal1.append(csp_c)
        labels1.append('CSP')
except: 
    print('No CSP')
    csp_included = False

try:
    batt_source = func_time_conversion(results_time['battery dispatch'], hours_to_avg)
    sources.append(batt_source)
    pal1.append(batt_c)
    labels1.append('Battery')
    batt_included = True
except: 
    print('No Batteries')
    batt_included = False

try:
    pgp_source = func_time_conversion(results_time['from_PGP dispatch'], hours_to_avg)
    sources.append(pgp_source)
    pal1.append(pgp_c)
    labels1.append('PGP')
    pgp_included = True
except: 
    print('No PGP')
    pgp_included = False
try:
    lost_load = func_time_conversion(results_time['lost_load dispatch'], hours_to_avg)
    sources.append(lost_load)
    pal1.append(lost_load_c)
    labels1.append('Lost Load')
    lost_load_included = True
except:
    print('No Lost Load')
    lost_load_included = False
    
demand_sink = np.multiply(func_time_conversion(results_time['demand potential'], hours_to_avg), -1)
sinks.append(demand_sink)
pal2.append(dem_c)
try:
    tes_sink = np.multiply(func_time_conversion(results_time['CSP_TES in dispatch'], hours_to_avg), -1) * 0.3774
    sinks.append(tes_sink)
    pal2.append(tes_c)
except: print('No TES')

try:
    batt_sink = np.multiply(func_time_conversion(results_time['battery in dispatch'], hours_to_avg), -1)
    sinks.append(batt_sink)
    pal2.append(batt_c)
except: print('No Batteries')

try:
    pgp_sink = np.multiply(func_time_conversion(results_time['to_PGP dispatch'], hours_to_avg), -1)
    sinks.append(pgp_sink)
    pal2.append(pgp_c)
except: print('No PGP')

num_storage = tes_included + batt_included + pgp_included
#num_cols = num_storage + 3

##============================================
# Plot second Dispatch Curve
##============================================
date1 = datetime.datetime(2017, 1, 1, 0)
date2 = datetime.datetime(2017, 12, 31, 23)
delta = datetime.timedelta(hours=1)
quick_dates = drange(date1, date2, delta)
x = quick_dates

y1 = np.vstack(sources)
y2 = np.vstack(sinks)
labels2 = ["Demand"]

ax4 = plt.subplot2grid((4, num_cols), (2, 0), colspan=3, rowspan=2)
ax4.stackplot(x, y1, colors=pal1, labels=labels1)
ax4.stackplot(x, y2, colors=pal2, labels=labels2)
ax4.plot(x, demand_source, '-', color=dem_c, linewidth=1.2)
ax4.set_xlim(quick_dates[0], quick_dates[-1])
ax4.set_ylim(-2,3.5)
ax4.spines['top'].set_visible(False)
ax4.spines['right'].set_visible(False)
ax4.xaxis.set_major_locator(AutoDateLocator())
ax4.xaxis.set_major_formatter(DateFormatter('%b'))
ax4.xaxis.set_tick_params(direction='out', which='both')
ax4.yaxis.set_tick_params(direction='out', which='both')
ax4.yaxis.set_major_locator(ticker.MultipleLocator(1))


##=====================================================
# Define sources and Sinks for Panels
##=====================================================

demand_source = results_time['demand potential']
if wind_included:
    wind_source = results_time['wind potential']
if PV_included:
    pv_source = results_time['PV potential']
if batt_included:
    batt_source = results_time['battery dispatch']
if tes_included:
    tes_source = results_time['CSP_TES dispatch'] * 0.3774
if csp_included:
    csp_source = results_time['CSP_turbine dispatch'] 
    if tes_included:
        csp_source = csp_source - tes_source
if pgp_included:
    pgp_source = results_time['from_PGP dispatch']
if lost_load_included:
    ll_source = results_time['lost_load dispatch']
    
demand_sink = results_time['demand potential']
if batt_included:
    batt_sink = results_time['battery in dispatch']
if tes_included:
    tes_sink = results_time['CSP_TES in dispatch'] * 0.3774
if pgp_included:
    pgp_sink = results_time['to_PGP dispatch']


start_hours = []
end_hours = []
if tes_included:
    study_variable_dict_1 = {
        'window_size':      4*24,
        'data':             results_time['CSP_TES dispatch'], 
        'print_option':     0,
        'search_option':    'max'
        }
    study_output_1 = func_find_period(study_variable_dict_1)
    start_hours.append(study_output_1['left_index'])
    end_hours.append(study_output_1['right_index'])

if batt_included:
    study_variable_dict_2 = {
        'window_size':      4*24,
        'data':             results_time['battery dispatch'], 
        'print_option':     0,
        'search_option':    'max'
        }
    study_output_2 = func_find_period(study_variable_dict_2)
    start_hours.append(study_output_2['left_index'])
    end_hours.append(study_output_2['right_index'])

if pgp_included:
    study_variable_dict_3 = {
        'window_size':      4*24,
        'data':             results_time['from_PGP dispatch'], 
        'print_option':     0,
        'search_option':    'max'
        }
    study_output_3 = func_find_period(study_variable_dict_3)
    start_hours.append(study_output_3['left_index'])
    end_hours.append(study_output_3['right_index'])

##=================================================
# Convert hours to datetime units for plotting
##=================================================

months = [0]
months.append(months[0] + 31*24)
months.append(months[1] + 28*24)
months.append(months[2] + 31*24)
months.append(months[3] + 30*24) 
months.append(months[4] + 31*24)
months.append(months[5] + 30*24)
months.append(months[6] + 31*24) 
months.append(months[7] + 31*24) 
months.append(months[8] + 30*24) 
months.append(months[9] + 31*24)  
months.append(months[10] + 30*24)   
months.append(months[11] + 31*24)   

##=================================================
# Loop to plot panels of max storage dispatch
##=================================================

for i in range(num_storage):
    start_hour = start_hours[i]
    end_hour = end_hours[i]
    times = convert_start_end(start_hour - 6, end_hour - 6) # -6 converts UTC to CST
    
    date1 = datetime.datetime(2017, times[0], times[1], times[2])
    date2 = datetime.datetime(2017, times[3], times[4], times[5])

    delta = datetime.timedelta(hours=1)
    dates = drange(date1, date2, delta)

    x = dates
    
    sources = []
    demand_source1 = demand_source[start_hour:end_hour]
    
    demand_sink1 = np.multiply(demand_sink[start_hour:end_hour],-1)
    sinks = [demand_sink1]
    
    if wind_included:
        wind_source1 = wind_source[start_hour:end_hour]
        sources.append(wind_source1)
    if PV_included:
        pv_source1 = pv_source[start_hour:end_hour]
        sources.append(pv_source1)
    if csp_included:
        csp_source1 = csp_source[start_hour:end_hour]
        sources.append(csp_source1)
    if tes_included:
        tes_source1 = tes_source[start_hour:end_hour]
        sources.append(tes_source1)
        tes_sink1 = np.multiply(tes_sink[start_hour:end_hour],-1)
        sinks.append(tes_sink1)
    if batt_included:
        batt_source1 = batt_source[start_hour:end_hour]
        sources.append(batt_source1)
        batt_sink1 = np.multiply(batt_sink[start_hour:end_hour],-1)
        sinks.append(batt_sink1)
    if pgp_included:
        pgp_source1 = pgp_source[start_hour:end_hour]
        sources.append(pgp_source1)
        pgp_sink1 = np.multiply(pgp_sink[start_hour:end_hour],-1)
        sinks.append(pgp_sink1)
    if lost_load_included:
        ll_source1 = ll_source[start_hour:end_hour]
        sources.append(ll_source1)

    y1 = np.vstack(sources)
    y2 = np.vstack(sinks)
    
    ax = plt.subplot2grid((4, num_cols), (2, 3+i), colspan=1, rowspan=2)
    ax.stackplot(x, y1, colors=pal1, labels=labels1)
    ax.stackplot(x, y2, colors=pal2, labels=labels2)
    ax.plot(x, demand_source1, '-', color=dem_c, linewidth=1.2)

    ax.set_xlim(dates[0], dates[-1])
    ax.set_ylim(-2,3.5)
    
    ax.xaxis.set_major_locator(HourLocator(byhour=range(24),interval=24))
    ax.xaxis.set_major_formatter(DateFormatter('%b %d')) #This is CST!!! 7am
    plt.setp(ax.get_yticklabels(), visible=False)
    ax.yaxis.set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    ax.yaxis.set_major_locator(ticker.MultipleLocator(1))
    plt.xticks(rotation=30, ha='right')
    ax.xaxis.set_tick_params(direction='out', which='both')
    ax.yaxis.set_tick_params(direction='out', which='both')
 
ax.legend(loc='upper center', bbox_to_anchor=(1.36, 0.98),frameon=False)

fig.text(0.085, 0.5, 'Electricty sources and sinks (kW)', va='center', rotation='vertical', size='xx-large' )
fig.text(.10, 0.87, 'a)', size='large')
fig.text(.52, 0.87, 'b)', size='large')
fig.text(.66, 0.87, 'c)', size='large')

fig.text(.10, 0.46, 'd)', size='large')
fig.text(.52, 0.46, 'e)', size='large')
fig.text(.66, 0.46, 'f)', size='large')
fig.text(.80, 0.46, 'g)', size='large')

#plt.tight_layout(True)
plt.savefig('PaperFigures/SI/figure_s4_lds_dispatch.jpg', dpi=300, bbox_inches='tight')
plt.show()