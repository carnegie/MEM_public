# -*- codiNatgas: utf-8 -*-
'''
  Top level function for the Simple Energy Model Ver 1.
  
  The main thing a user needs to do to be able to run this code from a download
  from github is to make sure that <case_input_path_filename> points to the 
  appropriate case input file.
  
  The format of this file is documented in the file called <case_input.csv>.
  
  If you are in Spyder, under the Run menu you can select 'configuration per File' Fn+Ctrl+F6
  and enter the file name of your input .csv file, e.g., Check 'command line options'
  and enter ./case_input_base_190716.csv
  
'''

from Preprocess_Input import preprocess_input
from Core_Model import core_model
from Extract_Cvxpy_Output import extract_cvxpy_output
from Save_Basic_Results import save_basic_results

import sys
from shutil import copy2
import os
import numpy as np
 

# =============================================================================

if len(sys.argv) == 1:
    #case_input_path_filename = './case_input.csv'
    case_input_path_filename = './Combo_4_all.csv'
else:
    case_input_path_filename = sys.argv[1]

# =============================================================================

print ('Macro_Energy_Model: Pre-processing input')
case_dic,tech_list = preprocess_input(case_input_path_filename)

#  parameter sweep of costs for CSP and TES
for idx in range(len(tech_list)):
    name = tech_list[idx]['tech_name']
    if name == 'CSP_TES': tes_idx = idx
    if name == 'battery': batt_idx = idx
    #if name == 'CSP_generation': cspg_idx = idx
    #if name == 'CSP_turbine': cspt_idx = idx
    #if name == 'PV': pv_idx = idx

tes_base = tech_list[tes_idx]['fixed_cost']
batt_base = tech_list[batt_idx]['fixed_cost']
#cspg_base = tech_list[cspg_idx]['fixed_cost']
#cspt_base = tech_list[cspt_idx]['fixed_cost']
#pv_base = tech_list[pv_idx]['fixed_cost']

multiplier = np.linspace(0,1.5,13)
batt_multiplier = np.array([1.125,1.25,1.375,1.5])
tes_costs = tes_base*multiplier
batt_costs = batt_base*batt_multiplier
#cspg_costs = cspg_base*multiplier
#cspt_costs = cspt_base*multiplier
#pv_costs = pv_base*multiplier

# PROBLEMS: Does not write correct input file, uses original base case every time
case_dic['output_path'] = 'Output_Data/Batt_TES_Sweep/'
for i in range(len(batt_costs)):
    case_name_default = 'Batt' + str(batt_multiplier[i]) + 'x_TES'
    tech_list[batt_idx]['fixed_cost'] = batt_costs[i]
    #tech_list[tes_idx]['fixed_cost'] = tes_costs[i]
    #tech_list[pv_idx]['fixed_cost'] = pv_costs[i]
    #tech_list[cspg_idx]['fixed_cost'] = cspg_costs[i]
    #tech_list[cspt_idx]['fixed_cost'] = cspt_costs[i]
    for j in range(len(multiplier)):
        tech_list[tes_idx]['fixed_cost'] = tes_costs[j]
        #tech_list[batt_idx]['fixed_cost'] = batt_costs[j]
        #tech_list[pv_idx]['fixed_cost'] = pv_costs[j]
        case_dic['case_name'] = case_name_default + str(multiplier[j]) + 'x'
        # Run models here
        output_folder = case_dic['output_path'] + case_dic['case_name']
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
            try:
                copy2(case_input_path_filename, output_folder)
            except:
                print ('case input file '+case_input_path_filename+' not copied. '+
                       'Perhaps it does not exist. Perhaps it is open and cannot be overwritten.')  
 
        print ('Macro_Energy_Model: Executing core model')
        print ('Case Name: ', case_dic['case_name'])
        constraint_list,cvxpy_constraints,cvxpy_prob,cvxpy_capacity_dic,cvxpy_dispatch_dic,cvxpy_stored_dic = core_model(case_dic, tech_list)
        prob_dic,capacity_dic,dispatch_dic,stored_dic = extract_cvxpy_output(case_dic,tech_list,constraint_list,
                                                                             cvxpy_constraints,cvxpy_prob,cvxpy_capacity_dic,cvxpy_dispatch_dic,cvxpy_stored_dic )
        print ('Simple_Energy_Model: Saving basic results')
        [[input_case_dic,   input_tech_list,  input_time_dic  ],
         [results_case_dic, results_tech_dic, results_time_dic]] = save_basic_results(case_dic, tech_list, cvxpy_constraints,prob_dic,capacity_dic,dispatch_dic,stored_dic)
