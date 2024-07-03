import numpy as np
import pandas as pd

# Change the delta T resolution of the input files
# and write a new output file.
# 
# Arguments: 
#   - f_name = full file path from the MEM directory
#   - new_resolution = new deltaT resolution, must be a divisor of 24.
#   - header = number of header rows in input file (so Pandas can open the data portion of the file
def change_resolution(f_name, new_resolution, header=1):

    print(f"Changing delta T resolution for input file: {f_name}")
    print(f"Old resolution == 1hr (this is default), New resolultion == {new_resolution}hr")

    assert(24%new_resolution==0), f"Selected merging threshold not a divisor of 24. 24%{new_resolution}=={24%new_resolution}."

    df = pd.read_csv(f_name, header=header)

    cols = df.columns
    print(f"These are the header columns: {cols}.")
    print("If these headers look incorrect, you many need to adjust the header argument to pick up the correct column names.")
    
    # Get naming convention for hour column (hour or Hour?)
    hr_col = ''
    if 'hour' in cols:
        hr_col = 'hour'
    elif 'Hour' in cols:
        hr_col = 'Hour'
    else:
        print("ERROR: It is unclear what the naming of the hour column is for this input file.")
        exit()

    df[f'{cols[-1]} mod'] = df[cols[-1]].rolling(window=new_resolution).sum()
    df = df.loc[ ~df[f'{cols[-1]} mod'].isna() ]
    df[f'{cols[-1]}'] = df[f'{cols[-1]} mod']/float(new_resolution)
    df1 = df.loc[ df[hr_col]%new_resolution == 0 ]
    df1 = df1.drop([f'{cols[-1]} mod',], axis=1)
    new_f_name = f_name.replace('.csv', '_deltaT')+str(new_resolution)+'.csv'
    df1.to_csv(new_f_name, index=False)
    print(f"New file: {new_f_name}")
    return

if '__main__' in __name__:
    import sys
    assert(len(sys.argv) == 4)
    print(sys.argv)
    f_name = 'Input_Data/Lei_Solar_Wind/US_capacity_wind_CONUS_unnormalized.csv'
    f_name = sys.argv[1]
    new_resolution = int(sys.argv[2])
    header = int(sys.argv[3])
    change_resolution(f_name, new_resolution, header)
    


