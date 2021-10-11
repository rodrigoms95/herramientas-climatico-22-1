# Renombra los archivos de CHIRPS.

import os

path = os.getcwd() + "/datos/CHIRPS/"
files = os.listdir(path)

for i in files:
    os.rename(path + i, path + i[:7] + "Pre" + i[18:23] + i[-3:])
