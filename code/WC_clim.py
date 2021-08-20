# Obtiene la climatología media para 1970-2000 a partir de
# datos de WorldClim.

import os

import numpy as np
import xarray as xr

origen = "WC"

path_d = os.getcwd() + "/datos/" + origen + "/"
path_r = os.getcwd() + "/resultados/" + origen + "/"

# Se enlistan las subcarpetas de WC_nc.
WC_nc = os.listdir(path_d)

# Año de inicio y de fin de climatología, inclusive.
with open(os.getcwd() + "/resultados/periodos", "r") as f:
    yr_i = f.readline()[:-1]
    yr_f = f.readline()[:-1]

# Si no existe la carpeta, la crea.
if not os.path.exists(path_r):
    os.mkdir(path_r)

# Preprocesamiento de cada archivo, donde se agrega la dimensión
# temporal de acuerdo al nombre del archivo.
def pre(ds):
    ds = ds.expand_dims(time =  [np.datetime64(
        ds["crs"].encoding["source"][-10:-3], "ns")])
    return ds

ds = []
var = ["tmax", "tmin"]

# Se obtiene el promedio mensual para cada conjunto de datos.
for i, value in enumerate(WC_nc[1:]): 
    # Se cargan y concatenan todos los archivos correspondientes
    # para cada subcarpeta de WC_nc.
    ds.append(xr.open_mfdataset(
        path_d + value + "\*.nc", combine = "nested",
        concat_dim = "time", parallel = True, preprocess = pre
        ))

    # Se selecciona el periodo deseado.
    ds[i] = ds[i].sel(time = slice(yr_i, yr_f))

    ds[i] = ds[i].rename_vars({var[i]: "T"})
    # Se agrega una dimensión para poder concatenar los archivos.
    ds[i] = ds[i].expand_dims(num =  [i])

# Se concatenan los archivos.
ds_conc = xr.combine_nested(ds, concat_dim = "num")
# Se promedia la temperatura maxima y mínima.
ds_conc = ds_conc.mean("num")

# Se obtiene la media mensual.
ds_conc = ds_conc.groupby("time.month").mean()

# Se guarda el netCDF.
ds_conc.to_netcdf(path_r + origen + "_clim_" + str(yr_i)
    + "_" + str(yr_f) + "_monthly.nc")
