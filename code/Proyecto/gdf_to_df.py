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
gdf = gpd.read_file( path_shp )

# Obtenemos el contorno de los municipios.
gdf["boundary"] = gdf.boundary

# Obtenemos el centroide de los municipios
# y seraparamos su latitud y longitud.
gdf["centroid"] = ( gdf.to_crs("epsg:6372")
    .centroid.to_crs("epsg:4326") )
gdf["lon"] = gdf["centroid"].x
gdf["lat"] = gdf["centroid"].y


# Columnas a retirar del GeoDataFrame.
drop = ["CVEGEO", "CVE_ENT", "CVE_MUN",
    "NOM_MUN", "Area", "PERIMETER", "COV_",
    "COV_ID", "geometry", "boundary", "centroid"]

# Columnas de variables explicativas.
cols = ["T_max", "T_min", "T_mean", "Pre", "HDD_mean",
    "CDD_mean", "HDD_p10", "CDD_p90", "CDD_18",
    "HDD_18", "Pre_T>Tmean", "Población",
    "Densidad_población", "PIB", "PCI", "$luz",
    "$GN", "$GLP"]

# Convertimos de GeoDataGrame a DataFrame. 
df_0 = pd.DataFrame(gdf.drop(drop, axis = 1))
df_0["Municipio"] = df_0.index
df_0["Año"] = 1995
df_0[cols] = np.nan

# Agregamos una fila para cada año en cada municipio.
df = df_0.copy()
for i in range(1996, 2018):
    df_0["Año"] = i
    df = df.append( df_0, ignore_index = True )

df.to_csv(path_r + "data_0.csv", index = False)