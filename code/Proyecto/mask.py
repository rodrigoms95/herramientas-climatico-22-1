# Obtiene una máscara para cada municipio del país.

import os


import rioxarray

import pandas as pd
import numpy as np

import geopandas as gpd
import xarray as xr


vars = ["Tmax", "Tmin", "Tmean", "Pre"]

path_d = [os.getcwd() + "/resultados/CHIRTS/",
    os.getcwd() + "/datos/CHIRPS/"]
path_r = os.getcwd() + "/resultados/Municipios/"
path_shp = os.getcwd() + "/datos/Mapas/Municipios/mun20gw.shp"

# Si no existe la carpeta, la crea.
if not os.path.exists(path_r):
    os.mkdir(path_r)


# Se cargan los municipios.
gdf = gpd.read_file( path_shp )

# Se obtiene el contorno de los municiipios.
gdf["boundary"] = gdf.boundary


# Abrimos el netCDF para el cuál se hará la 
# máscara de acuerdo con su resolución.
ds = xr.open_dataset( path_d + vars[0]
    + "/mexico_" + vars[0] + ".1995.nc" )
# Establecemos np.nan como valor sin datos.
ds = ds.where(ds > -9000)
# Se establece el datum de los datos.
ds = ds.rio.write_crs(gdf.crs)

# Se hace un Dataset con unos para todo el país
mask_0 = xr.ones_like( ds.isel(time = 0)
    .drop(["time", "spatial_ref"])
    .expand_dims(dim = "municipio"),
    dtype = int ).rio.write_crs(gdf.crs)

# La lista que contra los Datasets la 
# máscara para cada municipio.
mask = []

# Se hace la máscara para cada municipio.
for i in range(gdf.shape[0]):
    mask.append( mask_0.rio.clip(
        gdf[gdf.index == i].geometry,
        gdf.crs, drop=False, invert=False) )

# Para los municipios en los que no cae ningún
# punto, se relajan las condiciones para
# considerar cualquier punto que toque.
for i in range(len(mask)):
    if ( mask[i].where(mask[i] > -9000)
        .drop("spatial_ref")
        .to_dataframe().mean()[0] 
        ) != 1:
        
        mask[i] = mask_0.rio.clip(
        gdf[gdf.index == i].geometry,
        gdf.crs, all_touched = True, 
        drop=False, invert=False)

# Se unen las máscaras para todos los municipios.
mask = ( xr.concat(mask, dim = "municipio")
    .drop("spatial_ref")
    .rename(Tmax = "mask") )
mask = mask.where(mask > -9000)
mask.to_netcdf(path_r + "municipios_mask.nc")