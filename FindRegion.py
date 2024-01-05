"""
Lei updated on Feb 8, 2020;
Used to find the corresponding demand/solar/wind input data given year and region name; 
Also re-calculate the total days of that year.
"""


from Preprocess_Input import read_csv_dated_data_file
import numpy as np
import pandas as pd
import datetime

def GetNameList():
    TwoLettersCode = ['DZ','AR','AU','BR','CA','CL','CN',
                      'CO','EG','FR','DE','GH','IN','ID',
                      'IR','IT','JP','LY','MY','MX','MA',
                      'MZ','NZ','NG','PY','PE','PL','RU',
                      'SA','ZA','KR','ES','SD','SE','TH',
                      'TN','TR','UA','GB','US','VE','VN']
    return TwoLettersCode


def GetCFsName(region_name):
    FullDemandList = {'DZ': 'demand_series_Dan_normalized_to_1_mean_Algeria.csv', 'AR': 'demand_series_Dan_normalized_to_1_mean_Argentina.csv',
                      'AU': 'demand_series_Dan_normalized_to_1_mean_Australia.csv', 'BR': 'demand_series_Dan_normalized_to_1_mean_Brazil.csv',
                      'CA': 'demand_series_Dan_normalized_to_1_mean_Canada.csv', 'CL': 'demand_series_Dan_normalized_to_1_mean_Chile.csv',
                      'CN': 'demand_series_Dan_normalized_to_1_mean_China.csv', 'CO': 'demand_series_Dan_normalized_to_1_mean_Colombia.csv',
                      'EG': 'demand_series_Dan_normalized_to_1_mean_Egypt.csv', 'FR': 'demand_series_Dan_normalized_to_1_mean_France.csv',
                      'DE': 'demand_series_Dan_normalized_to_1_mean_Germany.csv', 'GH': 'demand_series_Dan_normalized_to_1_mean_Ghana.csv',
                      'IN': 'demand_series_Dan_normalized_to_1_mean_India.csv', 'ID': 'demand_series_Dan_normalized_to_1_mean_Indonesia.csv',
                      'IR': 'demand_series_Dan_normalized_to_1_mean_Iran.csv', 'IT': 'demand_series_Dan_normalized_to_1_mean_Italy.csv',
                      'JP': 'demand_series_Dan_normalized_to_1_mean_Japan.csv', 'LY': 'demand_series_Dan_normalized_to_1_mean_Libya.csv',
                      'MY': 'demand_series_Dan_normalized_to_1_mean_Malaysia.csv', 'MX': 'demand_series_Dan_normalized_to_1_mean_Mexico.csv',
                      'MA': 'demand_series_Dan_normalized_to_1_mean_Morocco.csv', 'MZ': 'demand_series_Dan_normalized_to_1_mean_Mozambique.csv',
                      'NZ': 'demand_series_Dan_normalized_to_1_mean_New Zealand.csv', 'NG': 'demand_series_Dan_normalized_to_1_mean_Nigeria.csv',
                      'PY': 'demand_series_Dan_normalized_to_1_mean_Paraguay.csv', 'PE': 'demand_series_Dan_normalized_to_1_mean_Peru.csv',
                      'PL': 'demand_series_Dan_normalized_to_1_mean_Poland.csv', 'RU': 'demand_series_Dan_normalized_to_1_mean_Russia.csv',
                      'SA': 'demand_series_Dan_normalized_to_1_mean_Saudi Arabia.csv', 'ZA': 'demand_series_Dan_normalized_to_1_mean_South Africa.csv',
                      'KR': 'demand_series_Dan_normalized_to_1_mean_South Korea.csv', 'ES': 'demand_series_Dan_normalized_to_1_mean_Spain.csv',
                      'SD': 'demand_series_Dan_normalized_to_1_mean_Sudan.csv', 'SE': 'demand_series_Dan_normalized_to_1_mean_Sweden.csv',
                      'TH': 'demand_series_Dan_normalized_to_1_mean_Thailand.csv', 'TN': 'demand_series_Dan_normalized_to_1_mean_Tunisia.csv',
                      'TR': 'demand_series_Dan_normalized_to_1_mean_Turkey.csv', 'UA': 'demand_series_Dan_normalized_to_1_mean_Ukraine.csv',
                      'GB': 'demand_series_Dan_normalized_to_1_mean_United Kingdom.csv', 'US': 'demand_series_Dan_normalized_to_1_mean_United States.csv',
                      'VE': 'demand_series_Dan_normalized_to_1_mean_Venezuela.csv', 'VN': 'demand_series_Dan_normalized_to_1_mean_Vietnam.csv'}
    DemandName = FullDemandList[region_name]
    SolarCFsName = '20201218_' + str(region_name) + '_mthd3_solar.csv'
    WindCFsName = '20201218_' + str(region_name) + '_mthd3_wind.csv'
    return DemandName, SolarCFsName, WindCFsName


def update_series(case_dic, tech_dic):
    series = read_csv_dated_data_file(case_dic['year_start'],
                                      case_dic['month_start'],
                                      case_dic['day_start'],
                                      case_dic['hour_start'],
                                      case_dic['year_end'],
                                      case_dic['month_end'],
                                      case_dic['day_end'],
                                      case_dic['hour_end'],
                                      case_dic['data_path'],
                                      tech_dic['series_file'])
    if 'normalization' in tech_dic:
        if tech_dic['normalization'] >= 0.0:
            series = series * tech_dic['normalization']/np.average(series)
    tech_dic['series'] = series


def update_timenum(case_dic):
    num_time_periods = (24 * (
            datetime.date(case_dic['year_end'],case_dic['month_end'],case_dic['day_end']) - 
            datetime.date(case_dic['year_start'],case_dic['month_start'],case_dic['day_start'])
            ).days +
            (case_dic['hour_end'] - case_dic['hour_start'] ) + 1)
    return num_time_periods

# Added by Tyler Ruggles
def return_file_info_map(region):
    #assert(region in ['CONUS', 'ERCOT', 'NYISO', 'TEXAS'])

    info_map = { # region : # f_path, header rows
        'CONUS': { # New Nov 2021
            'demand': ['CONUS_demand_synthetic_1950-2020_MEM.csv', 0, 'demand (MW)', 'year', 303461], # last is MW mean demand
            'wind': ['20210921_US_mthd3_1950-2020_wind.csv', 3, 'w_cfs', 'year'], # ERA5
            'solar': ['20210921_US_mthd3_1950-2020_solar.csv', 3, 's_cfs', 'year'], # ERA5
            'years' : [y for y in range(1979, 2021)],
            'temp': [None,],
            'to_local' : -6, # CST time = UTC-6
        },
        'ERCOT': { # New files June 2020
            ## Original
            #'demand': ['ERCOT_mem_1998-2019_expDT.csv', 0, 'demand (MW)', 'year'],
            ##'wind': ['20200624v4_ERCO_2018_mthd3_1990-2019_wind.csv', 0, 'w_cfs', 'year'],
            ##'solar': ['20200624v4_ERCO_2018_mthd3_1990-2019_solar.csv', 0, 's_cfs', 'year'],
            #'years' : [y for y in range(2003, 2020)],
            # New
            'demand': ['ERCOT_demand_synthetic_1950-2020_MEM.csv', 0, 'demand (MW)', 'year', 26308], # last is MW mean demand
            ##'wind': ['20210417v2_ERCO_2018_mthd3_1980-2019_wind.csv', 0, 'w_cfs', 'year'],
            ##'solar': ['20210417v2_ERCO_2018_mthd3_1980-2019_solar.csv', 0, 's_cfs', 'year'],
            'wind': ['20210921_ERCOT_mthd3_1950-2020_wind.csv', 3, 'w_cfs', 'year'], # ERA5
            'solar': ['20210921_ERCOT_mthd3_1950-2020_solar.csv', 3, 's_cfs', 'year'], # ERA5
            'years' : [y for y in range(1979, 2021)],
            'temp': ['20210113v5_ERCO_2018_mthd1_2000-2019_temp.csv',],
            'to_local' : -6, # CST time = UTC-6
        },
        'NYISO': { # New files June 2020
            'demand': ['NYISO_demand_unnormalized_expDT.csv', 0, 'demand (MW)', 'year'],
            'wind': ['20200624v4_NYIS_2018_mthd3_1990-2019_wind.csv', 0, 'w_cfs', 'year'],
            'solar': ['20200624v4_NYIS_2018_mthd3_1990-2019_solar.csv', 0, 's_cfs', 'year'],
            'temp': ['20210113v5_NYIS_2018_mthd1_2000-2019_temp.csv',],
            'years' : [y for y in range(2004, 2020)],
            'to_local' : -5, # EST time = UTC-5
        },
        'PJM': { # New files June 2020
            'demand': ['PJM_mem_1993-2019_expDT.csv', 0, 'demand (MW)', 'year'],
            'wind': ['20200624v4_PJM_2018_mthd3_1990-2019_wind.csv', 0, 'w_cfs', 'year'],
            'solar': ['20200624v4_PJM_2018_mthd3_1990-2019_solar.csv', 0, 's_cfs', 'year'],
            'temp': ['20210113v5_PJM_2018_mthd1_2000-2019_temp.csv',],
            'years' : [y for y in range(2006, 2020)],
            'to_local' : -5, # EST time = UTC-5
        },
        'FR': { # New files Dec 2020
            'demand': ['FR_demand_unnormalized_expDT.csv', 0, 'demand (MW)', 'year'],
            #'wind': ['20201230v3_FR_mthd3_1990-2019_wind.csv', 0, 'w_cfs', 'year'],
            #'solar': ['20201230v3_FR_mthd3_1990-2019_solar.csv', 0, 's_cfs', 'year'],
            # New, resources only, no demand avail outside USA
            'wind': ['20210417v2_FR_mthd3_1980-2019_wind.csv', 0, 'w_cfs', 'year'],
            'solar': ['20210417v2_FR_mthd3_1980-2019_solar.csv', 0, 's_cfs', 'year'],
            'temp': ['20210113v4_FR_mthd1_2000-2019_temp.csv',],
            'years' : [y for y in range(2008, 2018)],
            'to_local' : 1, # FR time = UTC+1
        }
    }
    return info_map[region]

# Can grab year long selections from given file and stitch
# them together into a "new" time series.
# returns vector of that new time series.
def stitch_together_select_years(years, f_path):

    head = 1 # if 'rmLeap' in f_path else 5
    # List of files with head = 3
    if f_path.split('/')[-1] in [
            '20210921_ERCOT_mthd3_1950-2020_solar.csv',
            '20210921_ERCOT_mthd3_1950-2020_wind.csv',
            '20210921_US_mthd3_1950-2020_solar.csv',
            '20210921_US_mthd3_1950-2020_wind.csv',
            ]:
        head = 3
    #print(f_path, head)
    df = pd.read_csv(f_path, header=head)

    # Get data column name
    if 'wind' in f_path:
        col = 'w_cfs' 
    elif 'solar' in f_path:
        col = 's_cfs'
    else:
        col = 'demand (MW)'

    for i, year in enumerate(years):

        if i == 0:
            vect = df.loc[ df['year'] == year, col ].values
        else:
            vect = np.append( vect, df.loc[ df['year'] == year, col ].values )
    return vect

# Function to select a random set of study years from an input range.
# Can force the function to avoid perfect overlaps (concurrent years) with avoid_vect.
# Can allow or exclude repeated years with allow_repeats.
# Avoid_vect ensure that values are non-concurrent, but can exist at other times in the time series
def select_random_years(min_yr, max_yr, n_years, seed, avoid_vect=[], allow_repeats=False):

    # Set seed based on 2 versions of numpy
    try:
        rng = np.random.default_rng(seed)
    except:
        np.random.seed(seed)

    vals = []
    cnt = 0
    while len(vals) < n_years:
        try:
            year = rng.integers(low=min_yr, high=max_yr+1, size=1)
            year = year[0]
        except:
            year = np.random.choice([i for i in range(min_yr, max_yr+1)])

        # Check if new year is the same as that position in avoid_vect,
        # Skip if it is
        if len(avoid_vect) > len(vals):
            if avoid_vect[ len(vals) ] == year:
                continue

        # Append if not already in vect, or do it either way if allowing repeats
        if year not in vals or allow_repeats:
            vals.append(year)

        if cnt > 1000:
            print(f"error in select_random_years({min_yr}, {max_yr}, {n_years}, {seed}, avoid_vect={avoid_vect}, allow_repeats {allow_repeats})")
            return -1
        cnt += 1

    for i, val in enumerate(avoid_vect):
        if val == vals[i]:
            print(f"Error in select_random_years: avoid_vect={avoid_vect}, vals {vals}")

    return vals


# Iterate by adding and incrementing years to year vector
def iterate(v, n_years, years, output):
    #print(f"entering iterate, v={v}, n_years={n_years}")

    for yr in years:
        vect = list(v)

        # skip unles >= value to left as we're keeping them
        # ordered, this will save time
        if len(vect) != 0 and yr <= vect[-1]:
            continue

        vect.append(yr)
        this_len = len(vect)

        # Add another entry and
        # check if no unique vals can be added
        while len(vect) < n_years and vect[-1] != years[-1]:
            vect = iterate(vect, n_years, years, output)

        # Check if valid combo
        if len(vect) == n_years and this_len == n_years:
            #print(vect)
            output.append(vect)

    return vect


def nYears_year_combinations(n_years, years):

    if n_years > len(years):
        return []
    print(f"NYears: {n_years}")
    output = []
    vect = []
    iterate(vect, n_years, years, output)
    return output

