# Calcula la temperatura media anual.

import os

import numpy as np

import xarray as xr


path_d = os.getcwd() + "/resultados/CHIRTS/"

# Variables de CHIRTS.
vars = ["Tmax", "Tmin", "Tmean"]

# Si no existe la carpeta, la crea.
if not os.path.exists(path_d):
    os.mkdir(path_d)


# Creamos un Dataset sobre el que concatenaremos
# las temperaturas medias anuales.
with xr.open_dataset( path_d + vars[0] + "/mexico_" 
    + vars[0] + ".1995.nc" ) as ds_max:
    # Creamos un Dataset con las dimensiones
    # adecuadas y un solo tiempo.
    Tmean = xr.ones_like(
        ds_max.mean(dim = "time")
        .assign_coords({"time": np.datetime64("1994")} )
        ).rename_vars(Tmax = vars[2])
    Tmax = Tmean.copy()
    Tmin = Tmean.copy()
    T = [Tmean, Tmax, Tmin]


# Calculamos la temperatura media anual.
for j in range(1995, 2017):
    # Si no existe la carpeta, la crea.
    if not os.path.exists(path_d + vars[2]):
        os.mkdir(path_d + vars[2])
    
    # Abrimos la temperatura máxima.
    with xr.open_dataset( path_d + vars[0] + "/mexico_" 
        + vars[0] + "." + str(j) + ".nc" ) as ds_max:
        # Establecemos np.nan como valor sin datos.
        ds_max = ds_max.where(ds_max > -9000)
        with xr.open_dataset( path_d + vars[1] + "/mexico_" 
            + vars[1] + "." + str(j) + ".nc" ) as ds_min:
            ds_min = ds_min.where(ds_min > -9000)
        
        ds_mean = ( ( ( ds_max + (ds_min
            .rename_vars(Tmin = vars[0])) ) / 2 )
            .rename_vars(Tmax = vars[2]) )

        # Concatenamos las temperaturas.
        for i in T:
            i = xr.concat( [i, ( ds_mean
                .mean(dim = "time")
                .assign_coords({"time": np.datetime64(str(j))} )
                ) ], dim = "time" )
    
# Eliminamos el primer valor de tiempo,
# que solo sirvió como base para concatenar
# y obtenemos el promedio temporal.
for i in range(len(T)):
    T[i] = T[i].drop_sel(time = "1994")
    T[i] = T[i].mean(dim = "time")
    # Guardamos el archivo.
    T[i].to_netcdf(path_d + "mexico_" + vars[i] + ".nc")
