# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 16:25:06 2021

@author: Kathleen
"""
##========================================
# Figure 4: Cost Sensitivity Contour Plots
##========================================

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

##====================================================
# Gather all files from MEM output into a folder for plotting
##====================================================
'''
file_path = 'C:/Users/Kathleen/Documents/GradSchool/Research/EnergyModeling/MEM-master/Output_Data/PV_Batt_Sweep'
target = r'C:/Users/Kathleen/Desktop/Temp/PV_Batt_Sweep'

for root, dirs, files in os.walk(file_path):
    for file in files:
        if file.endswith(".pickle"):
            shutil.copy(os.path.join(root,file),target)
'''

##===================================================
# Read in the data to plot (CSP+TES) and (PV+Batt)
##===================================================

sys_costs = []
cases = os.listdir('C:/Users/Kathleen/Desktop/Temp/ComboSweep')
cases.sort()

for case in cases:
    pickle_in = open('C:/Users/Kathleen/Desktop/Temp/ComboSweep/' + case, 'rb')
    base = pickle.load(pickle_in)
    results_case = base[1][0]
    sys_costs.append(results_case['system_cost'])

##===================================================
# Make Contour Plot
##===================================================

params = {'legend.fontsize': 'large',
          'figure.figsize': (16.5, 4.2),
         'axes.labelsize': 'x-large',
         'axes.titlesize': 'large',
         'xtick.labelsize':'large',
         'ytick.labelsize':'large',
         'legend.fontsize': 'x-large'}
pylab.rcParams.update(params)

fig = plt.figure()
ax = plt.subplot2grid((1,3), (0, 0), colspan=1, rowspan=1)

mesh_sz = 13
x = np.linspace(0,1.5,mesh_sz)
X, Y = np.meshgrid(x, x)
Z = np.reshape(sys_costs,(mesh_sz,mesh_sz)) 
levels = [0,0.02,0.025,0.03,0.035,0.04,0.045,0.05,0.055,0.06,0.065,0.07,0.075,0.08,0.085,
          0.09,0.095,0.1,0.105,0.11,0.115]
ticks = [0,0.02,0.04,0.06,0.08,0.1,0.12]
CS = plt.contourf(X, Y, Z, levels = levels)
CS2 = plt.contour(CS, levels=[0.05,0.07,0.09,0.1], colors='black')
fmt = ticker.FormatStrFormatter('$%.2f')
q = plt.clabel(CS2, inline=1, fontsize=10, fmt=fmt)

ax = plt.gca()
#ax.set_yticks([0,0.25,0.5,0.75,1.0,1.25,1.5])
ax.xaxis.set_major_formatter(FormatStrFormatter('%gx'))
ax.yaxis.set_major_formatter(FormatStrFormatter('%gx')) 
ax.set_ylim(0.0, 1.5)
ax.set_xlim(0.0, 1.5)

#plt.title('System cost sensitivity to\n(CSP+TES) and (PV+Battery) costs')
plt.xlabel('PV + Battery Cost\n(multiple of base case)')
plt.ylabel('CSP + TES Cost\n(multiple of base case)')

# Make a colorbar for the ContourSet returned by the contourf call
cbar = plt.colorbar(CS, shrink=0.9,extend='both',format='%.2f',ticks=ticks,
                    spacing='proportional')
cbar.ax.set_ylabel('System cost ($/kWh)')
##===================================================
# Read in the data to plot (CSP and TES)
##===================================================

sys_costs = []
cases = os.listdir('C:/Users/Kathleen/Desktop/Temp/CSP_TES_Sweep')
cases.sort()

for case in cases:
    pickle_in = open('C:/Users/Kathleen/Desktop/Temp/CSP_TES_Sweep/' + case, 'rb')
    base = pickle.load(pickle_in)
    results_case = base[1][0]
    sys_costs.append(results_case['system_cost'])

##===================================================
# Make Contour Plot
##===================================================

ax = plt.subplot2grid((1,3), (0, 1), colspan=1, rowspan=1)

mesh_sz = 13
x = np.linspace(0,1.5,mesh_sz) # multiplier from param_sweep
X, Y = np.meshgrid(x, x)
Z = np.reshape(sys_costs,(mesh_sz,mesh_sz)) 
levels = [0,0.02,0.025,0.03,0.035,0.04,0.045,0.05,0.055,0.06,0.065,0.07,0.075,0.08,0.085,
          0.09,0.095,0.1,0.105,0.11,0.115]
ticks = [0,0.02,0.04,0.06,0.08,0.1,0.12]
CS = plt.contourf(X, Y, Z, levels = levels)
CS2 = plt.contour(CS, levels=[0.05,0.07,0.09,0.1], colors='black')
fmt = ticker.FormatStrFormatter('$%.2f')
q = plt.clabel(CS2, inline=1, fontsize=10, fmt=fmt)

a = np.array([0.355,1])
b = np.array([1.326,1])
ax = plt.gca()
ax.scatter(a,b, c='black')
ax.text(0.24,1.37,'SPT',c='black',size='large')
ax.text(0.91,1.05,'PTC',c='black',size='large')
ax.xaxis.set_major_formatter(FormatStrFormatter('%gx'))
ax.yaxis.set_major_formatter(FormatStrFormatter('%gx')) 
ax.set_ylim(0.0, 1.5)
ax.set_xlim(0.0, 1.5)
#plt.title('System cost sensitivity\nto CSP and TES costs')
plt.xlabel('TES Cost\n(multiple of base case)')
plt.ylabel('CSP Cost\n(multiple of base case)')

# Make a colorbar for the ContourSet returned by the contourf call.
cbar = plt.colorbar(CS, shrink=0.9,extend='both',format='%.2f',ticks=ticks,spacing='proportional')
cbar.ax.set_ylabel('System cost ($/kWh)')

##===================================================
# Read in the data to plot (PV and batteries)
##===================================================

sys_costs = []
cases = os.listdir('C:/Users/Kathleen/Desktop/Temp/PV_Batt_Sweep')
cases.sort()

for case in cases:
    pickle_in = open('C:/Users/Kathleen/Desktop/Temp/PV_Batt_Sweep/' + case, 'rb')
    base = pickle.load(pickle_in)
    results_case = base[1][0]
    sys_costs.append(results_case['system_cost'])

##===================================================
# Make Contour Plot
##===================================================

ax = plt.subplot2grid((1,3), (0, 2), colspan=1, rowspan=1)

mesh_sz = 13
x = np.linspace(0,1.5,mesh_sz) # multiplier from param_sweep
X, Y = np.meshgrid(x, x)
Z = np.reshape(sys_costs,(mesh_sz,mesh_sz)) 
levels = [0,0.02,0.025,0.03,0.035,0.04,0.045,0.05,0.055,0.06,0.065,0.07,0.075,0.08,0.085,
          0.09,0.095,0.1,0.105,0.11,0.115]
ticks = [0,0.02,0.04,0.06,0.08,0.1,0.12]
CS = plt.contourf(X, Y, Z, levels = levels)
CS2 = plt.contour(CS, levels=[0.05,0.07,0.09,0.1], colors='black')
fmt = ticker.FormatStrFormatter('$%.2f')
q = plt.clabel(CS2, inline=1, fontsize=10, fmt=fmt)

a = np.array([0.355,1])
b = np.array([1.326,1])
ax = plt.gca()
ax.xaxis.set_major_formatter(FormatStrFormatter('%gx'))
ax.yaxis.set_major_formatter(FormatStrFormatter('%gx')) 
ax.set_ylim(0.0, 1.5)
ax.set_xlim(0.0, 1.5)
#plt.title('System cost sensitivity\nto PV and Battery costs')
plt.xlabel('Battery Cost\n(multiple of base case)')
plt.ylabel('PV Cost\n(multiple of base case)')

# Make a colorbar for the ContourSet returned by the contourf call.
cbar = plt.colorbar(CS, shrink=0.9,extend='both',format='%.2f',ticks=ticks,spacing='proportional')
cbar.ax.set_ylabel('System cost ($/kWh)')

fig.text(0.02,.95,'a)',size='x-large')
fig.text(0.35,.95,'b)',size='x-large')
fig.text(0.68,.95,'c)',size='x-large')

plt.tight_layout(True)
plt.savefig('PaperFigures/figure_6_contours.jpg', dpi=300, bbox_inches='tight')
plt.show()