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


# Searches for files matching the path below where "*" is a wildcard
files = glob('Output_Data/Mike_EV/TestCase-0emit_evLoad*/*.xlsx')
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

# Add Demand and EV Demand to columns
# by looping over all rows and getting EV Demand from the scenario name
dems = []
evs = []
for idx in first.index:

    # Demand is always '1'
    dems.append(1.)

    # Get EV Demand from scenario
    scen = first.loc[idx, 'scenario']
    ev = evs.append(float(scen.split('evLoad')[-1].replace('p','.')))
first['demand'] = dems
first['ev demand'] = evs

# Save this dataframe to a csv file so you can skip the reading files part next time
# b/c it takes a long time!
first.to_csv('tmp.csv', index=False)
print("Saved to tmp.xlsx")

# Next time when you run this, you can comment out everything above this
# except the "import" lines
df = pd.read_csv('tmp.xlsx', index_col=False)
# Add columns
df['total demand'] = df['demand'] + df['ev demand']
df['ev load fraction'] = df['ev demand'] / df['total demand']

print(df.head())






