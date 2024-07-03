# Import

from __future__ import division
import os
import sys

module_directory = r"C:/Users/covel/OneDrive/Desktop/Rerun-for-Anna/Dom Plotting Code"

# Add the directory to sys.path
if module_directory not in sys.path:
    sys.path.append(module_directory)

import copy
import numpy as np
from numpy import ma
import math as m
import pandas as pd
import string
import cmasher as cmr

import pickle
from numpy import genfromtxt
from scipy.interpolate import griddata
from matplotlib import rc
import matplotlib.pyplot as plt
plt.style.use('default')
import matplotlib.gridspec as gridspec
import matplotlib.ticker as ticker
import matplotlib.colors as colors
from matplotlib.pyplot import figure
from matplotlib.lines import Line2D

import datetime
from matplotlib.dates import DayLocator, MonthLocator, HourLocator, AutoDateLocator, DateFormatter, drange
from matplotlib.dates import MO, TU, WE, TH, FR, SA, SU, WeekdayLocator
from numpy import arange
from matplotlib.ticker import ScalarFormatter
from matplotlib.ticker import FormatStrFormatter
from matplotlib.ticker import NullFormatter
from mpl_toolkits.axes_grid1 import make_axes_locatable

import matplotlib.cm as cm
import matplotlib.mlab as mlab

import glob


# Plot Settings

# Colors

darkblue = '#4e79a7'
orange = '#f28e2b'
red = '#e15759'
lightblue = '#76b7b2'
green = '#59a14f'
yellow = '#edc948'
purple = '#b07aa1'
pink = '#ff9da7'
brown = '#9c755f'
gray = '#bab0ac'

cbar_pad = 0.15

# Font / Figure Size
import matplotlib.pylab as pylab
params = {'legend.fontsize': '7',
         'axes.labelsize': '7',
         'axes.titlesize': '7',
         'xtick.labelsize': '7',
         'ytick.labelsize': '7',
          
         'xtick.major.pad': '7',
         'ytick.major.pad': '7',
         'axes.titlepad': 35,
         'axes.labelpad': 15,
         
         'font.sans-serif':'Avenir',
          'axes.linewidth': 0.5,
         'xtick.major.width': 0.5,
         'ytick.major.width': 0.5}
pylab.rcParams.update(params)

def all_nonzero(arr_iter):
    """return non zero elements of all arrays as a np.array"""
    return np.concatenate([a[a != 0] for a in arr_iter])

# toc: total installed cost ($/kWh for energy costs, $/kW for power costs)
# fhc: fixed hourly cost ($/kWh/h for energy costs, $/kW/h for power costs)

hours_per_year = 8760 # number of hours in a year (h/yr)
crf = 0.0806 # capital recovery factor, assuming a discount rate of 7% and 30 year lifetime (%/yr)
fixed_om = 0.015 # Fixed O&M (% of capital cost)
fixed_ptilp = 0.015 # Fixed property tax, insurance, licencing, permiting (% of capital cost)

# functions to calculate fhc from toc of technologies
def get_energy_fhc(toc):
    return ((toc + fixed_om * toc) * crf) / hours_per_year

def get_energy_toc(fhc):
    return (fhc * hours_per_year) / crf / (1 + fixed_om)

def get_power_fhc(toc):
    return ((toc + fixed_ptilp * toc) * crf) / hours_per_year

def get_power_toc(fhc):
    return (fhc * hours_per_year) / crf / (1 + fixed_ptilp)

def reshape(data):
    # X and Y axes
    x = data['third_tech_energy_cost']
    y = data['third_tech_power_cost']
    
    X = list(set(x))
    X.sort()
    Y = list(set(y))
    Y.sort()
    
    for key in data.keys():
        if len(data[key]) > 0:
            data[key] = np.reshape(data[key], (len(Y), len(X)))
    
    data['X'] = X
    data['Y'] = Y

def existence(data):
    epsilon = 10**-3
    data['batt_exist'] = data['battery_cap'] > epsilon
    data['third_tech_exist'] = data['third_tech_energy_cap'] > epsilon
    
    # What is the number of technologies
    data['num_techs'] = sum([data['batt_exist'], data['third_tech_exist']])
    
    # Scatterplot data for if technology exists or not
    data['batt_exist_scatter_energy'] = all_nonzero(np.multiply(data['third_tech_energy_cost'], data['batt_exist']))
    data['batt_exist_scatter_power'] = all_nonzero(np.multiply(data['third_tech_power_cost'], data['batt_exist']))
    data['third_tech_exist_scatter_energy'] = all_nonzero(np.multiply(data['third_tech_energy_cost'], data['third_tech_exist']))
    data['third_tech_exist_scatter_power'] = all_nonzero(np.multiply(data['third_tech_power_cost'], data['third_tech_exist']))    
    data['both_exist_scatter_energy'] = all_nonzero(np.multiply(data['third_tech_energy_cost'], data['num_techs'] == 2))
    data['both_exist_scatter_power'] = all_nonzero(np.multiply(data['third_tech_power_cost'], data['num_techs'] == 2))
            
def prop(data):
    battery_dispatch = data['battery_tot_dispatch']
    third_tech_dispatch = data['third_tech_energy_tot_dispatch']
    tot_dispatch = sum(np.array([battery_dispatch, third_tech_dispatch]))
    data['battery_prop'] = np.divide(battery_dispatch, tot_dispatch)
    data['third_tech_prop'] = np.divide(third_tech_dispatch, tot_dispatch)
    
def storage_cost_cont(data):
    batt = data['batt_cost']
    third_tech = data['third_tech_cost']
    tot_storage_tech_cost = sum(np.array([batt, third_tech]))
    data['batt_cost_cont'] = np.divide(batt, tot_storage_tech_cost)
    data['third_tech_cost_cont'] = np.divide(third_tech, tot_storage_tech_cost)
    data['cost_eff_num_batt'] = np.divide(1, np.square(np.square(data['batt_cost_cont']) + np.square(data['third_tech_cost_cont'])))

# Import Data

from extract_data_param_Li_ion_X import get_data_one_power

# Two tech case
path = 'C:/Users/covel/OneDrive/Desktop/Rerun-for-Anna//Output_Data/For Fig 5/Param_Lion_X_MISO/'
data = get_data_one_power(path, 5, 'fixed_cost', 6, 'fixed_cost', False)
                          
data['third_tech_energy_cost'] = [get_energy_toc(i) for i in data['third_tech_energy_cost']]
data['third_tech_power_cost'] = [get_power_toc(i) for i in data['third_tech_power_cost']]

# One tech case
one_tech_path = "C:/Users/covel/OneDrive/Desktop/Rerun-for-Anna/Output_Data/For Figs 3 and 4/MISO/one_storage/Li-ion/"
one_tech_data = get_data_one_power(one_tech_path, 2, 'fixed_cost', 3, 'fixed_cost', False)

reshape(data)
existence(data)
prop(data)
storage_cost_cont(data)

# Functions for marking Li-ion and PGP energy/power-capacity total overnight costs

batt_energy_toc = 326.4
batt_power_toc = 250.92

pgp_energy_toc = 1.9992
pgp_power_toc = 1560.6

w=1
l=10

def current_PGP_current_li_ion(ax):
    energy_ticks = ax.twiny()
    energy_ticks.set_xlim(ax.get_xlim())
    energy_ticks.set_xticks([batt_energy_toc])
    energy_ticks.set_xticklabels(['Li-ion'])
    energy_ticks.tick_params(direction='inout', length=l, width=w, pad=2.5)
    
    power_ticks = ax.twinx()
    power_ticks.set_ylim(ax.get_ylim())
    power_ticks.set_yticks([batt_power_toc])
    power_ticks.set_yticklabels(['Li-ion'])
    power_ticks.tick_params(direction='inout', length=l, width=w, pad=2.5)

mm = 1/25.4 # millimeters in inches
fig_w = 172*mm
fig_h = (172/3)*mm
fig = plt.subplots(nrows=1,ncols=2, figsize=(fig_w, fig_h), dpi=300)

X = data['X']
Y = data['Y']

num_techs_cmap = cmr.get_sub_cmap('viridis_r', 0.02, 0.98)
cost_reduction_cmap = 'plasma_r'

###################################################
# Figure 2a: When do 1, 2, 3, technologies exist? #
###################################################

ax1 = plt.subplot2grid((1, 2), (0, 0), colspan=1, rowspan=1)
cbar_ylabel1 = 'Number of Technologies'

Z1 = data['num_techs']
cpf1 = ax1.contourf(X, Y, Z1, cmap=num_techs_cmap, levels=[0,1,2,3], vmin=1, vmax=3)

#cbar1 = plt.colorbar(cpf1, ax=ax1, pad=0.1)
#cbar1.ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.0f'))
#cbar1.ax.set_ylabel(cbar_ylabel1, labelpad=10)

####################################################################
# Figure 2b: What is the effective number of storage technologies? #
####################################################################

ax2 = plt.subplot2grid((1, 2), (0, 1), colspan=1, rowspan=1)
cbar_ylabel2 = '% System Cost Reductions'

Z2 = np.abs(np.around(((data['system_cost'] - one_tech_data['system_cost'][0]) / one_tech_data['system_cost'][0])*100, 10))

# log colorbar
# levels2 = [0.001, 0.1, 0.5, 2.5, 10, 60]
# cpf2 = ax2.contourf(X, Y, Z2, cmap=cost_reduction_cmap, levels=levels2, locator=ticker.LogLocator(), vmin=0.1, vmax=30)

# linear colorbar
levels2 = [0.01, 10, 20, 30, 40, 50, 60]
cpf2 = ax2.contourf(X, Y, Z2, cmap=cost_reduction_cmap, levels=levels2)

cbar2 = plt.colorbar(cpf2, ax=ax2, pad=0.1)
cbar2.ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.1f'))
cbar2.ax.set_ylabel(cbar_ylabel2, labelpad=10)

# Show where 3 techs compete
'''
dotsize=1.5
dotcolor = 'gray'
dots_indices = [i for i,j in enumerate(data['both_exist_scatter_energy']) if ((j>=20) or (round(j,2)==0.01))]
dots_x = [data['both_exist_scatter_energy'][i] for i in tuple(dots_indices)]
dots_y = [data['both_exist_scatter_power'][i] for i in tuple(dots_indices)]
ax2.scatter(dots_x, dots_y, c=gray, s=dotsize)
'''    

# Axis labels, settings
axes = [ax1, ax2]
for ax in axes: 
    current_PGP_current_li_ion(ax)
    ax.set_xlim(0, 400)
    ax.set_ylim(0, 2000)
    ax.set_xlabel('Storage X Energy Cost ($/kWh)', labelpad=10)
    ax.set_ylabel('Storage X Power Cost ($/kW)', labelpad=10)
    ax.set_box_aspect(1)

# Adjust distance between subplots

plt.tight_layout()
plt.subplots_adjust(wspace=0.2, hspace=0.45)

ax1.text(-0.55, 1.25, 'A', transform=ax1.transAxes, fontsize=10, fontweight='bold', name='Arial')
ax1.text(-0.55, 1.5, 'Region: MISO', transform=ax1.transAxes, fontsize=12, fontweight='bold', name='Arial')
ax2.text(-0.55, 1.25, 'B', transform=ax2.transAxes, fontsize=10, fontweight='bold', name='Arial')



if not os.path.exists('Figures'):
    os.makedirs('Figures')
plt.savefig('C:/Users/covel/OneDrive/Desktop/Rerun-for-Anna/Dom Plotting Code/Plots/Fig 5/Fig_5_MISO.png', bbox_inches='tight', dpi=900)
plt.show()