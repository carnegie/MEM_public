### Input Data for ISO regions

Regions included here are: CISO, MISO, ISNE, ERCO

The demand files have been obtained with [EIA Cleaned Hourly Electricity Demand Data](https://zenodo.org/records/4116342).

The previously obtained files (e.g. CISO.csv) were then reformatted to the format required by MEM using the following command:

```datetime_to_MEM_format.ipynb```

resulting in the reformatted files (e.g. CISO_reformatted.csv).

The capacity factor files were created with [Create Wind and Solar Resource Files](https://github.com/carnegie/Create_Wind_and_Solar_Resource_Files/tree/master).