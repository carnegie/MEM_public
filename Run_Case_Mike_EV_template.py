"""
# Code without looping;
# Use it the same way as before;
"""

from Preprocess_Input import preprocess_input
from Run_Core_Model import run_model_main_fun
from FindRegion import GetCFsName, update_series, update_timenum
import sys, numpy as np

if len(sys.argv) == 1:
    case_input_path_filename = './case_EV_template_main.csv'
else:
    case_input_path_filename = sys.argv[1]

### Pre-processing
print ('Macro_Energy_Model: Pre-processing input')
case_dic,tech_list = preprocess_input(case_input_path_filename)

if case_dic.get('co2_constraint',-1) >= 0:
    case_dic['co2_constraint'] = case_dic['co2_constraint']
else:
    case_dic['co2_constraint'] = -1

# Store base name for output scenario
case_name_default = case_dic['case_name']

# Make list of EV Loads to scan
# This could be done better to make thoughtful spacing and an upper range
ev_loads = [0.000000001, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19, 0.2, 0.21, 0.22, 0.23, 0.24, 0.25, 0.26, 0.27, 0.28, 0.29, 0.3, 0.31, 0.32, 0.33, 0.34, 0.35, 0.36, 0.37, 0.38, 0.39, 0.4, 0.41, 0.42, 0.43, 0.44, 0.45, 0.46, 0.47, 0.48, 0.49, 0.5, 0.51, 0.52, 0.53, 0.54, 0.55, 0.56, 0.57, 0.58, 0.59, 0.6, 0.61, 0.62, 0.63, 0.64, 0.65, 0.66, 0.67, 0.68, 0.69, 0.7, 0.71, 0.72, 0.73, 0.74, 0.75, 0.76, 0.77, 0.78, 0.79, 0.8, 0.81, 0.82, 0.83, 0.84, 0.85, 0.86, 0.87, 0.88, 0.89, 0.9, 0.91, 0.92, 0.93, 0.94, 0.95, 0.96, 0.97, 0.98, 0.99, 1]
#while ev_loads[-1] < 5:
    #ev_loads.append( ev_loads[-1] * 1.5 )
#ev_loads.append(0.) # Zero has to go last b/c of normalization occuring later in code
print(f"EV Demands to scan: {ev_loads}")

# Define the Storage / EV Load fraction
# Adjust this based on your findings.
# A storage_to_load_fraction = 0.1 means a 100 kWh Tesla drives on avg 10 kWh or 10% of their charge per day
# Is it safe to assume this value is ~ consistent across most light duty vehicles?
storage_to_load_fraction = 222.35

# Loop over all EV Loads and run model
for i, ev_load in enumerate(ev_loads):

    # Set the EV Load and Storage for each scenario
    for i, vect in enumerate(tech_list):
        if 'demand_ev1' in vect['tech_name']:
            vect['normalization'] = ev_load

            # Need to actually normalize now (original time series normalization
            # is done when the model is loaded with `preprocess_input`)
            series = vect['series']
            vect['series'] = series * vect['normalization']/np.average(series)

        if 'storage_ev1' in vect['tech_name']:
            vect['capacity'] = ev_load * storage_to_load_fraction

    # Update name for scenario
    case_dic['case_name'] = case_name_default + f"_evLoad{str(round(ev_load,4)).replace('.','p')}"

    run_model_main_fun(case_dic, tech_list) 



