@echo off
echo ========================================
echo   Sistema de Bascula Academica
echo ========================================
echo.
echo Iniciando aplicacion...
echo.

REM Verificar si Python esta instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python no esta instalado o no esta en el PATH
    echo Por favor instale Python desde https://python.org
    pause
    exit /b 1
)

REM Verificar si las dependencias estan instaladas
python -c "import streamlit" >nul 2>&1
if %errorlevel% neq 0 (
    echo Instalando dependencias...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo ERROR: No se pudieron instalar las dependencias
        pause
        exit /b 1
    )
)

REM Ejecutar la aplicacion
echo Ejecutando aplicacion...
echo La aplicacion se abrira en su navegador web
echo Para detener la aplicacion, presione Ctrl+C
echo.
streamlit run app.py

pause
