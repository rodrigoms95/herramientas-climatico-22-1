# Suma el delta de temperatura obtenido del modelo Access
# con el del los datos medidos del CRU y de WorldClim,
# para el periodo 1970-2000 proyectado a 2020-2040.

import os


import xarray as xr

origen = ["CRU", "WC"]
modelo = "Access"

# Año de inicio y de fin de climatología, inclusive.
with open(os.getcwd() + "/resultados/periodos", "r") as f:
    yr_i = [f.readline()[:-1]]
    yr_f = [f.readline()[:-1]]
    yr_i.append(f.readline()[:-1])
    yr_f.append(f.readline()[:-1])

path_modelo= os.getcwd() + "/resultados/" + modelo + "/"
fname_modelo = (modelo + "_delta_" + yr_i[0] + "_" + yr_f[0]
    + "_" + yr_i[1] + "_" + yr_f[1] + "_monthly.nc")

ds_modelo = (xr.load_dataset(path_modelo + fname_modelo)
    .rename_vars(tas = "T"))

for i in range(0, len(origen)):
    path_real = os.getcwd() + "/resultados/" + origen[i] + "/"
    fname_real = (origen[i] + "_clim_" + yr_i[0]
    + "_" + yr_f[0] + "_monthly.nc")

    with xr.load_dataset(path_real + fname_real) as ds_real:
        # Se suma la climatología real y el delta del modelo.
        ds_delta = ds_real + ds_modelo.interp_like(ds_real)

        # Se guarda el netCDF.
        ds_delta.to_netcdf(
            path_real + origen[i] + "_" + modelo + "_delta_"
            + str(yr_i[0]) + "_" + str(yr_f[0]) + "_"
            + str(yr_i[1]) + "_" + str(yr_f[1])+
            "_monthly.nc"
            )
