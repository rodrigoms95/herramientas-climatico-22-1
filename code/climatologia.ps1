# Corre toda la lista de programas para generar una climatología proyectada.

$DIR = Get-Location

conda activate gv

$yr_i_0 = "1970"
$yr_f_0 = "2000"
$yr_i_1 = "2020"
$yr_f_1 = "2040"

echo "Calculo de climatologias proyectadas"
echo "Autor: Rodrigo Munoz"

echo ""
echo "definiendo periodos..."
python "$DIR/code/periodos.py" $yr_i_0 $yr_f_0 $yr_i_1 $yr_f_1

echo ""
echo "calculando climatologia del CRU..."
python "$DIR/code/CRU_clim.py"

echo ""
echo "calculando promedios de WC..."
python "$DIR/code/WC_prom.py"

echo ""
echo "calculando climatologia de WC..."
python "$DIR/code/WC_clim.py"

echo ""
echo "Calculando delta a partir de Access..."
python "$DIR/code/Access_delta.py"

echo ""
echo "Calculando climatologia proyectada..."
python "$DIR/code/proyeccion_Access_delta.py"

echo ""
echo "Proceso terminado."
echo ""
