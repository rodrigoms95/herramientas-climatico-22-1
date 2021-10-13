# Calcula la precipitación en días con
# temperatura mayor a la media anual.

import os

import xarray as xr


path_T = os.getcwd() + "/resultados/CHIRTS/"
path_P = os.getcwd() + "/datos/CHIRPS/"
path_r = os.getcwd() + "/resultados/vars/"

# Variables de CHIRTS/CHIRPS.
vars = ["Tmax", "Tmin", "Tmean",
    "Pre", "Pre_Tmean"]

# Si no existen las carpetas, las crea.
if not os.path.exists(path_r):
    os.mkdir(path_r)
if not os.path.exists(path_r + vars[4]):
    os.mkdir(path_r + vars[4])


years = list(range(1995, 2017))

ds_T = ( xr.open_dataset(path_T + "mexico_Tmean.nc")
        .rename(Tmean = "Pre") )

for j in years:
    # Abrimos la media anual

    with ( xr.open_dataset( path_T + vars[2] + "/mexico_" 
        + vars[2] + "." + str(j) + ".nc" )
        .rename(Tmean = "Pre") ) as ds_mean:
        with xr.open_dataset( path_P + "/mexico_" +
            vars[3] + "." + str(j) + ".nc" ) as ds_pre:
            # Establecemos np.nan como valor sin datos.
            ds_pre = ds_pre.where(ds_pre > -9000)
            # Quitamos los puntos donde la temperatura
            # es menor a la media anual.
            ds_pre = ds_pre.where( ds_mean >
                ds_T.isel(time = j -1995) )
    
        # Guardamos el archivo.
        ds_pre = ds_pre.rename(Pre = vars[4])
        ds_pre.to_netcdf( path_r + vars[4] + "/mexico_" 
        + vars[4] + "." + str(j) + ".nc")
