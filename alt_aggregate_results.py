#!/usr/bin/env python3

import numpy as np
import pandas as pd
from glob import glob
import pickle
from collections import OrderedDict
import os

if not os.path.exists('plotting-scripts'):
    os.mkdir('plotting-scripts')

### MAKE RESULTS FILE

nYrs_map = {
        1 : 500,
        2 : 500,
        3 : 500,
        4 : 500,
        5 : 500,
        7 : 500,
        10 : 500,
        15 : 150,
        25 : 150,
        40 : 20,
}

def make_results_file(date, techs, region, prefix, test=False, deltaT=''):
    
    status = []
    syst_cost = []
    name = []
    pct_decarb = []
    dates = []
    regions = []

    n_years = []
    opt_years = []
    test_years = []
    ITER = []
    end_test_years = []
    curtailed_gen = []
    lost_load = []
    max_lost_load = []
    sfs = []
    
    initial_years_name = 'OptYears'
    test_years_name = 'Tested'

    first = True
    cnt = 0

    app = ''
    if os.getenv('HOSTNAME') and 'maz' in os.getenv('HOSTNAME'):
        app = f'/scratch/{os.getenv("USER")}/MEM/' 
    print(app)
    post = f'dT{deltaT}' if not test else 'TestArchs'
    f_names = f'{app}Output_Data/n_years_{date}_{techs}_{region}_{post}/{region}_nYears*/{prefix}_*/*.pickle'

    print(f_names)
    files = glob(f_names)
    if len(files) == 0:
        print("Zero files found. Skipping.\n\n")
        return -1
    #print(files)
    my_results = {}
    for i, f in enumerate(files):

        
        # Check file naming for first file
        if i == 0:
            if 'DYrs' in f:
                initial_years_name = 'DYrs'
                test_years_name = 'RenewableYear'
        
        ### Try to open file before appending anything
        ### b/c we might need to skip this file
        try:
            infile = open(f,'rb')
            pi = pickle.load(infile)
            infile.close()
        except:
            print(f"Loading file {f} did not work, skipping this file.")
            continue
        
        dates.append(date)
        regions.append(region)
        
        #print(f)
        info = f.split('/')[-1]
        info = info.split('_')
        #print(info)
        mod = 0 if 'SF' in f else 1
        mod = 2
        if test:
            mod -= 1 
        n_years.append(int(f.split('/')[-3].split('_')[-1].replace('nYears','')))
        nYr = str(n_years[-1])
        if nYr not in my_results.keys():
            my_results[nYr] = {}
        opt_years.append( pi[0][0]['case_notes'].strip("'") )
        # For testing get opt_years from name
        if 'Tested' in pi[0][0]['case_name']:
            opt_years[-1] = pi[0][0]['case_name'].split('DYrs')[-1].split('_')[0]
        if test_years_name in info[-3+mod]:
            test_years.append(int(info[-3+mod].replace(test_years_name,'').split('-')[0]))
            end_test_years.append(int(info[-3+mod].replace(test_years_name,'').split('-')[-1]))
            if 'SF' in f:
                sfs.append(float(info[-2].replace('SF','')))
            else:
                sfs.append(-1)
        else:
            test_years.append(-1)
            end_test_years.append(-1)
            sfs.append(-1)
        if 'Iter' in info[-3]:
            ITER.append(int(info[-3].replace('Iter','')))
        else:
            ITER.append(-1)

        # Fix test years, should redo above code but...
        if test_years[-1] == -1 and 'Tested' in pi[0][0]['case_name']:
            test_years[-1] = pi[0][0]['case_name'].split('Tested')[-1]
        
        status.append(pi[1][0]['status'])
        name.append(pi[0][0]['case_name'])
        syst_cost.append(pi[1][0]['system_cost'])
        try: # This indentation is new b/c we now may skip saving
            # the time series results and will have these values in the summary
            # results area instead.
            curtailed_gen.append(np.mean(pi[1][2]['main_node_curtailment dispatch']))
            lost_load.append(np.mean(pi[1][2]['lost_load dispatch']))
            max_lost_load.append(np.max(pi[1][2]['lost_load dispatch']))

            if 'natgas dispatch' in pi[1][2].keys():
                pct_decarb.append(1. - np.mean(pi[1][2]['natgas dispatch']))
                # Calc the NG dispatch vector
                n_slices_per_year = int(8760/int(deltaT)) # should adjust by mapping calendar year to n_hrs_per_year (~8760)
                NGs = []
                for yr in range(int(nYr)):
                    NG_disp = pi[1][2]['natgas dispatch'][yr * n_slices_per_year : (yr + 1) * n_slices_per_year ]
                    NGs.append(np.mean(NG_disp))
                my_results[nYr][f] = NGs

            else:
                pct_decarb.append(1)
        except:
            curtailed_gen.append(-1)
            lost_load.append(pi[1][1]['lost_load dispatch'])
            max_lost_load.append(pi[1][1]['lost_load max dispatch'])

            if 'natgas dispatch' in pi[1][1].keys():
                pct_decarb.append(1. - np.mean(pi[1][1]['natgas dispatch']))
            else:
                pct_decarb.append(1)
        
        if first:
            first = False
            df = pd.DataFrame(data=pi[1][1], index=[cnt,])
        else:
            df = pd.concat( [df, pd.DataFrame(data=pi[1][1], index=[cnt,])] )
        cnt += 1
    #print(name)
    #print(syst_cost)
    df['status'] = status
    df['name'] = name
    df['date'] = dates
    df['region'] = regions
    df['n_years'] = n_years
    df['opt_years'] = opt_years
    df['test_years'] = test_years
    df['iter'] = ITER
    df['end_test_year'] = end_test_years
    df['scale_factor'] = sfs
    df['syst_cost'] = syst_cost
    df['curtailed_gen'] = curtailed_gen
    df['lost_load'] = lost_load
    df['max_lost_load'] = max_lost_load
    df['decarbonization'] = pct_decarb
    df['co2_intensity'] = 1. - np.array(pct_decarb)
    
    print(f"Found entries {len(df.index)}")
    df = df.sort_values(by=['n_years', 'scale_factor','opt_years','test_years'])
    post = '' if not test else '_TestArchs'
    df.to_csv(f'plotting-scripts/n_years_{date}_{region}_{techs}{post}.csv')
    #save_my_results(my_results)
    return df


def save_my_results(my_results):

    n_years = list(my_results.keys())
    f_out = "-".join(n_years)
    
    with open(f_out + '.pickle', 'wb') as f:
        pickle.dump(my_results, f, protocol=pickle.HIGHEST_PROTOCOL)
    print(f"Pickle file written: {f_out}.pickle")

    # Also, save a set of csv files for easy inspection
    for NYEAR, items in my_results.items():
        df = pd.DataFrame(items)
        df.to_csv(f"my_results_{NYEAR}.csv")
    



test = False # This denotes we ran a fixed capacity test of syst performance
#test = True
verbose = True
#verbose = False
combos = OrderedDict()
for date in ['Dec10Demo',]:
    for region in ['CONUS',]:# 'FR']:
        for tech in ['SWB', 'SWBNG', 'SWBPGP']:
            combos[f'{region} {tech} 0% {date}'] = [date, tech, 'nYrs', region, 0]

dfs = {}
deltaT = '' # '2' # '4' # used for Mar21v2dT
for deltaT in ['4',]:#1,]:#2, 4, 6, 8, 12, 24]:
    deltaT = str(deltaT)
    for name, vals in combos.items():
        #print(name, vals)
        df = make_results_file(vals[0], vals[1], vals[3], vals[2], test, deltaT)
        if type(df) == int:
            continue
        for NYEARS in df['n_years'].unique():
            tmp = df.loc[ df['n_years'] == NYEARS ]
            print(f" --- n_years: {NYEARS} = {len(tmp.index)} files")
            if not verbose:
                continue
            missing = []
            # I hand checked the ones with -1 and they are all good
            if tmp.iloc[0]['iter'] == -1:
                continue 
            for ITER in range(nYrs_map[NYEARS]):
                selected = tmp[ tmp['iter'] == ITER ]
                if len(selected.index) > 1:
                    print("This sounds no happen")
                    assert(False)
                if len(selected.index) == 0:
                    missing.append(ITER)
            if len(missing) > 0:
                print(f" ------ missing {missing}")



