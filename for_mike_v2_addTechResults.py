#######################################
# v2 updates this script to run on the output of `case_EV_template_2021-08-16_v3.csv`
# It searches for the set of excel output files from running
# "python Run_Case_Mike_EV_template.py  case_EV_template_2021-08-16_v3.csv"
# And makes some simple distributions.



# As you go through this code, Mike, use "#" to comment out lines. This can help
# if you get annoyed with the print statements.



# Import the modules you will use
import numpy as np # lots of helpful math stuff
import pandas as pd # lots of helpful csv/table/dataframe stuff
import matplotlib.pyplot as plt # lots of helpful plotting stuff
from glob import glob # searches for files
import sys


print("These are the arguments you included when running the script")
print(sys.argv)

# This allows you to choose the output directory so you don't have to hardcode
# it every time.
if len(sys.argv) > 1:
    base_path = sys.argv[1]
else:
    base_path = 'Output_Data/Mike_EV/'



# Searches for files matching the path below where "*" is a wildcard
path_to_search = f'{base_path}/Looping_Gas_Test_evLoad*/*.xlsx'
print(f"Searching path: {path_to_search}")
files = glob(path_to_search)
print(f"Found files: {files}")

# Loop over all found files and make a counter "i"
for i, f in enumerate(files):
    print(f" --- opening file {i}: {f}")

    # Load a "dataframe" from a sheet in an excel file
    df = pd.read_excel(f, sheet_name='case results', index_col=1)
    # Transpose
    df = df.T
    print(df.head())
    # Add column to dataframe with CASE_NAME
    df['scenario'] = f.split('/')[-1].split('_2021')[0] # you can split this command
    # up into multiple lines and print it out if curious
    #print(df.head())
   
    # Open tech_results sheet
    df2 = pd.read_excel(f, sheet_name='tech results', index_col=1)
    # Transpose
    df2 = df2.T
    print(df2.head())

    # Extend df with df2's data
    for col in df2.columns:
        df[col] = df2[col]
    print(df.head())


    # Keep track of growing list of results
    if i == 0:
        first = df
    else:
        first = first.append(df)

# Print current dataframe
print(first.head(50))
# Drop those dummy/empty rows
first = first.loc[ first['status'] == 'optimal' ]
# Sort results by CASE_NAME (which has EV load in it)
first = first.sort_values(['scenario'])
# Reset index values b/c appending dataframes can be messy
first = first.reset_index()
print(first.head(50))

# Drop dummy old index
first = first.drop(columns=['index',])

## THESE ARE CALCULATED IN MEM NOW, SO COMMENT OUT
## Add Demand and EV Demand to columns
## by looping over all rows and getting EV Demand from the scenario name
#dems = []
#evs = []
#for idx in first.index:
#
#    # Demand is always '1'
#    dems.append(1.)
#
#    # Get EV Demand from scenario
#    scen = first.loc[idx, 'scenario']
#    ev = evs.append(float(scen.split('evLoad')[-1].replace('p','.')))
#first['demand'] = dems
#first['ev demand'] = evs
# Add columns
first['ev demand'] = np.zeros(len(first.index))
for col in ['ev1 mean demand', 'ev1 mean demand']:
    if col in first.columns:
        first['ev demand'] += first[col]
first['total demand'] = first['main mean demand'] + first['ev demand']
first['ev load fraction'] = first['ev demand'] / first['total demand']

# Save this dataframe to a csv file so you can skip the reading files part next time
# b/c it takes a long time!
append = base_path.split('/')[1] # Takes second piece of "output_data/XYZ" by splitting on the "/"
first.to_csv(f'tmp_{append}.csv', index=False)
print(f"Saved to tmp_{append}.xlsx")

## Next time when you run this, you can comment out everything above this
## except the "import" lines
#df = pd.read_csv('tmp.csv', index_col=False)
#
#print(df.head())



## Make super simple time series plot of demand --- this one plots ALL the data and is too hard to view.
#fig, ax = plt.subplots()
#ax.plot(df['ev load fraction'], df['system_cost'], label='system cost')
#ax.set_xlabel('ev load / total load')
#ax.set_ylabel('system cost ($/hr)')
#ax.set_ylim(0, ax.get_ylim()[1])
#plt.legend()
#plt.show()
#
## Make super simple time series plot of demand but only take the first 100 hours [You will have to read about python slice notation :-) ]
#
#fig, ax = plt.subplots()
#ax.plot(df['ev load fraction'], df['system_cost']/df['total demand'], label='system cost/total demand')
#ax.set_xlabel('ev load / total load')
#ax.set_ylabel('system cost/total load ($/kWh)')
#ax.set_ylim(0, ax.get_ylim()[1])
#plt.legend()
#plt.show()
#
## Plot on same figure
#max_ = 0
#fig, axs = plt.subplots(ncols=2, figsize=(8,4))
#axs[0].plot(df['ev load fraction'], df['system_cost'], label='system cost')
#axs[0].set_xlabel('ev load / total load')
#axs[0].set_ylabel('system cost ($/hr)')
#axs[1].plot(df['ev load fraction'], df['system_cost']/df['total demand'], label='system cost/total demand')
#axs[1].set_xlabel('ev load / total load')
#axs[1].set_ylabel('system cost/total load ($/kWh)')
#top = np.max([axs[0].get_ylim()[1], axs[1].get_ylim()[1]]) # Max of both distributions
#axs[0].set_ylim(0, top)
#axs[1].set_ylim(0, top)
#plt.tight_layout()
#plt.show()



