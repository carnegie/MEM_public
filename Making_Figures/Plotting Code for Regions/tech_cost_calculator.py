import numpy as np
import math as m

hours_per_year = 8760

#%% RFB cost calculator

rfb_crf = 0.10

def get_third_tech_fhc(oc):
    return (oc * rfb_crf) / hours_per_year

def get_third_tech_oc(fhc):
    return (fhc * hours_per_year) / rfb_crf


#%% Battery cost calculator

batt_crf = 0.1424
batt_fixed_om = 24.7 / m.sqrt(0.9)

def get_batt_fhc(oc):
    return ((oc * batt_crf) + batt_fixed_om) / hours_per_year

def get_batt_oc(fhc):
    return ((fhc * hours_per_year) - batt_fixed_om) / batt_crf

#%% PGP cost calculator

############ To_PGP Costs ############ 

kWh_LHV_per_kg_H2 = 33.33

# stack, BoP, and compressor overnight costs ($/kWh)
stack_cost = 20673.73626903 / kWh_LHV_per_kg_H2
bop_cost = 6904.42752000 / kWh_LHV_per_kg_H2
comp_cost = 916.61494263 / kWh_LHV_per_kg_H2
total_cost = stack_cost + bop_cost + comp_cost

# stack, BoP, and compressor fraction of total costs ($/kWh)
stack_f = stack_cost / total_cost
bop_f = bop_cost / total_cost
comp_f = comp_cost / total_cost

# stack, BoP, and compressor capital recovery factors
stack_crf = 0.1855532196
bop_crf = 0.0750091389
comp_crf = 0.1097946247
total_crf = (stack_f * stack_crf) + (bop_f * bop_crf) + (comp_f * comp_crf)

# stack, BoP, and compressor fixed O&M ($/kWh)
stack_bop_fixed_om = 2180.06989802 / kWh_LHV_per_kg_H2
comp_fixed_om = 182.33331310 / kWh_LHV_per_kg_H2
total_fixed_om = stack_bop_fixed_om + comp_fixed_om

def get_to_pgp_fhc(oc):
    return (oc * total_crf + total_fixed_om) / hours_per_year

def get_to_pgp_oc(fhc):
    return ((fhc * hours_per_year) - total_fixed_om) / total_crf

############ PGP_storage Costs ############ 

# cavern cost, capital recovery factor, and fixed O&M
cavern_cost = 6.85909051 / kWh_LHV_per_kg_H2
cavern_crc = 0.0805864035
cavern_fixed_om =  0.53720535 / kWh_LHV_per_kg_H2

def get_pgp_storage_fhc(oc):
    return (oc * cavern_crc + cavern_fixed_om) / hours_per_year

def get_pgp_storage_oc(fhc):
    return ((fhc * hours_per_year) - cavern_fixed_om) / cavern_crc

############ From_PGP Costs ############ 

# PEM fuel cell cost, capital recovery factor
pem_cost = 2182.8
pem_crc = 0.0943929257

def get_from_pgp_fhc(oc):
    return (oc * pem_crc) / hours_per_year

def get_from_pgp_oc(fhc):
    return (fhc * hours_per_year) / pem_crc
