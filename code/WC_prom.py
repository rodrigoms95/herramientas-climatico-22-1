# Obtiene la temperatura promedio mensual en el periodo
# 1970-2000 con datos de WorldClim.

import os

import numpy as np
import xarray as xr

origen = "WC"

path_d = os.getcwd() + "/datos/" + origen + "/"
path_r = os.getcwd() + "/resultados/" + origen + "/"

# Se enlistan las subcarpetas de WC.
fdir = os.listdir(path_d)

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

# Se obtiene el promedio mensual para cada conjunto de datos.
for value in fdir: 
    # Se cargan y concatenan todos los archivos correspondientes
    # para cada subcarpeta de WC.
    with xr.open_mfdataset(
        path_d + value + "\*.nc", combine = "nested",
        concat_dim = "time", parallel = True, preprocess = pre
        ) as ds:

        # Se selecciona el periodo deseado.
        ds = ds.sel(time = slice(yr_i, yr_f))

        # Se obtiene la media mensual.
        ds = ds.groupby("time.month").mean()

        # Se guarda el netCDF.
        ds.to_netcdf(path_r + value + "_" + str(yr_i)
            + "_" + str(yr_f) + "_monthly.nc")