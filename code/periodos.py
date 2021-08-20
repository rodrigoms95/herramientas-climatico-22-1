# Registra los periodos para estudio de la climatología y proyección.

import os
import sys

# Año de inicio y de fin de climatología, inclusive.
yr_i = [sys.argv[1], sys.argv[3]]
yr_f = [sys.argv[2], sys.argv[4]]

yr = [yr_i[0] + "\n", yr_f[0] + "\n", yr_i[1] + "\n", yr_f[1] + "\n"]

with open(os.getcwd() + "/resultados/periodos", "w") as f:
    f.writelines(yr)