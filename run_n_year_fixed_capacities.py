#
#
# Script to take aggregated results file with capacities from
# original MEM runs, and test those system capacities with
# other years of data. Essentially, this runs MEM as a dispatch-only
# model with lost load being the interesting output value.
#
#

import pandas as pd
from Preprocess_Input import preprocess_input
from Run_Core_Model import run_model_main_fun
from FindRegion import update_series, update_timenum, return_file_info_map, stitch_together_select_years, select_random_years, nYears_year_combinations
import sys, numpy as np
import calendar
import random

print("\nGiven arguments")
print(sys.argv)

### Read input data
if len(sys.argv) < 2:
    print ('run this code as\n"python run_n_year_fixed_capacities.py <case_input_path_filename> <results_file.csv>"') 
    sys.exit()
else:
    results_filename = sys.argv[1]
    test_n_years = int(sys.argv[2])
if len(sys.argv) > 3:
    NG_disp = float(sys.argv[3])
else:
    NG_disp = -1
tgt_idx = -1
if len(sys.argv) > 4:
    tgt_idx = int(sys.argv[4])
if len(sys.argv) > 5:
    test_on_all_years = bool(sys.argv[5])
else:
    test_on_all_years = False

case_input_path_filename = "case_input_reli_20210220.csv"
if "PGP" in results_filename:
    case_input_path_filename = "case_input_reli_20210220_w_PGP.csv"

### Parse results file for region, techs, date
info = results_filename.split('n_years_')[-1].replace('.csv','').split('_')
print(info)
date = info[0]
region = info[1]
techs = info[2]

# Don't store time series results to save space
include_timeseries_results = False
#include_timeseries_results = True

print(f"Date: {date}")
print(f"Region: {region}")
print(f"Techs: {techs}")
print(f"Test n_years {test_n_years}")
print(f"Default config file: {case_input_path_filename}")
print(f"NatGas Dispatch: {NG_disp}")
print(f"Test specific results file index: {tgt_idx}")
print(f"Test on all years: {test_on_all_years}")
print(f"Include timeseries in results: {include_timeseries_results}")



### Pre-processing
print ('Macro_Energy_Model: Pre-processing input')
case_dic,tech_list = preprocess_input(case_input_path_filename)
case_dic['case_name'] += f'_{techs}'
case_name_default = case_dic['case_name']
case_dic['include_timeseries_results'] = include_timeseries_results



### Find values
for idx in range(len(tech_list)):
    name = tech_list[idx]['tech_name']
    if name == 'demand': demand_idx = idx
    if name == 'solar': solar_idx = idx 
    if name == 'wind': wind_idx = idx



### Load region specific resource files
info = return_file_info_map(region)
print(f"Years in input data: {info['years']}")


### Set basic information
deltaT = 4
case_dic['delta_t'] = deltaT
csv = '.csv' if deltaT <= 1 else f'_deltaT{deltaT}.csv'
tech_list[demand_idx]['series_file'] = info['demand'][0].replace('.csv', csv)
if 'S' in techs:
    tech_list[solar_idx]['series_file'] = info['solar'][0].replace('.csv', csv)
if 'W' in techs:
    tech_list[wind_idx]['series_file'] = info['wind'][0].replace('.csv', csv)





### Zero unused techs
# Code is S = solar, W = wind, NG = NatGas, B = battery storage
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
        l['mean_dispatch'] = -1



### Open results file
print(f"Opening: {results_filename}")
df = pd.read_csv(results_filename)

# Select subset of csv file with appropriate n_years
print(f"Original length of df: {len(df.index)}")
df = df[ df['n_years'] == test_n_years ]
print(f"Length of df skimming for n_years=={test_n_years}: {len(df.index)}")

# Prep capacity column names
cols = df.columns
tech_cols = []
for col in cols:
    if ' capacity' in col:
        tech_cols.append(col.replace(' capacity', ''))
print(f"Setting capacities for: {tech_cols}")


### Iterate
for i, idx in enumerate(df.index):

    if tgt_idx > -1:
        if tgt_idx != i:
            continue
        print(f"Selected idx: {idx} based on tgt_idx: {tgt_idx} and ITER {i}")
    random.seed(42 + idx)

    orig_n_years = df.loc[idx, 'n_years']

    print(df.loc[idx, 'name'])


    ### Find years in original optimization
    year_tag = str(df.loc[idx, 'opt_years'])
    split_tag = year_tag.split('-')
    original_years = []
    for yr in split_tag:
        yr = int(yr)
        original_years.append(2000+yr) if yr < 25 else original_years.append(1900+yr)
    print(f"Year tag: {year_tag}, original years: {original_years}")

    #if i > 15:
    #    break

    ### Set capacities
    for l in tech_list:
        if l['tech_name'] in tech_cols:
            l['capacity'] = df.loc[idx, l['tech_name']+' capacity']
            print(f"Cap for tech: {l['tech_name']}, {l['capacity']}")



    ### Determine which years to test/
    out_of_sample_years = []
    for yr in info['years']:
        if yr not in original_years:
            out_of_sample_years.append(yr)
    print(f"Out of sample years: {out_of_sample_years}")

    to_test = []
    
    if test_on_all_years:
        to_test = out_of_sample_years
    else:
        # Take subset to increase processing speed, 4 iters per original simulation
        ITERS = 10
        while len(to_test) < ITERS:
            test_yr = random.choice(out_of_sample_years)
            #if test_yr not in to_test:
            # TR - 3 Nov 2022, this new choice treats the out-of-sample year selection
            # like the original optimization, years are selected with replacement from the
            # out-of-sample years. One could hypothetically select the same out-of-sample year
            # 10 times.
            to_test.append(test_yr)
        #to_test.sort() # Don't sort, keep years as they were randomly selected.
    print(f"Years to test: {to_test}")



    #### Iterate over out-of-sample years with n_years=1
    #for year in to_test:
    #    print(f"Testing year: {year}")


    #    ### Update time series region and year of input data
    #    data_years = [year,]
    #    tech_list[demand_idx]['series'] = stitch_together_select_years(data_years, "Input_Data/n_years2/"+tech_list[demand_idx]['series_file'])
    #    if 'S' in techs:
    #        tech_list[solar_idx]['series'] = stitch_together_select_years(data_years, "Input_Data/n_years2/"+tech_list[solar_idx]['series_file'])
    #    if 'W' in techs:
    #        tech_list[wind_idx]['series'] = stitch_together_select_years(data_years, "Input_Data/n_years2/"+tech_list[wind_idx]['series_file'])
    #    case_dic['num_time_periods'] = len(tech_list[demand_idx]['series'])



    #    ### Set casename and output dir
    #    case_dic['output_path'] = f'Output_Data/n_years_{date}_{techs}_{region}_TestArchs/{region}_nYears{orig_n_years}'
    #    case_dic['case_name'] = case_name_default + '_DYrs' + year_tag + '_Tested' + str(year)
    #    print(case_dic['output_path'])
    #    print(case_dic['case_name'])



    #    ### Run
    #    results_case_dic, results_tech_dic, results_time_dic = run_model_main_fun(case_dic, tech_list) 


    ### Single test over out-of-sample years with n_years=ITERS (10 currently)
    print(f"Testing years: {to_test}")


    ### Update time series region and year of input data
    data_years = to_test
    tech_list[demand_idx]['series'] = stitch_together_select_years(data_years, "Input_Data/n_years2/"+tech_list[demand_idx]['series_file'])
    if 'S' in techs:
        tech_list[solar_idx]['series'] = stitch_together_select_years(data_years, "Input_Data/n_years2/"+tech_list[solar_idx]['series_file'])
    if 'W' in techs:
        tech_list[wind_idx]['series'] = stitch_together_select_years(data_years, "Input_Data/n_years2/"+tech_list[wind_idx]['series_file'])
    case_dic['num_time_periods'] = len(tech_list[demand_idx]['series'])



    ### Set casename and output dir
    case_dic['output_path'] = f'Output_Data/n_years_{date}_{techs}_{region}_TestArchs/{region}_nYears{orig_n_years}'
    test_yr_str = '-'.join([str(yr) for yr in data_years])
    case_dic['case_name'] = case_name_default + '_DYrs' + year_tag + '_Iter'+ str(tgt_idx).zfill(4) +'_Tested' + test_yr_str
    print(case_dic['output_path'])
    print(case_dic['case_name'])



    ### Run
    results_case_dic, results_tech_dic, results_time_dic = run_model_main_fun(case_dic, tech_list) 
