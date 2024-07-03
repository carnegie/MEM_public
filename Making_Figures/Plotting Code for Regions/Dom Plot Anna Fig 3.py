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
import matplotlib.patches as mpatches
import string
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

# Custom Colors
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

from extract_data_sep_power import get_data_sep_power
from extract_data_one_power import get_data_one_power
from extract_data_non_sep_power import get_data_non_sep_power

def cost_conts(ax, path, x_labels, colors):
    dic = {}
    solar_cost = np.empty(len(x_labels))
    wind_cost = np.empty(len(x_labels))
    batt_cost = np.empty(len(x_labels))
    storage_x_cost = np.empty(len(x_labels))
    pgp_cost = np.empty(len(x_labels))
    
    for i, x_label in enumerate(x_labels):
        if x_label == '':
            solar_cost[i] = 0
            wind_cost[i] = 0
            pgp_cost[i] = 0
            storage_x_cost[i] = 0
            batt_cost[i] = 0
            continue
        elif x_label == 'Metal-Air':
            dic[x_label] = get_data_non_sep_power(path + '/' + x_label, 2, 'fixed_cost', 3, 'fixed_cost', False)
        elif x_label == 'CAES':
            dic[x_label] = get_data_sep_power(path + '/' + x_label, 2, 'fixed_cost', 3, 'fixed_cost', False)
        else:
            dic[x_label] = get_data_one_power(path + '/' + x_label, 2, 'fixed_cost', 3, 'fixed_cost', False)
        
        solar_cost[i] = dic[x_label]['solar_cost'][0]
        wind_cost[i] = dic[x_label]['wind_cost'][0]
        pgp_cost[i] = dic[x_label]['pgp_cost'][0]
        storage_x_cost[i] = dic[x_label]['third_tech_cost'][0]
        batt_cost[i] = dic[x_label]['batt_cost'][0]
    
    w=0.8
    ax.bar(x_labels, solar_cost, label='Solar', color=yellow, width=w)
    ax.bar(x_labels, wind_cost, bottom=solar_cost, label='Wind', color='cornflowerblue', width=w)
    ax.bar(x_labels, pgp_cost, bottom=solar_cost+wind_cost, label='PGP', color=pink, width=w)
    ax.bar(x_labels, storage_x_cost, bottom=solar_cost+wind_cost+pgp_cost, label='Storage X', color=colors, width=w)
    ax.bar(x_labels, batt_cost, bottom=solar_cost+wind_cost+pgp_cost+storage_x_cost, label='Li-ion', color=purple, width=w)
    
    plt.xticks(rotation=90)   

Li_ion_PGP_X_directory = 'C:/Users/covel/OneDrive/Desktop/Rerun-for-Anna/Output_Data/CISO/three_storage'
PGP_X_directory = 'C:/Users/covel/OneDrive/Desktop/Rerun-for-Anna/Output_Data/CISO/two_storage_pgp'
Li_ion_X_directory = 'C:/Users/covel/OneDrive/Desktop/Rerun-for-Anna/Output_Data/CISO/two_storage_lion'

# Set up techs
{'Li-ion': 326.4, 'RFB': 199.92, 'PSH': 105.162, 'Gravitational': 110.0315246, 'Thermal': 37.842, 'CAES': 51.102, 'Metal-Air': 2.448, 'PGP': 1.9992}

storage_names = ['Li-ion', 'RFB', 'PSH', 'Gravitational', 'Thermal', 'CAES', 'Metal-Air', 'Hydrogen']
storage_colors= [purple, green, darkblue, red, orange, lightblue, gray, pink] #For the cases with 1 tech

Li_ion_PGP_X_techs = ['RFB', 'PSH', 'Gravitational', 'Thermal', 'CAES', 'Metal-Air'] #Name of folders containing pickle for each technology in case
PGP_X_techs = ['RFB', 'PSH', 'Gravitational', 'Thermal', 'CAES', 'Metal-Air'] #Name of folders containing pickle for each technology in case
Li_ion_X_techs = ['RFB', 'PSH', 'Gravitational', 'Thermal', 'CAES', 'Metal-Air', 'PGP'] #Name of folders containing pickle for each technology in case

storage_x_colors = [green, darkblue, red, orange, lightblue, gray, pink] #For all cases with >1 tech

# Just Storage X

X_directory = 'C:/Users/covel/OneDrive/Desktop/Rerun-for-Anna/Output_Data/CISO/one_storage'

X_techs = ['Li-ion', 'RFB', 'PSH', 'Gravitational', 'Thermal', 'CAES', 'Metal-Air', 'PGP'] #For the cases with 1 tech

# Plot Figure

mm = 1/25.4 # millimeters in inches
fig_w = 172*mm
fig_h = 112*mm
fig = plt.subplots(nrows=1,ncols=2, figsize=(fig_w,fig_h), dpi=300)

########################################################################################
#                X : Cost Contributions of Different Storage X Techs           #
########################################################################################

ax1 = plt.subplot2grid((1, 27), (0, 0), colspan=8, rowspan=1)

ax1.set_title('One Storage Technology')
ax1.set_ylabel('System Cost Contributions ($/kWh)')
ax1.set_xticklabels(['Li-ion', 'RFB', 'PSH', 'Gravity', 'Thermal', 'CAES', 'Metal-Air', 'PGP'])
cost_conts(ax1, X_directory, X_techs, storage_colors)

###############################################################################
#        Li-ion + X : Cost Contributions of Different Storage X Techs         #
###############################################################################

ax2 = plt.subplot2grid((1, 27), (0, 8), colspan=7, rowspan=1)

ax2.set_title('Two Storage\nTechnologies\n(Li-ion + X)')
ax2.set_xticklabels(['Li-ion + RFB', '+ PSH', '+ Gravity', '+ Thermal', '+ CAES', '+ Metal-Air', '+ Hydrogen'])
cost_conts(ax2, Li_ion_X_directory, Li_ion_X_techs, storage_x_colors)

####################################################################################
#               PGP + X: Cost Contributions of Different Storage X Techs           #
####################################################################################

ax3 = plt.subplot2grid((1, 27), (0, 15), colspan=6, rowspan=1, )

ax3.set_title('Two Storage\nTechnologies\n(Hydrogen + X)')
ax3.set_xticklabels(['Hydrogen + RFB', '+ PSH', '+ Gravity', '+ Thermal', '+ CAES', '+ Metal-Air'])
cost_conts(ax3, PGP_X_directory, PGP_X_techs, storage_x_colors)
  
####################################################################################
#      Li-ion + PGP + X: Cost Contributions of Different Storage X Techs           #
####################################################################################

ax4 = plt.subplot2grid((1, 27), (0, 21), colspan=6, rowspan=1)

ax4.set_title('Three Storage\nTechnologies\n(Li-ion + Hydrogen + X)')
ax4.set_xticklabels(['Li-ion + H$_2$ + RFB', '+ PSH', '+ Gravity', '+ Thermal', '+ CAES', '+ Metal-Air'])
cost_conts(ax4, Li_ion_PGP_X_directory, Li_ion_PGP_X_techs,  storage_x_colors)
  
#####################################################################

# Set x and y lims

ymax = 0.3
ax1.set_ylim(0, ymax)
ax2.set_ylim(0, ymax)
ax3.set_ylim(0, ymax)
ax4.set_ylim(0, ymax)

#####################################################################

#ax1.set_box_aspect(1)
#ax2.set_box_aspect(1)
#ax3.set_box_aspect(1)

ax2.set_yticks([])
ax3.set_yticks([])
ax4.set_yticks([])

plt.tight_layout()
plt.subplots_adjust(wspace=1.5, hspace=0.25)

ax1.text(-0.15, 1.15, 'A', transform=ax1.transAxes, fontsize=10, fontweight='bold')
ax2.text(-0.15, 1.15, 'B', transform=ax2.transAxes, fontsize=10, fontweight='bold')
ax3.text(-0.15, 1.15, 'C', transform=ax3.transAxes, fontsize=10, fontweight='bold')
ax4.text(-0.15, 1.15, 'D', transform=ax4.transAxes, fontsize=10, fontweight='bold')

#plt.savefig('C:/Users/covel/OneDrive/Desktop/Rerun-for-Anna/Dom Plotting Code/Plots/Fig_3_sys_costs_CISO.png', bbox_inches='tight')
plt.show()