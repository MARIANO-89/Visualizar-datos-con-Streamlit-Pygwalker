import streamlit as st
import pandas as pd
import pygwalker as pyg
from pygwalker.api.streamlit import StreamlitRenderer

# Configurar la página de Streamlit
st.set_page_config(
    page_title="Análisis de datos",
    layout="wide"
)

# Título de la aplicación
st.title('Visualización de Datos con Streamlit - Pygwalker')

# Incluir CSS para el fondo cambiante, texto blanco y estilos del área de carga de archivos
st.markdown("""
    <style>
    body {
        margin: 0;
        padding: 0;
        height: 100vh;
        font-family: Arial, sans-serif;
        display: flex;
        justify-content: center;
        align-items: center;
        overflow: hidden;
        background-image: linear-gradient(to top, #9890e3 0%, #b1f4cf 100%);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
        color: white; /* Color del texto en toda la aplicación */
    }

    @keyframes gradient {
        0% { background-position: 0% 0%; }
        50% { background-position: 100% 100%; }
        100% { background-position: 0% 0%; }
    }

    .stApp {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        height: 100vh;
        text-align: center;
        width: 100%;
         margin: 0;
        padding: 0;
        height: 100vh;
        font-family: Arial, sans-serif;
        display: flex;
        justify-content: center;
        align-items: center;
        overflow: hidden;
        background-image: linear-gradient(to top, #9890e3 0%, #b1f4cf 100%);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
    }

    .stFileUploader {
        background-image: linear-gradient(to top, #9890e3 0%, #b1f4cf 100%);
        border: 2px dashed white; /* Borde para el área de carga */
        padding: 20px;
        border-radius: 10px;
        color: white; /* Color del texto en toda la aplicación */
    }

 .css-1kyxreq {
        background-image: linear-gradient(to top, #9890e3 0%, #b1f4cf 100%);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
         color: white; /* Color del texto en toda la aplicación */
    }

    .stFileUploader:hover {
        background-image: linear-gradient(to top, #9890e3 0%, #b1f4cf 100%);

    }
    </style>
    """, unsafe_allow_html=True)

# Función para cargar datos
@st.cache_data
def cargar_datos(archivo):
    try:
        if archivo.name.endswith('.csv'):
            return pd.read_csv(archivo)  # Cargar usando pandas
        elif archivo.name.endswith('.xlsx'):
            return pd.read_excel(archivo, engine='openpyxl')
        else:
            st.error('Formato de archivo no soportado')
            return None
    except Exception as e:
        st.error(f"Error al cargar el archivo: {e}")
        return None

# Función para obtener el renderer de Pygwalker
@st.cache_resource
def get_pyg_renderer(df) -> "StreamlitRenderer":
    # Si quieres usar la característica de guardar configuración, setea spec_io_mode="rw"
    return StreamlitRenderer(df, kernel_computation=True,spec_io_mode="rw")

# Estado inicial de visualización de PyGWalker
if 'show_pygwalker' not in st.session_state:
    st.session_state.show_pygwalker = False

# Cargar archivo
archivo = st.file_uploader('Carga tu archivo CSV o XLSX', type=['csv', 'xlsx'])

if archivo is not None:
    df = cargar_datos(archivo)

    if df is not None:
        st.write('Datos cargados exitosamente:')

        # Selector para el número de filas a mostrar
        num_filas = st.number_input('Número de filas a mostrar', min_value=10, max_value=10000, value=100, step=100)
        st.dataframe(df.head(num_filas))  # Muestra solo las primeras num_filas filas

        # Botón para visualizar con Pygwalker
        if st.button('Visualizar con Pygwalker'):
            st.session_state.show_pygwalker = True

        # Mostrar PyGWalker si el botón ha sido presionado
        if st.session_state.show_pygwalker:
            st.markdown('## Visualización con PyGwalker')
            try:
                renderer = get_pyg_renderer(df)
                renderer.explorer()
            except Exception as e:
                st.error(f"Error al visualizar con Pygwalker: {e}")
