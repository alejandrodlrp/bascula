import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import sqlite3
import pandas as pd
import random
import time
from datetime import datetime, timedelta
import re

# Configuración de la página
st.set_page_config(
    page_title="Sistema de Báscula Académica",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

class BasculaSimulator:
    """Clase para simular la lectura de báscula"""
    
    @staticmethod
    def leer_peso():
        """Simula la lectura del peso de una báscula RS232"""
        peso = round(random.uniform(21.5, 23.8), 1)
        return f"{peso}Kg"
    
    @staticmethod
    def extraer_peso_numerico(peso_str):
        """Extrae el valor numérico del string de peso"""
        match = re.search(r'(\d+\.?\d*)Kg', peso_str)
        if match:
            return float(match.group(1))
        return None

class QRSimulator:
    """Clase para simular la lectura de códigos QR"""
    
    PRODUCTOS = [
        "Arroz Premium", "Frijoles Rojos", "Lentejas Verdes", 
        "Quinoa Orgánica", "Avena Integral", "Pasta Italiana"
    ]
    
    REFERENCIAS = ["REF001", "REF002", "REF003", "REF004", "REF005", "REF006"]
    LOTES = ["L2024001", "L2024002", "L2024003", "L2024004", "L2024005"]
    
    @staticmethod
    def generar_qr():
        """Simula la lectura de un código QR con formato CSV"""
        op = random.randint(1000, 9999)
        descripcion = random.choice(QRSimulator.PRODUCTOS)
        referencia = random.choice(QRSimulator.REFERENCIAS)
        lote = random.choice(QRSimulator.LOTES)
        peso_minimo = round(random.uniform(20.0, 24.0), 1)
        fecha_vencimiento = (datetime.now() + timedelta(days=random.randint(30, 365))).strftime("%Y-%m-%d")
        
        return f"{op},{descripcion},{referencia},{lote},{peso_minimo},{fecha_vencimiento}"
    
    @staticmethod
    def parsear_qr(qr_string):
        """Parsea el string CSV del código QR"""
        try:
            partes = qr_string.split(',')
            return {
                'op': int(partes[0]),
                'descripcion': partes[1],
                'referencia': partes[2],
                'lote': partes[3],
                'peso_minimo': float(partes[4]),
                'fecha_vencimiento': partes[5]
            }
        except (ValueError, IndexError):
            return None

class DatabaseManager:
    """Clase para manejar la base de datos SQLite"""
    
    def __init__(self, db_path="bascula_data.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Inicializa la base de datos y crea las tablas necesarias"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mediciones (
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
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def guardar_medicion(self, datos):
        """Guarda una medición en la base de datos"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO mediciones 
            (peso_leido, peso_string, op, descripcion, referencia, lote, 
             peso_minimo, fecha_vencimiento, cumple_regla, margen_error, diferencia_peso)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            datos['peso_leido'], datos['peso_string'], datos['op'],
            datos['descripcion'], datos['referencia'], datos['lote'],
            datos['peso_minimo'], datos['fecha_vencimiento'], datos['cumple_regla'],
            datos['margen_error'], datos['diferencia_peso']
        ))
        
        conn.commit()
        conn.close()
    
    def obtener_mediciones(self, limit=None):
        """Obtiene las mediciones de la base de datos"""
        conn = sqlite3.connect(self.db_path)
        query = "SELECT * FROM mediciones ORDER BY timestamp DESC"
        if limit:
            query += f" LIMIT {limit}"
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df

class ProcesadorLogica:
    """Clase para procesar la lógica de negocio"""
    
    @staticmethod
    def validar_peso(peso_leido, peso_minimo, margen_error=5.0):
        """Valida si el peso está dentro del rango permitido"""
        limite_inferior = peso_minimo * (1 - margen_error / 100)
        limite_superior = peso_minimo * (1 + margen_error / 100)
        
        cumple = limite_inferior <= peso_leido <= limite_superior
        diferencia = abs(peso_leido - peso_minimo)
        
        return {
            'cumple': cumple,
            'diferencia': diferencia,
            'limite_inferior': limite_inferior,
            'limite_superior': limite_superior
        }

def main():
    """Función principal de la aplicación"""
    
    # Título principal
    st.title("⚖️ Sistema de Báscula Académica")
    st.markdown("---")
    
    # Inicializar componentes
    if 'db_manager' not in st.session_state:
        st.session_state.db_manager = DatabaseManager()
    
    if 'mediciones_realizadas' not in st.session_state:
        st.session_state.mediciones_realizadas = []
    
    # Sidebar para configuración
    st.sidebar.header("⚙️ Configuración")
    margen_error = st.sidebar.slider(
        "Margen de Error (%)", 
        min_value=1.0, 
        max_value=5.0, 
        value=2.8, 
        step=0.1
    )
    
    auto_refresh = st.sidebar.checkbox("Auto-actualizar cada 5 segundos", value=False)
    
    if auto_refresh:
        time.sleep(2)
        st.rerun()
    
    # Layout principal
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📊 Simulación de Lectura")
        
        if st.button("🔄 Realizar Nueva Medición", type="primary", use_container_width=True):
            # Simular lectura de báscula
            peso_string = BasculaSimulator.leer_peso()
            peso_numerico = BasculaSimulator.extraer_peso_numerico(peso_string)
            
            # Simular lectura de QR
            qr_string = QRSimulator.generar_qr()
            qr_data = QRSimulator.parsear_qr(qr_string)
            
            if peso_numerico and qr_data:
                # Procesar lógica de negocio
                validacion = ProcesadorLogica.validar_peso(
                    peso_numerico, 
                    qr_data['peso_minimo'], 
                    margen_error
                )
                
                # Preparar datos para guardar
                datos_medicion = {
                    'peso_leido': peso_numerico,
                    'peso_string': peso_string,
                    'op': qr_data['op'],
                    'descripcion': qr_data['descripcion'],
                    'referencia': qr_data['referencia'],
                    'lote': qr_data['lote'],
                    'peso_minimo': qr_data['peso_minimo'],
                    'fecha_vencimiento': qr_data['fecha_vencimiento'],
                    'cumple_regla': validacion['cumple'],
                    'margen_error': margen_error,
                    'diferencia_peso': validacion['diferencia']
                }
                
                # Guardar en base de datos
                st.session_state.db_manager.guardar_medicion(datos_medicion)
                
                # Agregar a la lista de mediciones en memoria
                st.session_state.mediciones_realizadas.append(datos_medicion)
                
                st.success("✅ Medición realizada y guardada exitosamente")
        
        # Mostrar peso actual
        st.subheader("⚖️ Peso Actual")
        if st.session_state.mediciones_realizadas:
            ultimo_peso = st.session_state.mediciones_realizadas[-1]['peso_string']
            st.markdown(
                f"""
                <div style="
                    border: 2px solid #4CAF50;
                    border-radius: 10px;
                    padding: 20px;
                    text-align: center;
                    background-color: #f9f9f9;
                    margin: 10px 0;
                ">
                    <h1 style="font-size: 30px; color: #2E7D32; margin: 0;">
                        {ultimo_peso}
                    </h1>
                </div>
                """, 
                unsafe_allow_html=True
            )
            
            # Mostrar estado de validación
            ultima_medicion = st.session_state.mediciones_realizadas[-1]
            if ultima_medicion['cumple_regla']:
                st.success("✅ El peso cumple con los requisitos")
            else:
                st.error("❌ El peso NO cumple con los requisitos. Tome acción correctiva.")
                st.warning(f"Diferencia: {ultima_medicion['diferencia_peso']:.2f} Kg")
    
    with col2:
        st.header("📈 Gráfica de Mediciones")
        
        # Obtener datos de la base de datos
        df_mediciones = st.session_state.db_manager.obtener_mediciones(limit=20)
        
        if not df_mediciones.empty:
            # Crear gráfica de barras
            fig = go.Figure()
            
            # Colores según cumplimiento
            colores = ['green' if cumple else 'red' for cumple in df_mediciones['cumple_regla']]
            
            fig.add_trace(go.Bar(
                x=list(range(len(df_mediciones))),
                y=df_mediciones['peso_leido'],
                marker_color=colores,
                text=df_mediciones['peso_leido'],
                textposition='auto',
                name='Peso Leído'
            ))
            
            fig.update_layout(
                title="Historial de Pesos Medidos",
                xaxis_title="Medición #",
                yaxis_title="Peso (Kg)",
                showlegend=False,
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No hay mediciones disponibles. Realice una medición para ver la gráfica.")
    
    # Tabla de historial
    st.header("📋 Historial de Mediciones")
    
    df_mediciones = st.session_state.db_manager.obtener_mediciones()
    
    if not df_mediciones.empty:
        # Formatear la tabla para mejor visualización
        df_display = df_mediciones.copy()
        df_display['timestamp'] = pd.to_datetime(df_display['timestamp']).dt.strftime('%Y-%m-%d %H:%M:%S')
        df_display['cumple_regla'] = df_display['cumple_regla'].map({True: '✅ Sí', False: '❌ No'})
        df_display['peso_leido'] = df_display['peso_leido'].round(2)
        df_display['peso_minimo'] = df_display['peso_minimo'].round(2)
        df_display['diferencia_peso'] = df_display['diferencia_peso'].round(2)
        
        # Seleccionar columnas para mostrar
        columnas_mostrar = [
            'timestamp', 'peso_string', 'peso_leido', 'descripcion', 
            'referencia', 'lote', 'peso_minimo', 'cumple_regla', 'diferencia_peso'
        ]
        
        st.dataframe(
            df_display[columnas_mostrar],
            use_container_width=True,
            hide_index=True
        )
        
        # Estadísticas
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Mediciones", len(df_mediciones))
        
        with col2:
            cumplimientos = df_mediciones['cumple_regla'].sum()
            st.metric("Mediciones Válidas", cumplimientos)
        
        with col3:
            peso_promedio = df_mediciones['peso_leido'].mean()
            st.metric("Peso Promedio", f"{peso_promedio:.2f} Kg")
        
        with col4:
            if len(df_mediciones) > 0:
                porcentaje_exito = (cumplimientos / len(df_mediciones)) * 100
                st.metric("% Éxito", f"{porcentaje_exito:.1f}%")
    else:
        st.info("No hay mediciones registradas en la base de datos.")
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: center; color: #666;">
            <p>Sistema de Báscula Académica - Desarrollado con Streamlit y Python</p>
            <p>Autor Alejandro de los Rios</p>
        </div>
        """, 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
