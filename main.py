# Importando librerías necesarias
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
import nbformat
import ipywidgets as widgets
import plotly.io as pio
import os
import plotly.express as px


from src.extraction import sraping_webSite, carga_csv
from src.exploration import exploracion_data, exploracion_por_categoria
from src.transformation import limpieza_datos
from src.transformation import transformacion_datos
from src.visualizacion import grafico_cajas_columna, correlacion_variables, grafico_frecuencia_marcas,grafico_proporcion_tipo_piel,grafico_densidad_columna
from src.loadModel import cargar_df_a_staging, script_generar_mondelo_y_carga_datos,generar_modelo_a_partir_de_sql

###############################################
# Configuración de variables globales
###############################################

# Ruta de archivo para guardar y obtener los datos en csv
data_csv = "data/Primor/data_primor_lujo.csv"

nombre_bd = 'data/modeloEstrella/modelo_estrella.db'
nombre_tabla_staging = 'staging_data'
ruta_script_sql = 'data/modeloEstrella/script_carga_datos_modelo_estrella.sql'

# Lista de url de las categorías de productos
categorias = [
        ("Hidratantes y Nutrivas", "https://www.primor.eu/es_es/hidratantes-y-nutritivas-lujo"),
        ("Antiarrugas y antiedad", "https://www.primor.eu/es_es/antiarrugas-y-antiedad-lujo"),
        ("Contorno de Ojos", "https://www.primor.eu/es_es/contorno-de-ojos-lujo"),
        ("Tratamientos especificos", "https://www.primor.eu/es_es/tratamientos-especificos-lujo"),
        ("limpiadoras tonicos", "https://www.primor.eu/es_es/limpiadoras-tonicos-lujo"),
        ("cofres", "https://www.primor.eu/es_es/cofres-lujo-1"),
        ("labios balsamos y cuidados", "https://www.primor.eu/es_es/labios-balsamos-y-cuidados-lujo"),
        ("Antimanchas", "https://www.primor.eu/es_es/antimanchas-lujo"),
        ("Exfoliantes", "https://www.primor.eu/es_es/exfoliantes-lujo"),
        ("Tratamientos calmantes", "https://www.primor.eu/es_es/tratamientos-calmantes-y-para-piel-sensible")
    ]

# Lista de parámetros de tipos de piel para construir la url de los productos
tipos_de_piel = [
        ("Normal", 66101),
        ("Deshidratada", 66094),
        ("Sensible", 66110), 
        ("Todo tipo de piel", 66111),
        ("Madura", 66097),
        ("Muy seca", 66100),
        ("seca", 66107),
        ("Grasa", 66096),
        ("Mixta", 66098),
        ("Mixta a Grasa", 66099),
        ("Normal a seca", 66104),
        ("seca-muy seca", 66109),
        ("seca - mixta", 66108),
        ("atopica", 66092),
        ("Delicadas", 66093),
        ("Apagadas", 66091)
    ]

 # Lista de parámetros de zonas de aplicación para construir la url de los productos   
zonas_aplicacion = [        
        ("Rostro", 66325),
        ("Cuerpo", 66309),
        ("Manos", 66315),
        ("Ojos", 66319),
        ("Cuello", 66308)      
    ]




# Obtención de datos usando Selenium y BeautifulSoup para scrapear (Para ejecución de scraping descomentar la siguiente línea)
# df_primor = sraping_webSite(categorias, tipos_de_piel, zonas_aplicacion, data_csv)
# print(df_primor.head(5))


# Carga de datos desde un archivo CSV
df_cosmeticos = carga_csv(data_csv)
print(df_cosmeticos.head(5).to_string())

# Exploración de datos
exploracion_data(df_cosmeticos)
exploracion_por_categoria(df_cosmeticos)

# Limpieza de datos
df_cosmeticos = limpieza_datos(df_cosmeticos)
print(df_cosmeticos.head(5).to_string())

# Transformación de datos
df_cosmeticos = transformacion_datos(df_cosmeticos)
print(df_cosmeticos.head(5).to_string())

# Visualización de datos y análisis estadístico
grafico_cajas_columna(df_cosmeticos, "Calificacion")
grafico_cajas_columna(df_cosmeticos, "Total_calificadores")
grafico_cajas_columna(df_cosmeticos, "Precio_Euros")
correlacion_variables(df_cosmeticos)
grafico_frecuencia_marcas(df_cosmeticos)
grafico_proporcion_tipo_piel(df_cosmeticos)
grafico_densidad_columna(df_cosmeticos, "Calificacion")
grafico_densidad_columna(df_cosmeticos, "Total_calificadores")
grafico_densidad_columna(df_cosmeticos, "Precio_Euros")

#Carga de datos en base de datos
cargar_df_a_staging(nombre_bd,df_cosmeticos,nombre_tabla_staging)
script_generar_mondelo_y_carga_datos(ruta_script_sql)
generar_modelo_a_partir_de_sql(nombre_bd, ruta_script_sql)
