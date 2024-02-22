
# You will need to copy this into the MEM directory and update the BASE directory and FILE list and DELTAT

BASE="Input_Data/Lei_Solar_Wind/" # Path to input files
DELTAT=4 # Number of hours per time step
export HEADER=5 # Number of header rows in your selected MEM input files (this can vary from file to file)


for FILE in US_capacity_solar_25pctTop_unnormalized US_capacity_wind_25pctTop_unnormalized US_demand_unnormalized; do

    if [ ${FILE} == "US_demand_unnormalized" ]; then
        export HEADER=11
    fi

    python change_delta_T_for_inputs.py "${BASE}${FILE}.csv" ${DELTAT} ${HEADER}
    echo ""
    echo ""

    echo "Prepending to file: ${BASE}${FILE}_deltaT${DELTAT}.csv"
    echo "BEGIN_DATA,,,," > tmp.csv
    cat "${BASE}${FILE}_deltaT${DELTAT}.csv" >> tmp.csv
    mv tmp.csv "${BASE}${FILE}_deltaT${DELTAT}.csv"
done
