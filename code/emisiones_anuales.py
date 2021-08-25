import os


import pandas as pd

path_d = os.getcwd() + "/datos/our_world_in_data/"
path_r = os.getcwd() + "/resultados/our_world_in_data/"
name = "annual-co2-emissions-"
fname_d = name + "per-country_2019.csv"
fname_r = name + "world_2019.csv"

df = pd.read_csv(path_d + fname_d)

df = df[df["Entity"] == "World"].drop(["Entity", "Code"], axis = 1)
df = df.set_index("Year")

# Si no existe la carpeta, la crea.
if not os.path.exists(path_r):
    os.mkdir(path_r)

df.to_csv(path_r + fname_r)