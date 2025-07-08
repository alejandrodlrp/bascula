#!/bin/bash

echo "========================================"
echo "   Sistema de Báscula Académica"
echo "========================================"
echo ""
echo "Iniciando aplicación..."
echo ""

# Verificar si Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python3 no está instalado"
    echo "Por favor instale Python3:"
    echo "  Ubuntu/Debian: sudo apt install python3 python3-pip"
    echo "  macOS: brew install python"
    exit 1
fi

# Mostrar versión de Python
echo "Python version: $(python3 --version)"

# Verificar si pip está disponible
if ! command -v pip3 &> /dev/null; then
    echo "ERROR: pip3 no está instalado"
    echo "Por favor instale pip3:"
    echo "  Ubuntu/Debian: sudo apt install python3-pip"
    exit 1
fi

# Verificar si las dependencias están instaladas
if ! python3 -c "import streamlit" &> /dev/null; then
    echo "Instalando dependencias..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "ERROR: No se pudieron instalar las dependencias"
        echo "Intente ejecutar: pip3 install --user -r requirements.txt"
        exit 1
    fi
fi

# Verificar que todas las dependencias estén disponibles
echo "Verificando dependencias..."
python3 -c "
import sys
modules = ['streamlit', 'plotly', 'pandas', 'sqlite3']
missing = []
for module in modules:
    try:
        __import__(module)
        print(f'✓ {module}')
    except ImportError:
        missing.append(module)
        print(f'✗ {module}')

if missing:
    print(f'ERROR: Faltan módulos: {missing}')
    sys.exit(1)
else:
    print('✓ Todas las dependencias están instaladas')
"

if [ $? -ne 0 ]; then
    echo "ERROR: Hay problemas con las dependencias"
    exit 1
fi

# Ejecutar la aplicación
echo ""
echo "Ejecutando aplicación..."
echo "La aplicación se abrirá en su navegador web"
echo "Para detener la aplicación, presione Ctrl+C"
echo ""
echo "URL: http://localhost:8501"
echo ""

# Ejecutar Streamlit
streamlit run app.py

echo ""
echo "Aplicación terminada."
