"""
# Code without looping;
# Use it the same way as before;
"""

from Preprocess_Input import preprocess_input
from Run_Core_Model import run_model_main_fun
from FindRegion import GetCFsName, update_series, update_timenum
import sys, numpy as np

if len(sys.argv) == 1:
    case_input_path_filename = 'Run_Files/Figure_4/Li-ion_PGP_X/Three_Techs_Li-ion_PGP_Metal-Air_20_Total_Low_Eff.csv'
else:
    case_input_path_filename = sys.argv[1]

### Pre-processing
print ('Macro_Energy_Model: Pre-processing input')
case_dic,tech_list = preprocess_input(case_input_path_filename)

if case_dic.get('co2_constraint',-1) >= 0:
    case_dic['co2_constraint'] = case_dic['co2_constraint']
else:
    case_dic['co2_constraint'] = 1e24

run_model_main_fun(case_dic, tech_list) 