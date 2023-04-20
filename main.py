# x-ray data by
# https://data.ngdc.noaa.gov/platforms/solar-space-observing-satellites/goes/goes16/l2/data/xrsf-l2-avg1m_science/

import netCDF4
import pandas as pd
import glob
import numpy as np
import numpy.ma as ma

# solar flare
flare_class = [-7, -6, -5, -4]
paths = glob.glob("data/*.nc")
pickup_variable = ["time", "xrsa_flux", "class"]

df_all = pd.DataFrame(index=[], columns=pickup_variable)

for path in paths:
    day_data = netCDF4.Dataset(path, "r")
    # print(day_data.variables.keys())
    
    index = {}
    index["time"] = day_data["time"][0]
    index["xrsa_flux"] = max(day_data["xrsa_flux"])
    if type(index["xrsa_flux"]) == ma.core.MaskedConstant:
        continue

    index["class"] = len(flare_class)
    for i, c in enumerate(flare_class):
        if index["xrsa_flux"] < 10**c:
            index["class"] = i
            break
    df_all = pd.concat([df_all, pd.DataFrame([index])], ignore_index=True)

print(df_all)
df_all.to_csv("result/xraydata.csv")


