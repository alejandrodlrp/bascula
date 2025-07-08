#!/usr/bin/env python3
"""
Script de diagnóstico para el Sistema de Báscula Académica
Verifica que todos los componentes estén correctamente instalados
"""

import sys
import os
import sqlite3
import importlib
import platform
from datetime import datetime

def print_header():
    """Imprime el encabezado del diagnóstico"""
    print("=" * 60)
    print("   DIAGNÓSTICO DEL SISTEMA DE BÁSCULA ACADÉMICA")
    print("=" * 60)
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Sistema Operativo: {platform.system()} {platform.release()}")
    print(f"Arquitectura: {platform.machine()}")
    print("-" * 60)

def verificar_python():
    """Verifica la versión de Python"""
    print("1. VERIFICACIÓN DE PYTHON")
    print(f"   Versión: {sys.version}")
    print(f"   Ejecutable: {sys.executable}")
    
    if sys.version_info >= (3, 7):
        print("   ✓ Versión de Python compatible (3.7+)")
        return True
    else:
        print("   ✗ Versión de Python incompatible (necesita 3.7+)")
        return False

def verificar_modulos():
    """Verifica que todos los módulos requeridos estén instalados"""
    print("\n2. VERIFICACIÓN DE MÓDULOS")
    
    modulos_requeridos = {
        'streamlit': 'Framework web principal',
        'plotly': 'Gráficas interactivas',
        'pandas': 'Manipulación de datos',
        'sqlite3': 'Base de datos (incluido en Python)',
        'random': 'Generación de números aleatorios (incluido)',
        'datetime': 'Manejo de fechas (incluido)',
        're': 'Expresiones regulares (incluido)'
    }
    
    modulos_ok = True
    
    for modulo, descripcion in modulos_requeridos.items():
        try:
            mod = importlib.import_module(modulo)
            version = getattr(mod, '__version__', 'N/A')
            print(f"   ✓ {modulo:<12} - {descripcion} (v{version})")
        except ImportError:
            print(f"   ✗ {modulo:<12} - {descripcion} (NO INSTALADO)")
            modulos_ok = False
        except Exception as e:
            print(f"   ⚠ {modulo:<12} - {descripcion} (ERROR: {e})")
            modulos_ok = False
    
    return modulos_ok

def verificar_archivos():
    """Verifica que todos los archivos necesarios estén presentes"""
    print("\n3. VERIFICACIÓN DE ARCHIVOS")
    
    archivos_requeridos = {
        'app.py': 'Aplicación principal',
        'requirements.txt': 'Lista de dependencias',
        'README.md': 'Documentación principal',
        'ARQUITECTURA.md': 'Documentación de arquitectura',
        'GUIA_INSTALACION.md': 'Guía de instalación',
        'GUIA_RESOLUCION_PROBLEMAS.md': 'Guía de troubleshooting'
    }
    
    archivos_ok = True
    
    for archivo, descripcion in archivos_requeridos.items():
        if os.path.exists(archivo):
            size = os.path.getsize(archivo)
            print(f"   ✓ {archivo:<30} - {descripcion} ({size} bytes)")
        else:
            print(f"   ✗ {archivo:<30} - {descripcion} (NO ENCONTRADO)")
            archivos_ok = False
    
    return archivos_ok

def verificar_base_datos():
    """Verifica la funcionalidad de SQLite"""
    print("\n4. VERIFICACIÓN DE BASE DE DATOS")
    
    try:
        # Crear conexión de prueba en memoria
        conn = sqlite3.connect(':memory:')
        cursor = conn.cursor()
        
        # Crear tabla de prueba
        cursor.execute('''
            CREATE TABLE test_table (
                id INTEGER PRIMARY KEY,
                nombre TEXT,
                valor REAL
            )
        ''')
        
        # Insertar datos de prueba
        cursor.execute("INSERT INTO test_table (nombre, valor) VALUES (?, ?)", 
                      ("test", 123.45))
        
        # Consultar datos
        cursor.execute("SELECT * FROM test_table")
        resultado = cursor.fetchone()
        
        conn.close()
        
        if resultado:
            print("   ✓ SQLite funcionando correctamente")
            print(f"   ✓ Datos de prueba: {resultado}")
            return True
        else:
            print("   ✗ Error en consulta de datos")
            return False
            
    except Exception as e:
        print(f"   ✗ Error en SQLite: {e}")
        return False

def verificar_permisos():
    """Verifica permisos de escritura en el directorio actual"""
    print("\n5. VERIFICACIÓN DE PERMISOS")
    
    try:
        # Intentar crear archivo de prueba
        test_file = 'test_permisos.tmp'
        with open(test_file, 'w') as f:
            f.write("test")
        
        # Intentar leer el archivo
        with open(test_file, 'r') as f:
            content = f.read()
        
        # Eliminar archivo de prueba
        os.remove(test_file)
        
        if content == "test":
            print("   ✓ Permisos de lectura/escritura correctos")
            return True
        else:
            print("   ✗ Error en permisos de lectura")
            return False
            
    except Exception as e:
        print(f"   ✗ Error de permisos: {e}")
        return False

def verificar_red():
    """Verifica conectividad de red (opcional)"""
    print("\n6. VERIFICACIÓN DE RED")
    
    try:
        import urllib.request
        
        # Intentar conectar a un sitio web
        urllib.request.urlopen('https://www.google.com', timeout=5)
        print("   ✓ Conectividad a internet disponible")
        return True
        
    except Exception as e:
        print(f"   ⚠ Sin conectividad a internet: {e}")
        print("   ℹ La aplicación puede funcionar sin internet")
        return True  # No es crítico

def generar_reporte():
    """Genera un reporte de diagnóstico"""
    print("\n7. GENERANDO REPORTE")
    
    try:
        reporte = f"""
REPORTE DE DIAGNÓSTICO - SISTEMA DE BÁSCULA ACADÉMICA
=====================================================
Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Sistema: {platform.system()} {platform.release()}
Python: {sys.version}
Directorio: {os.getcwd()}

ESTADO DE COMPONENTES:
- Python: {'✓' if sys.version_info >= (3, 7) else '✗'}
- Módulos: Verificar salida anterior
- Archivos: Verificar salida anterior
- Base de datos: Verificar salida anterior
- Permisos: Verificar salida anterior

RECOMENDACIONES:
- Si hay módulos faltantes, ejecutar: pip install -r requirements.txt
- Si hay errores de permisos, verificar ubicación del proyecto
- Para soporte, consultar GUIA_RESOLUCION_PROBLEMAS.md
"""
        
        with open('diagnostico_reporte.txt', 'w', encoding='utf-8') as f:
            f.write(reporte)
        
        print("   ✓ Reporte guardado en 'diagnostico_reporte.txt'")
        return True
        
    except Exception as e:
        print(f"   ✗ Error generando reporte: {e}")
        return False

def main():
    """Función principal del diagnóstico"""
    print_header()
    
    # Ejecutar todas las verificaciones
    resultados = []
    resultados.append(verificar_python())
    resultados.append(verificar_modulos())
    resultados.append(verificar_archivos())
    resultados.append(verificar_base_datos())
    resultados.append(verificar_permisos())
    resultados.append(verificar_red())
    
    # Generar reporte
    generar_reporte()
    
    # Resumen final
    print("\n" + "=" * 60)
    print("   RESUMEN DEL DIAGNÓSTICO")
    print("=" * 60)
    
    exitosos = sum(resultados)
    total = len(resultados)
    
    if exitosos == total:
        print("🎉 ¡DIAGNÓSTICO EXITOSO!")
        print("   Todos los componentes están funcionando correctamente.")
        print("   Puede ejecutar la aplicación con: streamlit run app.py")
    elif exitosos >= total - 1:
        print("⚠️  DIAGNÓSTICO CON ADVERTENCIAS")
        print("   La mayoría de componentes están funcionando.")
        print("   Revisar los elementos marcados con ✗ arriba.")
    else:
        print("❌ DIAGNÓSTICO FALLIDO")
        print("   Hay problemas críticos que deben resolverse.")
        print("   Consultar GUIA_RESOLUCION_PROBLEMAS.md")
    
    print(f"\nResultado: {exitosos}/{total} verificaciones exitosas")
    print("=" * 60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nDiagnóstico interrumpido por el usuario.")
    except Exception as e:
        print(f"\nError inesperado durante el diagnóstico: {e}")
        print("Por favor reporte este error.")
