# Code to extract the data from a directory of pickle files

#%% Import
import pickle
import glob
import numpy as np
import sys
sys.path.append('C:/Users/covel/OneDrive/Desktop/Rerun-for-Anna/Dom Plotting Code')
from tech_cost_calculator import *

#%% tech_idx and corresponding technologies (changes based on the order of row in input file)

'''
inputs[2]: solar
inputs[3]: wind
inputs[4]: battery
inputs[5]: 3rd_tech_energy
inputs[6]: 3rd_tech_power
tech_list[0]: demand

tech_list[1]: curtainment
tech_list[2]: solar
techlist[3]: wind
techlist[4]: battery
techlist[5]: 3rd_tech_energy
techlist[6]: 3rd_tech_power
'''

#%%

# get_cost_contributions: sorts the contents of a pickle file into a dictionary

def get_cost_contributions(base):
    #mulitply var cost by dispatch
    #multiply fixed cost by capacity
    info = base[0]
    inputs = base[0][1]
    results = base[1]
    name_list = []
    fixed_costs = []
    var_costs = []
#    print(inputs)
    for tech in inputs:
        if tech['tech_name'] == 'demand':
            continue
        if tech['tech_name'] == 'main_curtailment':
            continue
        if tech['tech_name'] == 'unmet':
            continue
        name_list.append(tech['tech_name'])
        fixed_costs.append(float(tech['fixed_cost']))
        if 'var_cost' in tech:
            var_costs.append(tech['var_cost'])
        else:
            var_costs.append(0)
    caps = []
    disps = []
    for i in name_list:
        caps.append(results[1][str(i) + ' capacity'])
        if i == 'wind' or i =='PV':
            disps.append(np.mean(results[2][str(i) + ' potential'])) 
        else:
            disps.append(np.mean(results[2][str(i) + ' dispatch']))
    cost_list = []
    for i in range(len(name_list)):
        cost_list.append(fixed_costs[i]*caps[i] + var_costs[i]*disps[i])
    costconts = {}
    for k, v in zip(name_list, cost_list):
        costconts[k] = v
        
    return costconts

#%%

def calculate_duration(data_dic, energy_tech, power_tech, nones):
    energy_cap = data_dic.get(energy_tech + '_cap')
    power_cap = data_dic.get(power_tech + '_cap')
    duration = []
    for i in range(len(energy_cap)):
        if (power_cap[i] != 0) and (power_cap[i] != None):
            duration.append(energy_cap[i]/power_cap[i])
        else:
            if nones == True:
                duration.append(None)
            else:
                duration.append(10**-10)
    return duration
    
def calculate_cycles(data_dic, dispatch_tech, capacity_tech, nones):
    tot_dispatch = data_dic.get(dispatch_tech + '_tot_dispatch')
    cap = data_dic.get(capacity_tech + '_cap')
    cycles = []
    for i in range(len(cap)):
        if (cap[i] != 0) and (cap[i] != None):
            cycles.append(tot_dispatch[i]/cap[i])
        else:
            if nones == True:
                cycles.append(None)
            else:
                cycles.append(10**-10)
    return cycles

def add(*p):
    return sum(filter(None, p))

#%%
# Extracts data and makes calculations on data for all pickle files from 'path' directory
# Stores processed data into dictionary
# Change the parameters stored/processed as needed

storage_tech = ['battery', 'third_tech_energy', 'third_tech_power']
energy_tech = ['battery', 'third_tech_energy']
storage_tech_idx = [4, 6, 5]
parameters = ['fixed_cost', 'capacity', 'dispatch', 'stored']


def get_data_one_power(path, techidx1, var1, techidx2, var2, nones):

    unsorted_list = glob.glob(path + '/*.pickle')
    # Sort pickle files by variable

    par_list = []
    for i in range(len(unsorted_list)):
        pickle_in = open(unsorted_list[i],"rb")
        base = pickle.load(pickle_in)
        info = base[0]
        inputs = base[0][1]
        results = base[1]
        #var, pickle
        par_list.append((float(inputs[techidx1][var1]), float(inputs[techidx2][var2]), base))
        
    par_list.sort(key=lambda x:(x[0], x[1]))
    
    # Create empty dictionary to return values
    data = {}
    
    data['var1_list'] = [i[0] for i in par_list]
    data['var2_list'] = [i[1] for i in par_list]
    base_list = [i[2] for i in par_list]
    
    # Create empty lists for data dictionary
    
    # Output tech costs
    data['solar_cost'] = []
    data['wind_cost'] = []
    data['batt_cost'] = []
    data['third_tech_cost'] = []
    data['elec_cap'] = []
    data['system_cost'] = []
    
    # Create empty lists
    for tech in storage_tech:
        data[tech + '_cost'] = []
        data[tech + '_cap'] = []
        data[tech + '_tot_dispatch'] = []
    for tech in energy_tech:
        data[tech + '_time_stored'] = []
   
    # Unmet Demand   
    data['unmet_demand'] = []

    # Extract data from each pickle file

    for base in base_list:
        info = base[0]
        inputs = base[0][1]
        results = base[1]
        
        dic = get_cost_contributions(base)
        
        # Output tech costs
        data['solar_cost'].append(dic.get('PV'))
        data['wind_cost'].append(dic.get('wind'))
        data['batt_cost'].append(dic.get('battery'))
        data['third_tech_cost'].append(add(dic.get('third_tech_energy'), dic.get('third_tech_power')))
        data['system_cost'].append(results[0].get('system_cost'))
        
        for idx, tech in enumerate(storage_tech):
            try:
                data[tech + '_cost'].append(float(inputs[storage_tech_idx[idx]].get('fixed_cost')))
            except:
                pass
            data[tech + '_cap'].append(results[1].get(tech + ' capacity'))
            data[tech + '_tot_dispatch'].append(np.sum(results[2].get(tech + ' dispatch')))
        for tech in energy_tech:
            try:
                if (data[tech + '_cap'] is None):
                    data[tech + '_time_stored'].append(None)
                else:
                    data[tech + '_time_stored'].append(np.average(results[2].get(tech + ' stored')))
            except:
                pass
        
        # Unmet demand  
        if 'unmet dispatch' in results[2].keys():
            data['unmet_demand'].append(np.sum(results[2].get('unmet dispatch')))
    
    # Calculate cycles and durations
    data['third_tech_dur'] = calculate_duration(data, 'third_tech_energy', 'third_tech_power', nones)

    
    data['third_tech_cycles'] = calculate_cycles(data, 'third_tech_energy', 'third_tech_energy', nones)
    data['batt_cycles'] = calculate_cycles(data, 'battery', 'battery', nones)
    
    return data