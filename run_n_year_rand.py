"""
# Based off of Lei Duan's Run_Case_Example_loop.py file
"""

from Preprocess_Input import preprocess_input
from Run_Core_Model import run_model_main_fun
from FindRegion import update_series, update_timenum, return_file_info_map, stitch_together_select_years, select_random_years, nYears_year_combinations
import sys, numpy as np
import calendar
import random

print("To run this file you must have created the new timeseries files with different delta_t. Go to the directory: Input_Data/n_years2/")

print("Given arguments")
print(sys.argv)

### Read input data
if len(sys.argv) < 6:
    print ('give parameter ;;code input region start_year n_years techs date/tag;;') 
    print(len(sys.argv))
    sys.exit()
else:
    case_input_path_filename = sys.argv[1]
    region = str(sys.argv[2])
    n_years = int(sys.argv[3])
    techs = str(sys.argv[4])
    date = str(sys.argv[5])

if len(sys.argv) > 6:
    tmp = str(sys.argv[6])
    tmp = tmp.split('_')
    scale_factors = [float(val) for val in tmp]
    print(f"Scale factors: {scale_factors}")
else:
    scale_factors = [1.0, ]

if len(sys.argv) > 7:
    deltaT = int(sys.argv[7])
else:
    deltaT = 1

if len(sys.argv) > 8:
    iters = int(sys.argv[8])
else:
    iters = 50

if len(sys.argv) > 9:
    start_iter = int(sys.argv[9])
else:
    start_iter = 0

if len(sys.argv) > 10:
    NG_disp = float(sys.argv[10])
else:
    NG_disp = -1

if len(sys.argv) > 11:
    lost_load_disp = float(sys.argv[11])
else:
    lost_load_disp = 0 # 100% reliable




print(f"case_input_path_filename {case_input_path_filename}")
print(f"region {region}")
print(f"n_years {n_years}")
print(f"techs {techs}")
print(f"date {date}")
print(f"scale_factors {scale_factors}")
print(f"deltaT {deltaT}")
print(f"ITERS {iters}")
print(f"START_ITER {start_iter}")
print(f"NatGas Dispatch: {NG_disp}")
print(f"Lost load: {lost_load_disp}")


### Get selection of nYear combos
info = return_file_info_map(region)
#yr_vect = nYears_year_combinations(n_years, info['years'])
print(info['years'])
print(n_years)

### Pre-processing
print ('Macro_Energy_Model: Pre-processing input')
case_dic,tech_list = preprocess_input(case_input_path_filename)

### Find values
for idx in range(len(tech_list)):
    name = tech_list[idx]['tech_name']
    if name == 'demand': demand_idx = idx
    if name == 'solar': solar_idx = idx 
    if name == 'wind': wind_idx = idx

### Set basic information
case_dic['delta_t'] = deltaT
csv = '.csv' if deltaT <= 1 else f'_deltaT{deltaT}.csv'
tech_list[demand_idx]['series_file'] = info['demand'][0].replace('.csv', csv)
if 'S' in techs:
    tech_list[solar_idx]['series_file'] = info['solar'][0].replace('.csv', csv)
if 'W' in techs:
    tech_list[wind_idx]['series_file'] = info['wind'][0].replace('.csv', csv)

### Loop if non_consecutive else single go
case_dic['case_name'] += f'_{techs}'
case_name_default = case_dic['case_name']
#max_iters = len(yr_vect) if len(yr_vect) < iters else iters
max_iters = iters



for i in range(start_iter, start_iter + max_iters):

    # This will make each unique based on iteration number
    random.seed(i)

    # If choosing 71 years, run chronological full data set
    # or, the length of the dataset. 1979-2020 is 42 years.
    if n_years == len(info['years']):
        print("\nRunning all years chronologically\n")
        data_years = info['years']
    elif n_years == -1: # Run each year individually
        data_years = [min(info['years'])+i,]
        if data_years[-1] > max(info['years']):
            print("All done")
            exit()
    else: # any other number of n_years, this is the normal version
        data_years = []
        for j in range(n_years):
            yr = random.choice(info['years'])
            data_years.append(yr)

    print(f"Iter: {i}, data years: {data_years}")



    ### select years
    year_tag = f"{str(data_years[0])[-2:]}"
    for j in range(1, len(data_years)):
        year_tag += f"-{str(data_years[j])[-2:]}"
    case_dic['output_path'] = f'Output_Data/n_years_{date}_{techs}_{region}_dT{deltaT}/{region}_nYears{n_years}'
    case_dic['case_name'] = case_name_default + f'_iter{str(i).zfill(5)}'
    case_dic['case_notes'] = year_tag




    ### Update time series region and year of input data
    # Pick up time series w/o leap days
    tech_list[demand_idx]['series'] = stitch_together_select_years(data_years, "Input_Data/n_years2/"+tech_list[demand_idx]['series_file'])
    if 'S' in techs:
        tech_list[solar_idx]['series'] = stitch_together_select_years(data_years, "Input_Data/n_years2/"+tech_list[solar_idx]['series_file'])
    if 'W' in techs:
        tech_list[wind_idx]['series'] = stitch_together_select_years(data_years, "Input_Data/n_years2/"+tech_list[wind_idx]['series_file'])
    case_dic['num_time_periods'] = len(tech_list[demand_idx]['series'])
   


    ### Zero unused techs
    # Code is S = solar, W = wind, NG = NatGas, B = battery storage
    # 19 Nov 2021 - we are adding a PGP option, but with a tailored cfg file,
    #               so we do not need to zero it out in other cases
    for k, l in enumerate(tech_list):
        if 'solar' in l['tech_name'] and 'S' not in techs:
            l['capacity'] = 0
        if 'wind' in l['tech_name'] and 'W' not in techs:
            l['capacity'] = 0
        if 'natgas' in l['tech_name'] and 'NG' not in techs:
            l['capacity'] = 0
        if 'storage' in l['tech_name'] and 'B' not in techs:
            l['capacity'] = 0


    ### Other flexibility mechanisms
    for k, l in enumerate(tech_list):
        # Proxy for carbon constraint
        if 'natgas' in l['tech_name']:
            l['mean_dispatch'] = NG_disp
        # Lost load, -1 means free value, 0 = 100% reliable
        if 'lost_load' in l['tech_name']:
            l['mean_dispatch'] = lost_load_disp
            #l['max_capacity'] = 0.25 # TESTING
   
    ### Run
    results_case_dic, results_tech_dic, results_time_dic = run_model_main_fun(case_dic, tech_list) 
    
    
    
    
