# Guarda la información de cada municipio en un DataFrame.

import os

import pandas as pd
import numpy as np

import geopandas as gpd


path_r = os.getcwd() + "/resultados/RandomTree/data/"
path_shp = os.getcwd() + "/datos/Mapas/Municipios/mun20gw.shp"

# Si no existe la carpeta, la crea.
if not os.path.exists(path_r):
    os.mkdir(path_r)

# Cargamos los municipios.
gdf = gpd.read_file(path_shp, encoding='utf8')

# Obtenemos el contorno de los municipios.
gdf["boundary"] = gdf.boundary

# Obtenemos el centroide de los municipios
# y seraparamos su latitud y longitud.
gdf["centroid"] = ( gdf.to_crs("epsg:6372")
    .centroid.to_crs("epsg:4326") )
gdf["lon"] = gdf["centroid"].x
gdf["lat"] = gdf["centroid"].y


# Columnas a retirar del GeoDataFrame.
drop = ["CVEGEO", "PERIMETER", "COV_",
    "COV_ID", "geometry", "boundary", "centroid"]

# Columnas de variables explicativas.
cols = ["Consumo_1", "Usuarios_1", "Consumo_DAC",
    "Usuarios_DAC", "T_max", "T_min", "T_mean",
    "HDD_mean", "CDD_mean", "HDD_p10", "CDD_p90",
    "Pre", "Pre_Tmean", "Densidad_población",
    "PCI", "$luz", "$GLP", "Población", "PIB"]

# Convertimos de GeoDataFrame a DataFrame. 
df_0 = pd.DataFrame(gdf.drop(drop, axis = 1))
df_0["Año"] = 2010
df_0[cols] = np.nan

# Agregamos una fila para cada año en cada municipio.
df = df_0.copy()
for i in range(2011, 2017):
    df_0["Año"] = i
    df = df.append( df_0, ignore_index = True )
df = df[ list(df.columns[0:4]) + cols[0:4]
    + list(df.columns[5:7]) + cols[4:-2]
    + cols[-2:] + list(df.columns[7:8])
    + list(df.columns[4:5]) ]

df.to_csv(path_r + "data_0.csv",
    index = False, encoding = 'utf8')