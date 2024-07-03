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
import pickle
from numpy import genfromtxt
from scipy.interpolate import griddata
import matplotlib.pyplot as plt
plt.style.use('default')
import matplotlib.gridspec as gridspec
import matplotlib.ticker as ticker
import matplotlib.colors as colors

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

date1 = datetime.datetime(2018, 1, 1, 0)
date2 = datetime.datetime(2019, 1, 1, 0)
delta = datetime.timedelta(hours=1)
dates = drange(date1, date2, delta)

# Font / Figure Size
import matplotlib.pylab as pylab
params = {'legend.fontsize': '7',
         'axes.labelsize': '7',
         'axes.titlesize': '7',
         'xtick.labelsize': '7',
         'ytick.labelsize': '7',
          

         'xtick.major.pad': '7',
         'ytick.major.pad': '7',
         'axes.titlepad': 10,
         'axes.labelpad': 15,
         
         'font.sans-serif':'Avenir',
         
         'axes.linewidth': 0.5,
         'xtick.major.width': 0.5,
         'ytick.major.width': 0.5}
pylab.rcParams.update(params)

#storage_x_name = 'Thermal'
#storage_x_color = orange

storage_x_name = 'Gravitational'
storage_x_color = red

#storage_x_name = 'PSH'
#storage_x_color = darkblue

#storage_x_name = 'RFB'
#storage_x_color = green

#storage_x_name = 'CAES'
#storage_x_color = lightblue

#storage_x_name = 'Metal-Air'
#storage_x_color = gray

def get_series(path, time_series):
    pickle_in = open(glob.glob(path + '/*.pickle')[0], 'rb')
    base = pickle.load(pickle_in)
    info = base[0]
    inputs = base[0][1]
    results = base[1]
    return results[2][time_series]

main_path = 'C:/Users/covel/OneDrive/Desktop/Rerun-for-Anna/Output_Data/For Figs 3 and 4/CISO/'

##########################################################################
#               For PSH, RFB, Gravity, Thermal, CAES                     #
##########################################################################


############### Storage X ###############
path_1 = main_path + 'one_storage/' + storage_x_name
storage_x_energy_1 = get_series(path_1, 'third_tech_energy stored')

############### Li-ion + Storage X ###############
path_2 = main_path + 'two_storage_lion/' + storage_x_name

li_ion_energy_2 = get_series(path_2, 'battery stored')
storage_x_energy_2 = get_series(path_2, 'third_tech_energy stored')

############### PGP + Storage X ###############
path_3 = main_path + 'two_storage_pgp/' + storage_x_name

pgp_energy_3 = get_series(path_3, 'PGP_storage stored')
storage_x_energy_3 = get_series(path_3, 'third_tech_energy stored')

############### Li-ion + PGP + Storage X ###############
path_4 = main_path + 'three_storage/' + storage_x_name

pgp_energy_4 = get_series(path_4, 'PGP_storage stored')
li_ion_energy_4 = get_series(path_4, 'battery stored')
storage_x_energy_4 = get_series(path_4, 'third_tech_energy stored')
'''
##########################################################################
#                 For Metal-Air Only                                     #
##########################################################################

############### Storage X ###############
path_1 = main_path + 'one_storage/' + storage_x_name
storage_x_energy_1 = get_series(path_1, 'third_tech stored')

############### Li-ion + Storage X ###############
path_2 = main_path + 'two_storage_lion/' + storage_x_name

li_ion_energy_2 = get_series(path_2, 'battery stored')
storage_x_energy_2 = get_series(path_2, 'third_tech stored')

############### PGP + Storage X ###############
path_3 = main_path + 'two_storage_pgp/' + storage_x_name

pgp_energy_3 = get_series(path_3, 'PGP_storage stored')
storage_x_energy_3 = get_series(path_3, 'third_tech stored')

############### Li-ion + PGP + Storage X ###############
path_4 = main_path + 'three_storage/' + storage_x_name

pgp_energy_4 = get_series(path_4, 'PGP_storage stored')
li_ion_energy_4 = get_series(path_4, 'battery stored')
storage_x_energy_4 = get_series(path_4, 'third_tech stored')
'''




# Get numbers for optimized duration and annual cycles per year


##########################################################################
#                   For PSH, RFB, Gravity, Thermal                       #
##########################################################################
from extract_data_one_power import get_data_one_power
data_1 = get_data_one_power(path_1, 2, 'fixed_cost', 3, 'fixed_cost', False)
data_2 = get_data_one_power(path_2, 2, 'fixed_cost', 3, 'fixed_cost', False)
data_3 = get_data_one_power(path_3, 2, 'fixed_cost', 3, 'fixed_cost', False)
data_4 = get_data_one_power(path_4, 2, 'fixed_cost', 3, 'fixed_cost', False)

'''
##########################################################################
#                        For Metal-Air Only                              #
##########################################################################
from extract_data_non_sep_power import get_data_non_sep_power
data_1 = get_data_non_sep_power(path_1, 2, 'fixed_cost', 3, 'fixed_cost', False)
data_2 = get_data_non_sep_power(path_2, 2, 'fixed_cost', 3, 'fixed_cost', False)
data_3 = get_data_non_sep_power(path_3, 2, 'fixed_cost', 3, 'fixed_cost', False)
data_4 = get_data_non_sep_power(path_4, 2, 'fixed_cost', 3, 'fixed_cost', False)

##########################################################################
#                             For CAES Only                              #
##########################################################################
from extract_data_sep_power import get_data_sep_power
data_1 = get_data_sep_power(path_1, 2, 'fixed_cost', 3, 'fixed_cost', False)
data_2 = get_data_sep_power(path_2, 2, 'fixed_cost', 3, 'fixed_cost', False)
data_3 = get_data_sep_power(path_3, 2, 'fixed_cost', 3, 'fixed_cost', False)
data_4 = get_data_sep_power(path_4, 2, 'fixed_cost', 3, 'fixed_cost', False)
'''

data_list= [data_1, data_2, data_3, data_4]

def annotate(ax, dur, cyc):
  ax.text(0.5, 0.85, dur, transform=ax.transAxes, ha='center', fontsize=7)
  ax.text(0.5, 0.7, cyc, transform=ax.transAxes, ha='center', fontsize=7)

mm = 1/25.4 # millimeters in inches
fig_w = 172*mm
fig_h = 112*mm
fig, ax = plt.subplots(ncols=4, nrows=3, figsize=(fig_w, fig_h), dpi=300)

w = 0.2
pgp_max = 1200
pgp_days_max = pgp_max/24
storage_x_max = 100
li_ion_max = 4

def plot_energy(ax, energy, energy_max, color):
    ax.fill_between(dates, energy, color=color, linewidth=w)
    ax.set_xlim(dates[0], dates[-1])
    ax.set_ylim(0, energy_max)
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.xaxis.set_tick_params(direction='out', which='both', length=0)
    ax.yaxis.set_tick_params(direction='out', which='both')
    
def bottom_params(ax):
    ax.tick_params(axis='x', which='both', length=2.5)
    months = ['Jan', 'Apr', 'Jul', 'Oct', 'Jan']
    plt.xticks(np.linspace(dates[0], dates[-1], 5), months)
    
def left_params(ax):
    ax.set_yticklabels(ax.get_yticks())
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.0f'))

    
fake_energy = np.array([0]*len(storage_x_energy_1))    

#########################################################################################################
#                                             CASE 1                                                   #
#########################################################################################################
    
# Li-ion energy in storage
plot_energy(ax[0,0], fake_energy, li_ion_max, purple)
left_params(ax[0,0])

# Storage X energy in storage
plot_energy(ax[1,0], storage_x_energy_1, storage_x_max, storage_x_color)
left_params(ax[1,0])

# PGP energy in storage
plot_energy(ax[2,0], fake_energy, pgp_max, pink)

ax_days_1 = ax[2,0].twinx()
pgp_energy_days_1 = fake_energy/24
plot_energy(ax_days_1, pgp_energy_days_1, pgp_days_max, pink)

left_params(ax[2,0])
bottom_params(ax[1,0])

#########################################################################################################
#                                             CASE 2                                                    #
#########################################################################################################

# Li-ion energy in storage
plot_energy(ax[0,1], li_ion_energy_2, li_ion_max, purple)
left_params(ax[0,1])

# Storage X energy in storage
plot_energy(ax[1,1], storage_x_energy_2, storage_x_max, storage_x_color)

# PGP energy in storage
plot_energy(ax[2,1], fake_energy, pgp_max, pink)

ax_days_2 = ax[2,1].twinx()
pgp_energy_days_2 = fake_energy/24
plot_energy(ax_days_2, pgp_energy_days_2, pgp_days_max, pink)

bottom_params(ax[1,1])

#########################################################################################################
#                                             CASE 3                                                    #
#########################################################################################################

# Li-ion energy in storage
plot_energy(ax[0,2], fake_energy, li_ion_max, purple)

# Storage X energy in storage
plot_energy(ax[1,2], storage_x_energy_3, storage_x_max, storage_x_color)

# PGP energy in storage
plot_energy(ax[2,2], pgp_energy_3, pgp_max, pink)
left_params(ax[2,2])

ax_days_3 = ax[2,2].twinx()
pgp_energy_days_3 = pgp_energy_3/24
plot_energy(ax_days_3, pgp_energy_days_3, pgp_days_max, pink)

bottom_params(ax[2,2])

#########################################################################################################
#                                             CASE 4                                                    #
#########################################################################################################

# Li-ion energy in storage
plot_energy(ax[0,3], li_ion_energy_4, li_ion_max, purple)
left_params(ax[0,3])

# Storage X energy in storage
plot_energy(ax[1,3], storage_x_energy_4, storage_x_max, storage_x_color)

# PGP energy in storage
plot_energy(ax[2,3], pgp_energy_4, pgp_max, pink)

ax_days_4 = ax[2,3].twinx()
pgp_energy_days_4 = pgp_energy_4/24
plot_energy(ax_days_4, pgp_energy_days_4, pgp_days_max, pink)
left_params(ax_days_4)
ax_days_4.set_ylabel('(Days of mean\n CAISO demand)', size=8)

bottom_params(ax[2,3])

#=================================================================================================
# Label the optimized durations and annual cycles per year for each storage technology

data_list = [data_1, data_2, data_3, data_4]

# Label 1st row (Li-ion batteries)
for i,e in enumerate([1, 3]):
  data = data_list[e]
  cyc = round(data['batt_cycles'][0])
  annotate(ax[0,e], '4 hour discharge', str(cyc) + ' cycles/year')

# Label 2nd row (Storage X)
for i,e in enumerate([0, 1, 2, 3]):
  data = data_list[e]
  cyc = round(data['third_tech_cycles'][0])
  dur = round(data['third_tech_dur'][0])
  
  if dur == 0 or cyc == 0:
    continue

  annotate(ax[1,e], str(dur) + ' hour discharge', str(cyc) + ' cycles/year')
  #annotate(ax[1,e], str(100) + ' hour discharge', str(cyc) + ' cycles/year') #use for metal-air only

# Label 3rd row (Hydrogen Energy Storage)
for i,e in enumerate([2, 3]):
  data = data_list[e]
  dur = round(data['PGP_dur'][0])
  cyc = round(data['PGP_cycles'][0], 1)
  annotate(ax[2,e], str(dur) + ' hour discharge', str(cyc) + ' cycles/year')
  
#=================================================================================================
# Label the storage technologies

plt.tight_layout()

fig.text(-0.02, 0.5, 'Energy in storage (hours of mean CAISO demand)', va='center', ha='center', 
         rotation='vertical', size=10)

fig.text(-0.15, 0.85, 'Li-ion', va='center', ha='center', rotation='horizontal', size=12)

fig.text(-0.15, 0.53, '$\it{' + storage_x_name + '}$', va='center', ha='center', rotation='horizontal', size=12)

fig.text(-0.15, 0.23, 'Hydrogen', va='center', ha='center', rotation='horizontal', size=12)

#=================================================================================================
# Label the panesl A, B, C, D

ax[0,0].text(-0.15, 1.25, 'A', transform=ax[0,0].transAxes, fontsize=10, fontweight='bold')
ax[0,1].text(-0.15, 1.25, 'B', transform=ax[0,1].transAxes, fontsize=10, fontweight='bold')
ax[0,2].text(-0.15, 1.25, 'C', transform=ax[0,2].transAxes, fontsize=10, fontweight='bold')
ax[0,3].text(-0.15, 1.25, 'D', transform=ax[0,3].transAxes, fontsize=10, fontweight='bold')

ax[0,0].set_title('$\it{' + storage_x_name + '}$', pad=8, linespacing=2, fontsize=8)
ax[0,1].set_title('Li-ion + $\it{' + storage_x_name + '}$', pad=8, linespacing=2, fontsize=8)
ax[0,2].set_title(r'H$_{\rm 2}$' + ' + $\it{' + storage_x_name + '}$', pad=8, linespacing=2, fontsize=8)
ax[0,3].set_title('Li-ion + ' + r'H$_{\rm 2}$' + ' + $\it{' + storage_x_name + '}$', pad=8, linespacing=2, fontsize=8)

plt.subplots_adjust(wspace=0.25, hspace=0.25)

#=================================================================================================
# Turn off axis that don't have plots

ax[0,0].axis('off')
ax[2,0].axis('off')
ax[2,1].axis('off')
ax[0,2].axis('off')
ax_days_1.axis('off')
ax_days_2.axis('off')


if not os.path.exists('Figures'):
    os.makedirs('Figures')
plt.savefig('C:/Users/covel/OneDrive/Desktop/Rerun-for-Anna/Dom Plotting Code/Plots/Fig 4/Plots before GIMP Processing/CAISO/Fig_4_energy_storage_CAISO_Gravity.png', bbox_inches='tight', dpi=900)
plt.show()