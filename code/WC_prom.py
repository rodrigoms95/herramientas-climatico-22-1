import os

import numpy as np
import xarray as xr


fdir_d = os.getcwd() + "/datos/WC_nc/"
fdir_r = os.getcwd() + "/resultados/WC_nc/"

# Se enlistan las subcarpetas de WC_nc.
dir_a = os.listdir(fdir_d)

dir_b = []

# Año de inicio y de fin de climatología, inclusive.
yr_i = 1970
yr_f = 2000

# Se enlistan los archivos de cada subcarpeta de WC_nc.
for i in range(0 , len(dir_a)):
    dir_b.append(os.listdir(fdir_d + dir_a[i]))
    # Se seleccionan los años escogidos.
    dir_b[i] = dir_b[i][((yr_i - 1961) * 12) : ((yr_f + 1 - 1961) * 12)]

# Se obtiene el promedio mensual para cada conjunto de datos.
for i, value in enumerate(dir_a):
    ds_time = []

    # Se itera sobre los archivos de la subcarpeta de WC_nc en turno.
    for j in range(0, len(dir_b[i])):
        # Se abre el netCDF y se agrega a una lista.
        ds_time.append(
            xr.load_dataset(fdir_d + dir_a[i] + "/" + dir_b[i][j]))
        # Se agrega la dimensión temporal con la fecha dada en el
        # nombre del archivo.
        ds_time[j] = ds_time[j].expand_dims(
            time =  [np.datetime64(
            ds_time[j]["crs"].encoding["source"][-10:-3], "ns")])

    # Se concatenan todos los netCDF.
    ds = xr.combine_nested(ds_time, concat_dim = "time")
    # Se obtiene la media mensual.
    ds = ds.groupby("time.month").mean()
    # Se guarda el netCDF.
    ds.to_netcdf(fdir_r + dir_a[i] + "_" + str(yr_i)
        + "_" + str(yr_f) + "_monthly.nc")


# Otra posibilidad, revisar implementación.
# Debería ser más rápido.

#def pre(ds):
#    ds = ds.expand_dims(
#        time =  [np.datetime64(ds["prec"].encoding["source"][-10:-3], "ns")]
#        )

#Prec_xr = xr.open_mfdataset(
#    fdir + WC[0] + "\*.nc", combine = "nested", concat_dim = "time",
#    parallel = True, preprocess = pre)

#Prec_xr
