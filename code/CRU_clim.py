# Obtiene la climatología media para 1970-2000 a partir de
# datos del CRU y de WorldClim.

import os


import xarray as xr

origen = "CRU"

# Año de inicio y de fin de climatología, inclusive.
with open(os.getcwd() + "/resultados/periodos", "r") as f:
    yr_i = f.readline()[:-1]
    yr_f = f.readline()[:-1]

# Nombre de variables en cada conjunto de archivos.
var = ["tmx", "tmn", "pre"]

ds = []
    
path_d = os.getcwd() + "/datos/" + origen + "/"
path_r = os.getcwd() + "/resultados/" + origen + "/"

# Formato del nombre de los archivos.
name = "cru_ts4.03.1901.2018."
fname = []

# Si no existe la carpeta, la crea.
if not os.path.exists(path_r):
    os.mkdir(path_r)

# Se obtiene el promedio mensual para cada conjunto de datos.
for i in range(0, len(var)): 
    # Nombre del archivo.
    fname.append(name + var[i] + ".dat.nc")

    # Se cargan y concatenan todos los archivos correspondientes
    # para cada subcarpeta de WC_nc.
    ds.append(xr.load_dataset(path_d + fname[i]).drop("stn"))

    # Se selecciona el periodo deseado.
    ds[i] = ds[i].sel(time = slice(yr_i, yr_f))

    # Se hace que las variables sean compatibles.
    ds[i] = ds[i].rename_vars({var[i]: "T"})
    # Se agrega una dimensión para poder concatenar los archivos.
    ds[i] = ds[i].expand_dims(num =  [i])

# Se concatenan los archivos.
ds_conc = xr.combine_nested(ds[0:2], concat_dim = "num")
# Se promedia la temperatura maxima y mínima.
ds_conc = ds_conc.mean("num")

# Se obtiene la media mensual.
ds_conc = ds_conc.groupby("time.month").mean()

# Se guardan los netCDF.
ds[-1].to_netcdf(path_r + origen + "_" + var[-1] + "_" + str(yr_i)
    + "_" + str(yr_f) + "_monthly.nc")
ds_conc.to_netcdf(path_r + origen + "_clim_" + str(yr_i)
    + "_" + str(yr_f) + "_monthly.nc")
