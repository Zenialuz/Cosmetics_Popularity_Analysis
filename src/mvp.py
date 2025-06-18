import streamlit as st
import pandas as pd
from recomendacion_productos import top10_productos, get_categoria_producto, get_tipos_producto, get_zona_aplicacion
from skin_type_classifier import predict_skin_type
import tempfile
from PIL import Image
st.set_page_config(page_title="Dermabotix App", page_icon=":guardsman:", layout="wide")

st.markdown(
    """
    <style>
    /* Fondo general */
    .stApp {
        background-color: #C99357;
        font-family: 'Segoe UI', sans-serif;
        padding-top: 30px;
        padding-bottom: 30px;
    }

    /* Contenedor tipo tarjeta */
    .card {
        background-color: #E9D4BD;
        max-width: 900px;
        margin: 0 auto;
        padding: 40px 30px;
        border-radius: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }

    /* Botones */
    .stButton>button {
        background-color: #E9D4BD;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        font-weight: bold;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        transition: 0.3s ease;
    }

    .stButton>button:hover {
        background-color: #A5D6C4;
        color: black;
    }

    /* Títulos */
    .stTitle, .stHeader, .stSubheader {
        color: #6E4B24;
        text-align: center;
    }

    /* Cajas y tablas */
    .stSelectbox, .stFileUploader, .stTextInput, .stTextArea, .stDataFrame, .dataframe {
        background-color: #E9D4BD !important;
        border-radius: 10px;
        padding: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }

    /* Ocultar footer */
    footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True
)

# Cargar la imagen del logo
logo = Image.open("Logo.png")

with st.container():
        
    # Mostrar el logo centrado y con tamaño ajustado
    st.image(logo, width=350, use_container_width =False)  # Ajusta el ancho a tu gusto
    

st.write("Welcome to the Dermabotix App!")

# Lista desplegable de categorías
categorias = get_categoria_producto("data/modelo_copo_nieve/modelo_copo_nieve.db")
categorias = categorias['categoria'].tolist()
categoria_seleccionada = st.selectbox("Selecciona una categoría de producto:", categorias)

# Lista desplegable de tipos de producto
tipos_producto = get_tipos_producto("data/modelo_copo_nieve/modelo_copo_nieve.db")
tipos_producto = tipos_producto['tipo_producto'].tolist()
tipo_producto = st.selectbox("Selecciona un tipo de producto:", tipos_producto)

# Lista desplegable de zona de aplicación

zonas_aplicacion = get_zona_aplicacion("data/modelo_copo_nieve/modelo_copo_nieve.db")
zonas_aplicacion = zonas_aplicacion['zona_aplicacion'].tolist()
zona_aplicacion = st.selectbox("Selecciona una zona de aplicación", zonas_aplicacion)

# Cargar imagen del usuario
imagen = st.file_uploader("Upload an image of your skin", type=["jpg", "jpeg", "png"])
if imagen is not None:
    st.image(imagen, caption="Uploaded Image", use_column_width=True)
    st.write("Image uploaded successfully!")
    
    # Guardar la imagen subida en un archivo temporal
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
        tmp_file.write(imagen.getbuffer())
        temp_image_path = tmp_file.name

    # Llamar a la función de predicción usando la ruta temporal
    tipo_piel = predict_skin_type(temp_image_path)
    st.write(f"Detected skin type: {tipo_piel}")
    
    
    
    df_cosmeticos = top10_productos("data/modelo_copo_nieve/modelo_copo_nieve.db", tipo_piel, categoria_seleccionada, tipo_producto, zona_aplicacion)
    
     # Mostrar el DataFrame
    st.subheader("Top Recommended Skin Care Products for skin type: " + tipo_piel)
    #st.dataframe(df_cosmeticos)
    st.write(df_cosmeticos.to_html(escape=False, index=False), unsafe_allow_html=True)
else:
    st.write("Please upload an image of your skin to get started.")
    
