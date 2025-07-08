# Sistema de Báscula Académica

## 📋 Descripción

Sistema web académico desarrollado en Python que simula la lectura de una báscula industrial y códigos QR para validación de productos. La aplicación utiliza Streamlit para la interfaz web, Plotly para visualizaciones interactivas, y SQLite para persistencia de datos.

## ✨ Características Principales

- **Simulación de Báscula**: Genera lecturas de peso aleatorias en formato RS232 (21.5-23.8 Kg)
- **Simulación de Códigos QR**: Genera datos CSV con información de productos
- **Validación de Reglas de Negocio**: Compara pesos con margen de error configurable (5% por defecto)
- **Visualización en Tiempo Real**: Gráficas de barras interactivas con Plotly
- **Historial Completo**: Tabla HTML con todas las mediciones realizadas
- **Persistencia de Datos**: Base de datos SQLite para almacenamiento permanente
- **Compatible con Raspberry Pi**: Optimizado para dispositivos embebidos

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────────────────────────┐
│                    INTERFAZ WEB (Streamlit)                │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │   Entrada   │  │ Procesamiento│  │       Salida        │  │
│  │   Módulo    │  │    Módulo    │  │      Módulo         │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
├─────────────────────────────────────────────────────────────┤
│                    CAPA DE LÓGICA DE NEGOCIO               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │ Báscula     │  │ QR          │  │ Procesador          │  │
│  │ Simulator   │  │ Simulator   │  │ Lógica              │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
├─────────────────────────────────────────────────────────────┤
│                    CAPA DE DATOS                           │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │            Database Manager (SQLite)                   │  │
│  └─────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 Inicio Rápido

### Requisitos Previos
- Python 3.7 o superior
- pip (gestor de paquetes de Python)

### Instalación

1. **Clonar o descargar los archivos del proyecto**

2. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Ejecutar la aplicación**:
   ```bash
   streamlit run app.py
   ```

4. **Abrir en el navegador**:
   - La aplicación se abrirá automáticamente
   - O ir manualmente a: `http://localhost:8501`

## 📁 Estructura del Proyecto

```
bascula_Alejo/
├── app.py                          # Aplicación principal
├── requirements.txt                # Dependencias de Python
├── README.md                       # Este archivo
├── ARQUITECTURA.md                 # Documentación de arquitectura
├── GUIA_INSTALACION.md            # Guía completa de instalación
├── GUIA_RESOLUCION_PROBLEMAS.md   # Guía de troubleshooting
└── bascula_data.db                # Base de datos SQLite (se crea automáticamente)
```

## 🛠️ Tecnologías Utilizadas

| Componente | Tecnología | Versión | Propósito |
|------------|------------|---------|-----------|
| Framework Web | Streamlit | 1.29.0 | Interfaz de usuario |
| Visualización | Plotly | 5.17.0 | Gráficas interactivas |
| Datos | Pandas | 2.1.4 | Manipulación de datos |
| Base de Datos | SQLite | 3.x | Persistencia |
| Lenguaje | Python | 3.7+ | Desarrollo principal |

## 📊 Funcionalidades

### Módulo de Entrada (Simulado)
- **Báscula RS232**: Simula lecturas de peso en formato "XX.XKg"
- **Código QR**: Genera strings CSV con formato: `op,descripción,referencia,lote,peso_mínimo,fecha_vencimiento`

### Módulo de Procesamiento
- **Extracción de Datos**: Parsea strings de peso y códigos QR
- **Validación de Reglas**: Compara peso leído vs peso mínimo con margen de error configurable
- **Cálculo de Diferencias**: Determina desviaciones y cumplimiento

### Módulo de Salida
- **Display de Peso**: Contenedor estilizado con fuente de 30px
- **Indicadores de Estado**: Mensajes claros sobre cumplimiento de reglas
- **Gráfica de Barras**: Visualización en tiempo real con Plotly
- **Tabla de Historial**: Registro completo de todas las mediciones
- **Métricas**: Estadísticas resumidas del sistema

### Persistencia
- **Base de Datos SQLite**: Almacenamiento local de todas las mediciones
- **Esquema Completo**: Incluye timestamps, datos de báscula, información QR, y resultados de validación

## 🎯 Casos de Uso

1. **Educación Académica**: Simulación de procesos industriales sin hardware físico
2. **Prototipado**: Desarrollo de lógica antes de implementar hardware real
3. **Demostración**: Presentación de conceptos de automatización industrial
4. **Pruebas**: Validación de algoritmos de control de calidad

## 📱 Interfaz de Usuario

### Panel Principal
- **Botón de Medición**: Inicia simulación completa
- **Display de Peso**: Muestra último peso medido con estilo visual
- **Estado de Validación**: Indicadores de cumplimiento/incumplimiento

### Panel de Visualización
- **Gráfica de Barras**: Historial de pesos con código de colores
- **Configuración**: Slider para ajustar margen de error
- **Auto-actualización**: Opción de refresh automático cada 5 segundos

### Panel de Datos
- **Tabla Completa**: Historial detallado de todas las mediciones
- **Métricas**: Total de mediciones, válidas, peso promedio, % de éxito
- **Filtros**: Visualización de últimas 20 mediciones en gráficas

## 🔧 Configuración

### Parámetros Configurables
- **Margen de Error**: 1-10% (default: 5%)
- **Rango de Peso**: 21.5-23.8 Kg (modificable en código)
- **Productos**: Lista expandible de productos simulados
- **Puerto de Red**: Configurable via parámetros de Streamlit

### Variables de Entorno
```bash
# Puerto personalizado
streamlit run app.py --server.port 8080

# Acceso desde red
streamlit run app.py --server.address 0.0.0.0

# Modo headless (sin navegador)
streamlit run app.py --server.headless true
```

## 🐛 Resolución de Problemas

### Problemas Comunes

1. **ModuleNotFoundError**: Instalar dependencias con `pip install -r requirements.txt`
2. **Puerto en uso**: Cambiar puerto con `--server.port 8502`
3. **Base de datos bloqueada**: Cerrar todas las instancias y reiniciar
4. **Rendimiento lento**: Reducir límite de datos mostrados

Ver [GUIA_RESOLUCION_PROBLEMAS.md](GUIA_RESOLUCION_PROBLEMAS.md) para soluciones detalladas.

## 📚 Documentación

- **[ARQUITECTURA.md](ARQUITECTURA.md)**: Documentación técnica completa
- **[GUIA_INSTALACION.md](GUIA_INSTALACION.md)**: Instrucciones de instalación paso a paso
- **[GUIA_RESOLUCION_PROBLEMAS.md](GUIA_RESOLUCION_PROBLEMAS.md)**: Troubleshooting y soluciones

## 🔄 Flujo de Trabajo

```
1. Usuario presiona "Realizar Nueva Medición"
   ↓
2. Sistema genera peso simulado (21.5-23.8 Kg)
   ↓
3. Sistema genera código QR simulado (CSV)
   ↓
4. Extrae datos numéricos y parsea información
   ↓
5. Valida peso contra reglas de negocio
   ↓
6. Guarda resultado en base de datos SQLite
   ↓
7. Actualiza interfaz (gráficas, tablas, métricas)
```

## 🎨 Capturas de Pantalla

La interfaz incluye:
- **Header**: Título y navegación
- **Sidebar**: Configuración y controles
- **Main Panel**: Botón de medición y display de peso
- **Charts Panel**: Gráfica de barras interactiva
- **Data Panel**: Tabla de historial y métricas
- **Footer**: Información del sistema

## 🚀 Instalación en Raspberry Pi

### Pasos Específicos
```bash
# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar dependencias
sudo apt install python3-pip python3-venv -y

# Crear entorno virtual
python3 -m venv bascula_env
source bascula_env/bin/activate

# Instalar librerías
pip install -r requirements.txt

# Ejecutar aplicación
streamlit run app.py --server.address 0.0.0.0
```

### Optimizaciones para Raspberry Pi
- Límite de datos en gráficas (20 registros)
- Uso eficiente de memoria
- Configuración de swap si es necesario
- Inicio automático opcional

## 📈 Métricas y Estadísticas

El sistema proporciona:
- **Total de Mediciones**: Contador acumulativo
- **Mediciones Válidas**: Que cumplen con las reglas
- **Peso Promedio**: Media aritmética de todas las mediciones
- **Porcentaje de Éxito**: Ratio de mediciones válidas

## 🔒 Seguridad

- **Base de Datos Local**: Sin exposición de red por defecto
- **Validación de Entrada**: Manejo de errores en parseo de datos
- **SQL Preparado**: Prevención de inyección SQL
- **Manejo de Excepciones**: Captura y manejo de errores

## 🌟 Características Avanzadas

- **Session State**: Mantiene estado entre recargas
- **Auto-refresh**: Actualización automática opcional
- **Responsive Design**: Adaptable a diferentes tamaños de pantalla
- **Código de Colores**: Verde para válido, rojo para inválido
- **Timestamps**: Registro temporal de todas las operaciones

## 📞 Soporte

Para soporte técnico:
1. Revisar la documentación incluida
2. Verificar logs del sistema
3. Consultar guía de resolución de problemas
4. Recopilar información del sistema antes de reportar

## 📄 Licencia

Este proyecto es de uso académico y educativo.

## 👥 Contribuciones

Para contribuir al proyecto:
1. Fork del repositorio
2. Crear rama para nueva funcionalidad
3. Implementar cambios con documentación
4. Enviar pull request con descripción detallada

---

**Desarrollado con ❤️ para educación académica en Python, Streamlit y sistemas embebidos.**
