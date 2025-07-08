# Guía de Instalación - Sistema de Báscula Académica

## 1. Requisitos del Sistema

### 1.1 Requisitos Mínimos

#### Para PC/Laptop:
- **Sistema Operativo**: Windows 10+, macOS 10.14+, o Linux Ubuntu 18.04+
- **RAM**: 4GB mínimo (8GB recomendado)
- **Espacio en Disco**: 1GB libre
- **Python**: Versión 3.7 o superior
- **Navegador Web**: Chrome, Firefox, Safari, o Edge (versiones recientes)

#### Para Raspberry Pi:
- **Modelo**: Raspberry Pi 3B+ o superior (Raspberry Pi 4 recomendado)
- **RAM**: 2GB mínimo (4GB recomendado)
- **Sistema Operativo**: Raspberry Pi OS (32-bit o 64-bit)
- **Espacio en Disco**: 2GB libre en tarjeta SD
- **Python**: Versión 3.7+ (incluido en Raspberry Pi OS)

### 1.2 Conexión a Internet
- Requerida para la instalación inicial de dependencias
- Opcional para el funcionamiento de la aplicación (funciona offline)

## 2. Instalación en Windows

### 2.1 Verificar Python

1. Abrir **Símbolo del sistema** (cmd) o **PowerShell**
2. Verificar instalación de Python:
   ```cmd
   python --version
   ```
   o
   ```cmd
   python3 --version
   ```

3. Si Python no está instalado:
   - Descargar desde [python.org](https://www.python.org/downloads/)
   - Durante la instalación, marcar "Add Python to PATH"
   - Reiniciar el sistema después de la instalación

### 2.2 Descargar la Aplicación

1. Descargar los archivos del sistema:
   - `app.py`
   - `requirements.txt`
   - Documentación (opcional)

2. Crear una carpeta para el proyecto:
   ```cmd
   mkdir C:\bascula_academica
   cd C:\bascula_academica
   ```

3. Colocar todos los archivos en esta carpeta

### 2.3 Instalar Dependencias

1. Abrir **Símbolo del sistema** como administrador
2. Navegar a la carpeta del proyecto:
   ```cmd
   cd C:\bascula_academica
   ```

3. Instalar las librerías requeridas:
   ```cmd
   pip install -r requirements.txt
   ```

   Si hay problemas con pip, usar:
   ```cmd
   python -m pip install -r requirements.txt
   ```

### 2.4 Ejecutar la Aplicación

1. En el símbolo del sistema:
   ```cmd
   streamlit run app.py
   ```

2. La aplicación se abrirá automáticamente en el navegador
3. Si no se abre automáticamente, ir a: `http://localhost:8501`

## 3. Instalación en macOS

### 3.1 Verificar Python

1. Abrir **Terminal**
2. Verificar Python:
   ```bash
   python3 --version
   ```

3. Si Python no está instalado:
   - Instalar Homebrew (si no está instalado):
     ```bash
     /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
     ```
   - Instalar Python:
     ```bash
     brew install python
     ```

### 3.2 Instalar la Aplicación

1. Crear directorio:
   ```bash
   mkdir ~/bascula_academica
   cd ~/bascula_academica
   ```

2. Colocar archivos en el directorio

3. Instalar dependencias:
   ```bash
   pip3 install -r requirements.txt
   ```

4. Ejecutar aplicación:
   ```bash
   streamlit run app.py
   ```

## 4. Instalación en Linux (Ubuntu/Debian)

### 4.1 Actualizar Sistema

```bash
sudo apt update
sudo apt upgrade -y
```

### 4.2 Instalar Python y pip

```bash
sudo apt install python3 python3-pip python3-venv -y
```

### 4.3 Crear Entorno Virtual (Recomendado)

```bash
mkdir ~/bascula_academica
cd ~/bascula_academica
python3 -m venv bascula_env
source bascula_env/bin/activate
```

### 4.4 Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 4.5 Ejecutar Aplicación

```bash
streamlit run app.py
```

## 5. Instalación en Raspberry Pi

### 5.1 Preparar Raspberry Pi

1. **Instalar Raspberry Pi OS**:
   - Descargar Raspberry Pi Imager
   - Flashear imagen en tarjeta SD
   - Configurar SSH y WiFi si es necesario

2. **Actualizar sistema**:
   ```bash
   sudo apt update
   sudo apt upgrade -y
   ```

### 5.2 Instalar Dependencias del Sistema

```bash
sudo apt install python3-pip python3-venv git -y
```

### 5.3 Crear Proyecto

```bash
mkdir ~/bascula_academica
cd ~/bascula_academica
```

### 5.4 Crear Entorno Virtual

```bash
python3 -m venv bascula_env
source bascula_env/bin/activate
```

### 5.5 Instalar Librerías Python

```bash
pip install -r requirements.txt
```

**Nota**: En Raspberry Pi, la instalación puede tomar varios minutos.

### 5.6 Configurar Inicio Automático (Opcional)

1. Crear script de inicio:
   ```bash
   nano ~/start_bascula.sh
   ```

2. Contenido del script:
   ```bash
   #!/bin/bash
   cd ~/bascula_academica
   source bascula_env/bin/activate
   streamlit run app.py --server.address 0.0.0.0 --server.port 8501
   ```

3. Hacer ejecutable:
   ```bash
   chmod +x ~/start_bascula.sh
   ```

4. Agregar a crontab para inicio automático:
   ```bash
   crontab -e
   ```
   
   Agregar línea:
   ```
   @reboot /home/pi/start_bascula.sh
   ```

## 6. Verificación de Instalación

### 6.1 Script de Diagnóstico

Crear archivo `test_instalacion.py`:

```python
import sys
import importlib

def test_python():
    print(f"Python version: {sys.version}")
    if sys.version_info >= (3, 7):
        print("✓ Python version OK")
        return True
    else:
        print("✗ Python version too old (need 3.7+)")
        return False

def test_modules():
    modules = ['streamlit', 'plotly', 'pandas', 'sqlite3']
    all_ok = True
    
    for module in modules:
        try:
            importlib.import_module(module)
            print(f"✓ {module} installed")
        except ImportError:
            print(f"✗ {module} NOT installed")
            all_ok = False
    
    return all_ok

def test_database():
    try:
        import sqlite3
        conn = sqlite3.connect(':memory:')
        conn.execute('CREATE TABLE test (id INTEGER)')
        conn.close()
        print("✓ SQLite working")
        return True
    except Exception as e:
        print(f"✗ SQLite error: {e}")
        return False

if __name__ == "__main__":
    print("=== VERIFICACIÓN DE INSTALACIÓN ===")
    python_ok = test_python()
    modules_ok = test_modules()
    db_ok = test_database()
    
    if python_ok and modules_ok and db_ok:
        print("\n🎉 ¡Instalación exitosa! Puede ejecutar la aplicación.")
    else:
        print("\n❌ Hay problemas con la instalación. Revisar errores arriba.")
```

Ejecutar:
```bash
python test_instalacion.py
```

### 6.2 Prueba Rápida

1. Ejecutar aplicación:
   ```bash
   streamlit run app.py
   ```

2. Abrir navegador en `http://localhost:8501`

3. Hacer clic en "Realizar Nueva Medición"

4. Verificar que aparezcan:
   - Peso simulado
   - Gráfica de barras
   - Tabla con datos

## 7. Configuración Avanzada

### 7.1 Configurar Puerto Personalizado

```bash
streamlit run app.py --server.port 8080
```

### 7.2 Acceso desde Red Local

```bash
streamlit run app.py --server.address 0.0.0.0
```

### 7.3 Configuración Permanente

Crear archivo `.streamlit/config.toml`:

```toml
[server]
port = 8501
address = "0.0.0.0"
headless = true

[browser]
gatherUsageStats = false
```

### 7.4 Variables de Entorno

Crear archivo `.env`:
```
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
```

## 8. Solución de Problemas Comunes

### 8.1 Error: "streamlit: command not found"

**Solución**:
```bash
# Verificar instalación
pip show streamlit

# Si no está instalado
pip install streamlit

# Si está instalado pero no se encuentra
export PATH=$PATH:~/.local/bin
```

### 8.2 Error: "Permission denied"

**En Linux/Raspberry Pi**:
```bash
sudo chown -R $USER:$USER ~/bascula_academica
chmod +x ~/bascula_academica/app.py
```

### 8.3 Error: "Port already in use"

**Solución**:
```bash
# Cambiar puerto
streamlit run app.py --server.port 8502

# O matar proceso existente
pkill -f streamlit
```

### 8.4 Problemas de Memoria en Raspberry Pi

**Solución**:
```bash
# Aumentar swap
sudo dphys-swapfile swapoff
sudo nano /etc/dphys-swapfile
# Cambiar CONF_SWAPSIZE=1024
sudo dphys-swapfile setup
sudo dphys-swapfile swapon
```

## 9. Desinstalación

### 9.1 Eliminar Aplicación

```bash
# Eliminar directorio
rm -rf ~/bascula_academica

# Desactivar entorno virtual (si está activo)
deactivate
```

### 9.2 Desinstalar Librerías (Opcional)

```bash
pip uninstall streamlit plotly pandas -y
```

## 10. Actualizaciones

### 10.1 Actualizar Dependencias

```bash
pip install --upgrade streamlit plotly pandas
```

### 10.2 Verificar Versiones

```bash
pip list | grep -E "(streamlit|plotly|pandas)"
```

## 11. Soporte Técnico

### 11.1 Información para Soporte

Antes de solicitar ayuda, recopilar:

```bash
# Información del sistema
python --version
pip --version
streamlit version

# Lista de paquetes instalados
pip list

# Información del sistema operativo
# Linux/Mac:
uname -a
# Windows:
systeminfo
```

### 11.2 Logs de Error

Ubicación de logs:
- **Windows**: `%USERPROFILE%\.streamlit\logs\`
- **Linux/Mac**: `~/.streamlit/logs/`
- **Raspberry Pi**: `/home/pi/.streamlit/logs/`

## 12. Recursos Adicionales

### 12.1 Documentación Oficial
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Plotly Documentation](https://plotly.com/python/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)

### 12.2 Comunidad
- [Streamlit Community Forum](https://discuss.streamlit.io/)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/streamlit)

---

**¡Felicitaciones!** Si siguió todos los pasos correctamente, ahora tiene el Sistema de Báscula Académica funcionando en su equipo. La aplicación está lista para simular mediciones y generar reportes académicos.

Para comenzar a usar la aplicación, simplemente ejecute `streamlit run app.py` y abra su navegador en `http://localhost:8501`.
