import streamlit as st
import pandas as pd
from src.recomendacion_productos import top10_productos, get_categoria_producto, get_tipos_producto, get_zona_aplicacion

st.set_page_config(page_title="Skin Care App", page_icon=":guardsman:", layout="wide")
st.title("Skin Care App")
st.write("Welcome to the Skin Care App!")

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

# Cargar la base de datos y obtener las categorías
imagen = st.file_uploader("Upload an image of your skin", type=["jpg", "jpeg", "png"])
if imagen is not None:
    st.image(imagen, caption="Uploaded Image", use_column_width=True)
    st.write("Image uploaded successfully!")
    tipo_piel = 'Seca'  # This should be determined by your skin analysis model
    st.write(f"Detected skin type: {tipo_piel}")
    
    df_cosmeticos = top10_productos("data/modelo_copo_nieve/modelo_copo_nieve.db", tipo_piel, categoria_seleccionada, tipo_producto, zona_aplicacion)
    
     # Mostrar el DataFrame
    st.subheader("Top Recommended Skin Care Products for skin type: " + tipo_piel)
    #st.dataframe(df_cosmeticos)
    st.write(df_cosmeticos.to_html(escape=False, index=False), unsafe_allow_html=True)
else:
    st.write("Please upload an image of your skin to get started.")
    
