DATE="Dec10Demo"

# Settings
DELTAT=4
LOSTLOAD=0
INPUT_FILE="case_input_reli_20210220.csv"
REGION="CONUS"
NGDIS=-1


for NYEARS in 1 2 3; do
    python run_n_year_fixed_capacities.py plotting-scripts/n_years_${DATE}_${REGION}_SWB.csv ${NYEARS} -1 &
    python run_n_year_fixed_capacities.py plotting-scripts/n_years_${DATE}_${REGION}_SWBNG.csv ${NYEARS} -1 &
    python run_n_year_fixed_capacities.py plotting-scripts/n_years_${DATE}_${REGION}_SWBPGP.csv ${NYEARS} -1 &
done
