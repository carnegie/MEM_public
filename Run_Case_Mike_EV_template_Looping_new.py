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
ev_loads = [0.0000000001, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
#while ev_loads[-1] < 5:
#    ev_loads.append( ev_loads[-1] * 1.5 )
#ev_loads.append(0.) # Zero has to go last b/c of normalization occuring later in code
print(f"EV Demands to scan: {ev_loads}")

# Define the Storage / EV Load fraction
# Adjust this based on your findings.
# A storage_to_load_fraction = 0.1 means a 100 kWh Tesla drives on avg 10 kWh or 10% of their charge per day
# Is it safe to assume this value is ~ consistent across most light duty vehicles?
storage_to_load_fraction = 222.35

# Loop over all EV Loads1 and run model
for ev_load1 in ev_loads:

    #for frac in [1e-6, .1, .2, .3, .4, .5, .6, .7, .8, .9, .999]: #... keep going
        #ev_load1 = ev_load * (1. - frac)
    for ev_load2 in ev_loads:
        #ev_load2 = ev_load * frac
        ev_load = ev_load1 + ev_load2
        frac = ev_load2 / ev_load

        print(f"Total EV Load = {ev_load}, EV Load1 = {ev_load1}, EV Load2 = {ev_load2}, Normal demand = 1, EV Load / Total load = {(ev_load + ev_load2)/(1 + ev_load + ev_load2)}")
        # Set the EV Load and Storage for each scenario
        for vect in tech_list:
            if 'demand_ev1' in vect['tech_name']:
                vect['normalization'] = ev_load1

                # Need to actually normalize now (original time series normalization
                # is done when the model is loaded with `preprocess_input`)
                series = vect['series']
                vect['series'] = series * vect['normalization']/np.average(series)

            if 'storage_ev1' in vect['tech_name']:
                vect['capacity'] = ev_load1 * storage_to_load_fraction


        # Set the EV Load and Storage for each scenario
        for vect in tech_list:
            if 'demand_ev2' in vect['tech_name']:
                vect['normalization'] = ev_load2

                # Need to actually normalize now (original time series normalization
                # is done when the model is loaded with `preprocess_input`)
                series = vect['series']
                vect['series'] = series * vect['normalization']/np.average(series)

            if 'storage_ev2' in vect['tech_name']:
                vect['capacity'] = ev_load2 * storage_to_load_fraction

        # Update name for scenario
        case_dic['case_name'] = case_name_default + f"_evLoad{str(round(ev_load,6)).replace('.','p')}_pctEVLoad2{str(round(frac,6)).replace('.','p')}"

        run_model_main_fun(case_dic, tech_list) 



