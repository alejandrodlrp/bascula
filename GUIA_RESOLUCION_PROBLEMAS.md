# Guía de Resolución de Problemas - Sistema de Báscula Académica

## 1. Problemas de Instalación

### 1.1 Error: "pip no reconocido como comando"

**Síntomas:**
```
'pip' no se reconoce como un comando interno o externo
```

**Solución:**
1. Verificar instalación de Python:
   ```bash
   python --version
   python3 --version
   ```
2. Si Python está instalado, usar:
   ```bash
   python -m pip install -r requirements.txt
   ```
3. En Raspberry Pi:
   ```bash
   sudo apt update
   sudo apt install python3-pip
   ```

### 1.2 Error: "ModuleNotFoundError: No module named 'streamlit'"

**Síntomas:**
```
ModuleNotFoundError: No module named 'streamlit'
```

**Solución:**
1. Instalar dependencias:
   ```bash
   pip install streamlit plotly pandas
   ```
2. O usar requirements.txt:
   ```bash
   pip install -r requirements.txt
   ```
3. En Raspberry Pi con permisos:
   ```bash
   sudo pip3 install -r requirements.txt
   ```

### 1.3 Error de permisos en Raspberry Pi

**Síntomas:**
```
Permission denied: '/usr/local/lib/python3.x/site-packages'
```

**Solución:**
1. Usar entorno virtual (recomendado):
   ```bash
   python3 -m venv bascula_env
   source bascula_env/bin/activate
   pip install -r requirements.txt
   ```
2. O instalar con permisos de usuario:
   ```bash
   pip3 install --user -r requirements.txt
   ```

## 2. Problemas de Ejecución

### 2.1 Error: "Address already in use"

**Síntomas:**
```
OSError: [Errno 98] Address already in use
```

**Solución:**
1. Cambiar puerto:
   ```bash
   streamlit run app.py --server.port 8502
   ```
2. Matar proceso existente:
   ```bash
   # Linux/Mac
   lsof -ti:8501 | xargs kill -9
   
   # Windows
   netstat -ano | findstr :8501
   taskkill /PID <PID> /F
   ```

### 2.2 Error: "Database is locked"

**Síntomas:**
```
sqlite3.OperationalError: database is locked
```

**Solución:**
1. Cerrar todas las instancias de la aplicación
2. Eliminar archivo de bloqueo:
   ```bash
   rm bascula_data.db-journal
   ```
3. Reiniciar la aplicación
4. Si persiste, eliminar la base de datos:
   ```bash
   rm bascula_data.db
   ```

### 2.3 Error: "Cannot connect to display"

**Síntomas:**
```
Cannot connect to display :0.0
```

**Solución en Raspberry Pi:**
1. Habilitar X11 forwarding:
   ```bash
   export DISPLAY=:0.0
   ```
2. O ejecutar sin interfaz gráfica:
   ```bash
   streamlit run app.py --server.headless true
   ```

## 3. Problemas de Rendimiento

### 3.1 Aplicación lenta en Raspberry Pi

**Síntomas:**
- Carga lenta de la interfaz
- Gráficas tardan en renderizar

**Solución:**
1. Reducir datos mostrados:
   - Modificar límite en `obtener_mediciones(limit=10)`
2. Deshabilitar auto-refresh:
   - Desmarcar checkbox "Auto-actualizar"
3. Optimizar memoria:
   ```bash
   # Aumentar swap en Raspberry Pi
   sudo dphys-swapfile swapoff
   sudo nano /etc/dphys-swapfile
   # Cambiar CONF_SWAPSIZE=1024
   sudo dphys-swapfile setup
   sudo dphys-swapfile swapon
   ```

### 3.2 Base de datos crece demasiado

**Síntomas:**
- Archivo bascula_data.db muy grande
- Consultas lentas

**Solución:**
1. Limpiar datos antiguos:
   ```python
   # Ejecutar en Python
   import sqlite3
   conn = sqlite3.connect('bascula_data.db')
   cursor = conn.cursor()
   cursor.execute("DELETE FROM mediciones WHERE timestamp < date('now', '-30 days')")
   conn.commit()
   conn.close()
   ```
2. Vacuumar base de datos:
   ```python
   import sqlite3
   conn = sqlite3.connect('bascula_data.db')
   conn.execute("VACUUM")
   conn.close()
   ```

## 4. Problemas de Interfaz

### 4.1 Gráficas no se muestran

**Síntomas:**
- Área en blanco donde debería estar la gráfica
- Error en consola del navegador

**Solución:**
1. Verificar versión de Plotly:
   ```bash
   pip show plotly
   ```
2. Actualizar si es necesario:
   ```bash
   pip install --upgrade plotly
   ```
3. Limpiar caché del navegador
4. Probar en navegador diferente

### 4.2 Tabla no se actualiza

**Síntomas:**
- Datos nuevos no aparecen en tabla
- Tabla muestra datos antiguos

**Solución:**
1. Refrescar página (F5)
2. Verificar conexión a base de datos
3. Reiniciar aplicación Streamlit

### 4.3 Botones no responden

**Síntomas:**
- Clicks no registran
- Interfaz congelada

**Solución:**
1. Verificar JavaScript habilitado
2. Refrescar página
3. Revisar consola del navegador para errores
4. Reiniciar Streamlit

## 5. Problemas de Datos

### 5.1 Datos simulados no realistas

**Síntomas:**
- Pesos fuera de rango esperado
- Productos repetitivos

**Solución:**
1. Modificar rangos en `BasculaSimulator`:
   ```python
   peso = round(random.uniform(21.5, 23.8), 1)  # Ajustar rango
   ```
2. Agregar más productos en `QRSimulator`:
   ```python
   PRODUCTOS = ["Producto1", "Producto2", ...]  # Expandir lista
   ```

### 5.2 Validaciones incorrectas

**Síntomas:**
- Pesos válidos marcados como inválidos
- Margen de error no funciona

**Solución:**
1. Verificar cálculo en `ProcesadorLogica.validar_peso()`:
   ```python
   limite_inferior = peso_minimo * (1 - margen_error / 100)
   limite_superior = peso_minimo * (1 + margen_error / 100)
   ```
2. Revisar parámetro margen_error en sidebar

## 6. Problemas de Red

### 6.1 No se puede acceder desde otra máquina

**Síntomas:**
- Aplicación solo accesible en localhost
- Timeout al conectar desde red

**Solución:**
1. Ejecutar con host específico:
   ```bash
   streamlit run app.py --server.address 0.0.0.0
   ```
2. Verificar firewall:
   ```bash
   # Ubuntu/Raspberry Pi
   sudo ufw allow 8501
   
   # Windows
   # Configurar Windows Firewall para puerto 8501
   ```

### 6.2 Puerto bloqueado

**Síntomas:**
```
Permission denied: bind to port 8501
```

**Solución:**
1. Usar puerto alternativo:
   ```bash
   streamlit run app.py --server.port 8080
   ```
2. En Raspberry Pi con puerto privilegiado:
   ```bash
   sudo streamlit run app.py --server.port 80
   ```

## 7. Herramientas de Diagnóstico

### 7.1 Script de verificación del sistema

Crear archivo `diagnostico.py`:
```python
import sys
import sqlite3
import importlib

def verificar_python():
    print(f"Python version: {sys.version}")
    return sys.version_info >= (3, 7)

def verificar_modulos():
    modulos = ['streamlit', 'plotly', 'pandas', 'sqlite3']
    for modulo in modulos:
        try:
            importlib.import_module(modulo)
            print(f"✓ {modulo} instalado")
        except ImportError:
            print(f"✗ {modulo} NO instalado")
            return False
    return True

def verificar_base_datos():
    try:
        conn = sqlite3.connect('bascula_data.db')
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM mediciones")
        count = cursor.fetchone()[0]
        print(f"✓ Base de datos OK - {count} registros")
        conn.close()
        return True
    except Exception as e:
        print(f"✗ Error en base de datos: {e}")
        return False

if __name__ == "__main__":
    print("=== DIAGNÓSTICO DEL SISTEMA ===")
    verificar_python()
    verificar_modulos()
    verificar_base_datos()
```

### 7.2 Logs de depuración

Para habilitar logs detallados:
```bash
streamlit run app.py --logger.level debug
```

### 7.3 Verificación de recursos

Script para monitorear recursos:
```python
import psutil
import os

def verificar_recursos():
    print(f"CPU: {psutil.cpu_percent()}%")
    print(f"RAM: {psutil.virtual_memory().percent}%")
    print(f"Disco: {psutil.disk_usage('/').percent}%")
    
    # Verificar proceso Streamlit
    for proc in psutil.process_iter(['pid', 'name', 'memory_percent']):
        if 'streamlit' in proc.info['name'].lower():
            print(f"Streamlit PID: {proc.info['pid']}, RAM: {proc.info['memory_percent']:.1f}%")

if __name__ == "__main__":
    verificar_recursos()
```

## 8. Contacto y Soporte

### 8.1 Información del Sistema
Antes de reportar problemas, recopilar:
- Versión de Python: `python --version`
- Sistema operativo: `uname -a` (Linux) o `systeminfo` (Windows)
- Versiones de librerías: `pip list`
- Logs de error completos

### 8.2 Archivos de Log
Ubicaciones comunes:
- **Linux/Mac**: `~/.streamlit/logs/`
- **Windows**: `%USERPROFILE%\.streamlit\logs\`
- **Raspberry Pi**: `/home/pi/.streamlit/logs/`

### 8.3 Pasos para Reportar Problemas
1. Reproducir el error
2. Capturar mensaje de error completo
3. Documentar pasos para reproducir
4. Incluir información del sistema
5. Adjuntar logs relevantes

## 9. Mantenimiento Preventivo

### 9.1 Tareas Regulares
- Limpiar base de datos mensualmente
- Actualizar dependencias trimestralmente
- Verificar espacio en disco semanalmente
- Reiniciar aplicación diariamente en producción

### 9.2 Monitoreo Automático
Script para cron (Linux/Raspberry Pi):
```bash
#!/bin/bash
# Verificar si Streamlit está ejecutándose
if ! pgrep -f "streamlit" > /dev/null; then
    echo "$(date): Streamlit no está ejecutándose, reiniciando..." >> /var/log/bascula.log
    cd /path/to/bascula_Alejo
    nohup streamlit run app.py &
fi
```

Agregar a crontab:
```bash
crontab -e
# Agregar línea:
*/5 * * * * /path/to/monitor_bascula.sh
```

Esta guía cubre los problemas más comunes y sus soluciones. Para problemas específicos no cubiertos aquí, revisar los logs del sistema y la documentación oficial de Streamlit.
