@echo off
setlocal
title Calculadora de Equacoes do 2o Grau
cd /d "%~dp0"

if not exist "main.py" goto arquivos_ausentes
if not exist "requirements.txt" goto arquivos_ausentes
if exist ".venv\Scripts\python.exe" goto preparar

echo Preparando o ambiente da calculadora...
py -3 -c "import sys; sys.exit(sys.version_info < (3, 10))" >nul 2>&1
if not errorlevel 1 (
    py -3 -m venv ".venv"
    if errorlevel 1 goto erro
    goto preparar
)
python -c "import sys; sys.exit(sys.version_info < (3, 10))" >nul 2>&1
if errorlevel 1 (
    echo Instale Python 3.10 ou superior com Tcl/Tk e a opcao Add Python to PATH.
    echo Download: https://www.python.org/downloads/
    goto erro
)
python -m venv ".venv"
if errorlevel 1 goto erro

:preparar
".venv\Scripts\python.exe" -c "import sys; sys.exit(sys.version_info < (3, 10))" >nul 2>&1
if errorlevel 1 (
    echo O ambiente .venv esta invalido ou usa um Python antigo.
    echo Renomeie a pasta .venv e execute este arquivo novamente.
    goto erro
)
".venv\Scripts\python.exe" -c "import tkinter, numpy; from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg" >nul 2>&1
if errorlevel 1 (
    echo Instalando dependencias. A primeira execucao precisa de internet...
    ".venv\Scripts\python.exe" -m pip install -r "requirements.txt"
    if errorlevel 1 goto erro
)

".venv\Scripts\python.exe" "main.py" %*
if errorlevel 1 goto erro
exit /b 0

:arquivos_ausentes
echo Extraia TODO o ZIP em uma pasta antes de abrir este arquivo.

:erro
echo.
echo Nao foi possivel iniciar. Confira a mensagem acima.
echo Para reparar as bibliotecas: .venv\Scripts\python.exe -m pip install -r requirements.txt
pause
exit /b 1

