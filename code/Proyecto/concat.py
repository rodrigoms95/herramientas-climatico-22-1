# Concatenación de GeoTIFFs de CHIRTS
# por año y conversión a NetCDF.

import os

import numpy as np
import xarray as xr


vars = ["Tmax", "Tmin"]

path_d = os.getcwd() + "/datos/CHIRTS/"
path_r = os.getcwd() + "/resultados/CHIRTS/"

# Si no existe la carpeta, la crea.
if not os.path.exists(path_r):
        os.mkdir(path_r)
for T in vars:
    if not os.path.exists(path_r + T):
        os.mkdir(path_r + T)


# Preprocesamiento de cada archivo, donde se agrega la
# dimensión temporal de acuerdo al nombre del archivo.

var = "Band1"
Range = [-17, -7]

def pre(ds):
    ds = ( ds.expand_dims(time =  [np.datetime64(
        ( ds[var].encoding["source"]
        [Range[0]:Range[1]].replace(".", "-")
        ), "ns") ] )
       .rename_vars({"Band1": "Tmax"} ) )
    return ds

# Se obtiene el promedio mensual para cada conjunto de datos.
for T in vars:
    # Se enlistan los años que se tienen para cada variable.
    files = os.listdir(path_d + T)

    for i, value in enumerate(files[0:]): 
        # Se cargan y concatenan todos los archivos correspondientes
        # para cada subcarpeta de año y cada variable.
        ds = xr.open_mfdataset(
            path_d + T + "/" + str(value) + "/*.nc",
            combine = "nested", concat_dim = "time",
            parallel = True, preprocess = pre
            )
        # Se guarda el archivo en formato NetCDF.
        ds.to_netcdf(path_r + T + "/"
            + "mexico_" + T + "." + str(value) + ".nc")
