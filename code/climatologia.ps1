# Corre toda la lista de programas para generar una climatología proyectada.

$DIR = Get-Location

conda activate gv

$yr_i_0 = "1970"
$yr_f_0 = "2000"
$yr_i_1 = "2020"
$yr_f_1 = "2040"

Write-Output "Calculo de climatologias proyectadas"
Write-Output "Autor: Rodrigo Munoz"

Write-Output ""
Write-Output "definiendo periodos..."
python "$DIR/code/periodos.py" $yr_i_0 $yr_f_0 $yr_i_1 $yr_f_1

Write-Output ""
Write-Output "calculando climatologia del CRU..."
python "$DIR/code/CRU_clim.py"

Write-Output ""
Write-Output "calculando promedios de WC..."
python "$DIR/code/WC_prom.py"

Write-Output ""
Write-Output "calculando climatologia de WC..."
python "$DIR/code/WC_clim.py"

Write-Output ""
Write-Output "Calculando delta a partir de Access..."
python "$DIR/code/Access_delta.py"

Write-Output ""
Write-Output "Calculando climatologia proyectada..."
python "$DIR/code/proyeccion_Access_delta.py"

Write-Output ""
Write-Output "Proceso terminado."
Write-Output ""
