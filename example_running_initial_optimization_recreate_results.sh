DATE="Jan29v1" # 1 yr sims

# Settings
DELTAT=4
LOSTLOAD=0
INPUT_FILE="case_input_reli_20210220.csv"

# Where to start and # to do
START=0
ITERS=1 # CHANGE

### SWBNG
TECHS="SWBNG"
NGDISP=$(echo "0.05 * "303461 | bc -l) # This is 5% emissions from pure NG baseline w/ CONUS demand profile
for REGION in "CONUS"; do
    for NYEARS in 1 2 3 4 5 7 10 15 25 40; do
        python run_n_year_rand.py ${INPUT_FILE} ${REGION} ${NYEARS} ${TECHS} ${DATE} 1 ${DELTAT} ${ITERS} ${START} ${NGDISP} ${LOSTLOAD}
    done
done

### SWB only
NGDISP=-1 # can use -1 or 0 b/c there is no emitting tech
TECHS="SWB"
for REGION in "CONUS"; do
    for NYEARS in 1 2 3 4 5 7 10 15 25 40; do
        python run_n_year_rand.py ${INPUT_FILE} ${REGION} ${NYEARS} ${TECHS} ${DATE} 1 ${DELTAT} ${ITERS} ${START} ${NGDISP} ${LOSTLOAD}
    done
done

NGDISP=-1
TECHS="SWBPGP"
INPUT_FILE="case_input_reli_20210220_w_PGP.csv"

for REGION in "CONUS"; do
    for NYEARS in 1 2 3 4 5 7 10 15 25 40; do
        python run_n_year_rand.py ${INPUT_FILE} ${REGION} ${NYEARS} ${TECHS} ${DATE} 1 ${DELTAT} ${ITERS} ${START} ${NGDISP} ${LOSTLOAD}
    done
done

