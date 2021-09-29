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
 



if len(sys.argv) == 1:
    #case_input_path_filename = './case_input.csv'
    case_input_path_filename = './Combo_4_all_lost_load.csv'
else:
    case_input_path_filename = sys.argv[1]

# =============================================================================


print ('Macro_Energy_Model: Pre-processing input')
case_dic,tech_list = preprocess_input(case_input_path_filename)


for idx in range(len(tech_list)):
    name = tech_list[idx]['tech_name']
    if name == 'lost_load': ll_idx = idx
    

#co2_prices_list = [50000,60000]
ll_prices = [0.25,0.5,0.75]

case_name_default = 'LostLoad_'
#for co2_price_n in co2_prices_list:
for ll_n in ll_prices:
    #case_dic['co2_price'] = co2_price_n
    tech_list[ll_idx]['var_cost'] = ll_n
    #case_dic['case_name'] = case_name_default + 'co2_' + str(co2_n)
    case_dic['case_name'] = case_name_default + str(ll_n)
    # Run models here
    case_dic['output_path'] = 'Output_Data/LLSweepFinal/'
    output_folder = case_dic['output_path'] + case_dic['case_name']
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    try:
        copy2(case_input_path_filename, output_folder)
    except:
        print ('case input file '+case_input_path_filename+' not copied. Perhaps it does not exist. Perhaps it is open and cannot be overwritten.')
    print ('Macro_Energy_Model: Executing core model')
    print ('Case Name: ', case_dic['case_name'])
    constraint_list,cvxpy_constraints,cvxpy_prob,cvxpy_capacity_dic,cvxpy_dispatch_dic,cvxpy_stored_dic = core_model(case_dic, tech_list)
    prob_dic,capacity_dic,dispatch_dic,stored_dic = extract_cvxpy_output(case_dic,tech_list,constraint_list,
                                                                        cvxpy_constraints,cvxpy_prob,cvxpy_capacity_dic,cvxpy_dispatch_dic,cvxpy_stored_dic )
    print ('Simple_Energy_Model: Saving basic results')
    [[input_case_dic,   input_tech_list,  input_time_dic  ],
    [results_case_dic, results_tech_dic, results_time_dic]] = save_basic_results(case_dic, tech_list, cvxpy_constraints,prob_dic,capacity_dic,dispatch_dic,stored_dic)