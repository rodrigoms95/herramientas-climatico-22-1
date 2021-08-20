# Obtiene el delta de temperatura entre el periodo 1970-2000
# y 2020-2040 con datos del modelo Access.

import os


import xarray as xr

modelo = "Access"

path_d= os.getcwd() + "/datos/" + modelo + "/"
path_r = os.getcwd() + "/resultados/" + modelo + "/"
name = ["tas_Amon_ACCESS1-0_historical_r1i1p1_185001-200512.nc",
    "tas_Amon_ACCESS1-0_rcp85_r1i1p1_200601-210012.nc",
    "hist", "proy", "delta"]

# Si no existe la carpeta, la crea.
if not os.path.exists(path_r):
    os.mkdir(path_r)

# Año de inicio y de fin de climatología, inclusive.
with open(os.getcwd() + "/resultados/periodos", "r") as f:
    yr_i = [f.readline()[:-1]]
    yr_f = [f.readline()[:-1]]
    yr_i.append(f.readline()[:-1])
    yr_f.append(f.readline()[:-1])

ds = []

vars = ["height", "time_bnds", "lat_bnds", "lon_bnds"]

# Se abre el archivo histórico y luego la proyección.
for i in range(0, 2):
    ds.append(xr.load_dataset(
        path_d + name[i]).drop(vars))

    # Se selecciona el periodo deseado.
    ds[i] = ds[i].sel(time = slice(yr_i[i], yr_f[i]))

    # Se obtiene la media mensual.
    ds[i] = ds[i].groupby("time.month").mean()

    # Se ajustan los valores de la longitud para que estén
    # en el rango (-180, 180).
    ds[i]["lon_ajus"] = xr.where(
        ds[i]["lon"] > 180,
        ds[i]["lon"] - 360,
        ds[i]["lon"])

    # Se ajustan los valores de la longitud para que estén
    # en el rango (-180, 180).
    ds[i] = (ds[i]
        .swap_dims(lon = "lon_ajus")
        .sel(lon_ajus = sorted(ds[i].lon_ajus))
        .drop("lon"))
    ds[i] = ds[i].rename(lon_ajus = "lon")

    # Se guarda el netCDF.
    ds[i].to_netcdf(
        path_r + "Access_clim_" + name[i + 2]
        + "_" + str(yr_i[i]) + "_" + str(yr_f[i])
        + "_monthly.nc"
        )

i = 2

# Se calcula el delta restando la climatología
# proyectada y la histórica del modelo.
ds.append(ds[1] - ds[0])

# Se ajustan los valores de la longitud para que estén
# en el rango (-180, 180).
ds[i]["lon_ajus"] = xr.where(
    ds[i]["lon"] > 180,
    ds[i]["lon"] - 360,
    ds[i]["lon"])

# Se reasignan las nuevas dimensiones como las
# principales dimensiones de longitud y se reordenan
# los datos.
ds[i] = (ds[i]
    .swap_dims(lon = "lon_ajus")
    .sel(lon_ajus = sorted(ds[i].lon_ajus))
    .drop("lon"))
ds[i] = ds[i].rename(lon_ajus = "lon")

# Se guarda el netCDF.
ds[i].to_netcdf(
    path_r + modelo + "_" + name[i + 2] + "_"
    + str(yr_i[0]) + "_" + str(yr_f[0]) + "_"
    + str(yr_i[1]) + "_" + str(yr_f[1])+
    "_monthly.nc"
    )
