# Documentación de Arquitectura - Sistema de Báscula Académica

## 1. Visión General del Sistema

El Sistema de Báscula Académica es una aplicación web desarrollada en Python que simula la lectura de una báscula industrial y códigos QR para validación de productos. La aplicación está diseñada para ser compatible con Raspberry Pi y utiliza una arquitectura modular basada en clases.

## 2. Arquitectura del Sistema

### 2.1 Diagrama de Arquitectura

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

### 2.2 Componentes Principales

#### 2.2.1 Capa de Presentación (Streamlit)
- **Responsabilidad**: Interfaz de usuario web
- **Tecnología**: Streamlit
- **Funciones**:
  - Renderizado de la interfaz web
  - Manejo de eventos de usuario
  - Visualización de datos y gráficas
  - Configuración de parámetros

#### 2.2.2 Capa de Lógica de Negocio

##### BasculaSimulator
- **Responsabilidad**: Simulación de lectura de báscula RS232
- **Métodos**:
  - `leer_peso()`: Genera peso aleatorio entre 21.5-23.8 Kg
  - `extraer_peso_numerico()`: Extrae valor numérico del string

##### QRSimulator
- **Responsabilidad**: Simulación de lectura de códigos QR
- **Métodos**:
  - `generar_qr()`: Genera string CSV simulado
  - `parsear_qr()`: Parsea string CSV a diccionario

##### ProcesadorLogica
- **Responsabilidad**: Lógica de validación de negocio
- **Métodos**:
  - `validar_peso()`: Valida peso contra reglas de negocio

#### 2.2.3 Capa de Datos

##### DatabaseManager
- **Responsabilidad**: Gestión de persistencia en SQLite
- **Métodos**:
  - `init_database()`: Inicializa base de datos
  - `guardar_medicion()`: Persiste mediciones
  - `obtener_mediciones()`: Recupera datos históricos

## 3. Modelo de Datos

### 3.1 Esquema de Base de Datos

```sql
CREATE TABLE mediciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    peso_leido REAL,
    peso_string TEXT,
    op INTEGER,
    descripcion TEXT,
    referencia TEXT,
    lote TEXT,
    peso_minimo REAL,
    fecha_vencimiento DATE,
    cumple_regla BOOLEAN,
    margen_error REAL,
    diferencia_peso REAL
);
```

### 3.2 Descripción de Campos

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | INTEGER | Clave primaria autoincremental |
| timestamp | DATETIME | Fecha y hora de la medición |
| peso_leido | REAL | Peso numérico leído de la báscula |
| peso_string | TEXT | String original del peso (ej: "22.5Kg") |
| op | INTEGER | Número de operación del QR |
| descripcion | TEXT | Descripción del producto |
| referencia | TEXT | Referencia del producto |
| lote | TEXT | Lote del producto |
| peso_minimo | REAL | Peso mínimo esperado |
| fecha_vencimiento | DATE | Fecha de vencimiento |
| cumple_regla | BOOLEAN | Si cumple con la validación |
| margen_error | REAL | Margen de error aplicado |
| diferencia_peso | REAL | Diferencia absoluta de peso |

## 4. Flujo de Datos

### 4.1 Proceso de Medición

```
1. Usuario presiona "Realizar Nueva Medición"
   ↓
2. BasculaSimulator.leer_peso() → Genera peso simulado
   ↓
3. QRSimulator.generar_qr() → Genera datos QR simulados
   ↓
4. ProcesadorLogica.validar_peso() → Valida reglas de negocio
   ↓
5. DatabaseManager.guardar_medicion() → Persiste en SQLite
   ↓
6. Actualización de interfaz (gráficas, tablas, métricas)
```

### 4.2 Flujo de Validación

```
Peso Leído vs Peso Mínimo
   ↓
Cálculo de límites:
- Límite Inferior = peso_minimo * (1 - margen_error/100)
- Límite Superior = peso_minimo * (1 + margen_error/100)
   ↓
Validación: límite_inferior ≤ peso_leido ≤ límite_superior
   ↓
Resultado: cumple_regla (True/False)
```

## 5. Patrones de Diseño Implementados

### 5.1 Singleton Pattern
- **Implementación**: DatabaseManager en session_state
- **Propósito**: Una sola instancia de conexión a BD por sesión

### 5.2 Static Factory Pattern
- **Implementación**: Métodos estáticos en simuladores
- **Propósito**: Creación de datos simulados sin instanciación

### 5.3 Strategy Pattern
- **Implementación**: ProcesadorLogica para validaciones
- **Propósito**: Algoritmos de validación intercambiables

## 6. Consideraciones de Rendimiento

### 6.1 Base de Datos
- **SQLite**: Adecuado para aplicaciones de escritorio/embedded
- **Índices**: Automático en PRIMARY KEY
- **Consultas**: Limitadas a últimas 20 mediciones en gráficas

### 6.2 Memoria
- **Session State**: Mantiene estado entre recargas
- **Caché**: Streamlit maneja caché automáticamente
- **Límites**: Sin límite explícito en historial

### 6.3 Interfaz
- **Lazy Loading**: Gráficas se cargan solo con datos
- **Responsive**: Layout adaptativo con columnas
- **Auto-refresh**: Opcional cada 5 segundos

## 7. Seguridad

### 7.1 Validación de Datos
- **Entrada**: Validación de tipos en parseo QR
- **SQL**: Uso de parámetros preparados
- **Errores**: Manejo de excepciones en operaciones críticas

### 7.2 Persistencia
- **SQLite**: Base de datos local, sin exposición de red
- **Permisos**: Depende del sistema operativo host
- **Backup**: Manual por parte del usuario

## 8. Escalabilidad

### 8.1 Limitaciones Actuales
- **Usuarios**: Aplicación monousuario
- **Datos**: SQLite hasta ~281 TB teóricos
- **Concurrencia**: Sin manejo de concurrencia

### 8.2 Posibles Mejoras
- **Base de Datos**: Migración a PostgreSQL/MySQL
- **Autenticación**: Sistema de usuarios
- **API**: Separación frontend/backend
- **Microservicios**: Separación por funcionalidad

## 9. Compatibilidad con Raspberry Pi

### 9.1 Requisitos Mínimos
- **RAM**: 1GB (recomendado 2GB+)
- **Storage**: 500MB libres
- **Python**: 3.7+
- **OS**: Raspberry Pi OS (Debian-based)

### 9.2 Optimizaciones
- **Dependencias**: Mínimas y ligeras
- **Recursos**: Sin procesamiento intensivo
- **Red**: Solo localhost por defecto

## 10. Mantenimiento

### 10.1 Logs
- **Streamlit**: Logs automáticos en consola
- **Errores**: Capturados y mostrados en UI
- **Debug**: Información disponible en terminal

### 10.2 Monitoreo
- **Métricas**: Disponibles en interfaz
- **Estado**: Indicadores visuales de funcionamiento
- **Historial**: Persistente en base de datos

## 11. Tecnologías Utilizadas

| Componente | Tecnología | Versión | Propósito |
|------------|------------|---------|-----------|
| Framework Web | Streamlit | 1.29.0 | Interfaz de usuario |
| Visualización | Plotly | 5.17.0 | Gráficas interactivas |
| Datos | Pandas | 2.1.4 | Manipulación de datos |
| Base de Datos | SQLite | 3.x | Persistencia |
| Lenguaje | Python | 3.7+ | Desarrollo principal |

## 12. Conclusiones

La arquitectura implementada proporciona:
- **Modularidad**: Separación clara de responsabilidades
- **Mantenibilidad**: Código organizado y documentado
- **Escalabilidad**: Base sólida para futuras mejoras
- **Usabilidad**: Interfaz intuitiva y responsive
- **Compatibilidad**: Funciona en Raspberry Pi sin modificaciones

Esta arquitectura cumple con todos los requisitos funcionales especificados y proporciona una base sólida para el desarrollo académico y futuras extensiones del sistema.
