DATE="May17v1"

# Settings
DELTAT=4
LOSTLOAD=0
INPUT_FILE="case_input_reli_20210220.csv"
REGION="CONUS"

# Where to start and how many iters
START=0
ITERS=100 # ITERS minus START = number of optimizations run

# TECHS lists the technologies present in a given optimization.
#   S = solar
#   W = wind
#   B = battery
#   PGP = PGP
#   NG = natgas
#       When using NG, you can specify the amount of natural gas dispatch to the system.
#       The value seen below for CONSU, 303461, is based on the non-normailzed CONUS demand where
#       and 0.05 in line 28 indicates 5% of full NG dispatch is allowed in the optimization.



# Case specific
### SWBNG
TECHS="SWBNG"
NGDISP=$(echo "0.05 * "303461 | bc -l) # This is 5% emissions from pure NG baseline w/ CONUS demand profile
for NYEARS in -1; do
    python run_n_year_rand.py ${INPUT_FILE} ${REGION} ${NYEARS} ${TECHS} ${DATE} 1 ${DELTAT} ${ITERS} ${START} ${NGDISP} ${LOSTLOAD} &
done

### SWB only
NGDISP=-1 # can use -1 or 0 b/c there is no emitting tech
TECHS="SWB"
for NYEARS in -1; do
    python run_n_year_rand.py ${INPUT_FILE} ${REGION} ${NYEARS} ${TECHS} ${DATE} 1 ${DELTAT} ${ITERS} ${START} ${NGDISP} ${LOSTLOAD} &
done

### SWBPGP
NGDISP=-1
TECHS="SWBPGP"
INPUT_FILE="case_input_reli_20210220_w_PGP.csv"
for NYEARS in -1; do
    python run_n_year_rand.py ${INPUT_FILE} ${REGION} ${NYEARS} ${TECHS} ${DATE} 1 ${DELTAT} ${ITERS} ${START} ${NGDISP} ${LOSTLOAD}
done


echo "THIS NEXT SECTION WILL NOT RUN UNTIL THE ABOVE CODE IS FINISHED"
echo "AFTER THE ORIGINAL OPTIMIZATIONS ARE COMPLETE, RUN"
echo "$ alt_aggregate_results.py"
echo "AFTER CHANGING THE DATE CORRESPONDINGLY"
echo "THEN UNCOMMENT THIS LOWER CODE"

#python run_n_year_fixed_capacities.py plotting-scripts/n_years_May17v1_${REGION}_SWB.csv -1 -1 -1 True &
#python run_n_year_fixed_capacities.py plotting-scripts/n_years_May17v1_${REGION}_SWBNG.csv -1 -1 -1 True &
#python run_n_year_fixed_capacities.py plotting-scripts/n_years_May17v1_${REGION}_SWBPGP.csv -1 -1 -1 True &
