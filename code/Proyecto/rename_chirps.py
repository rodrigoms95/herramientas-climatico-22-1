# Renombra los archivos de CHIRPS.

import os
import xarray as xr

path = os.getcwd() + "/datos/CHIRPS/"
path_mask = ( os.getcwd() +
    "/resultados/Municipios/municipios_mask.nc" )
files = os.listdir(path)

# Cargamos la máscara para alinear los archivos.
mask = ( xr.open_dataset(path_mask)
    .isel(municipio = 0).rename(mask = "Pre") )

for i in files:
    with xr.open_dataset(path + i) as ds:
        # Renombrar variables.
        ds = ds.rename({"latitude": "lat",
            "longitude": "lon", "precip": "Pre"})
        # Alinear con mask.
        ds = ds.interp_like(mask)
        # Guardar y renombrar archivos.
        ds.to_netcdf( path + i[:7] + "Pre"
            + i[18:23] + i[-3:] )
    os.remove(path + i)
