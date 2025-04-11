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


def grafico_cajas_columna(df_cosmeticos, columna): 
    # Boxplot para la columna 'Calificacion'
    plt.figure(figsize=(6, 4))
    sns.boxplot(data=df_cosmeticos, y=columna, color='skyblue')
    plt.title("Boxplot de "+columna, fontsize=14)
    plt.ylabel(columna, fontsize=12)
    plt.xlabel("")
    plt.show()
    
def correlacion_variables(df_cosmeticos): 
    # Generar el mapa de calor de correlación
    plt.figure(figsize=(10, 6))
    # Seleccionar solo las columnas numéricas para calcular la matriz de correlación
    correlacion = df_cosmeticos.select_dtypes(include=['float64', 'int64']).corr()
    sns.heatmap(correlacion, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)

    # Personalizar el título
    plt.title("Mapa de Calor de Correlación", fontsize=16)
    plt.show()
    
def grafico_frecuencia_marcas(df_cosmeticos): 
    import plotly.express as px

    # Obtener los datos de las 10 marcas más frecuentes
    top_marcas = df_cosmeticos['Marca'].value_counts().head(10).reset_index()
    top_marcas.columns = ['Marca', 'Frecuencia']

    # Crear el gráfico de barras interactivo
    fig = px.bar(
        top_marcas,
        x='Marca',
        y='Frecuencia',
        title="Top 10 Marcas Más Frecuentes",
        labels={'Frecuencia': 'Frecuencia', 'Marca': 'Marca'},
        #text='Frecuencia'  # Mostrar los valores en las barras
    )

    # Personalizar el diseño
    fig.update_traces(textposition='outside', marker_color='purple')
    fig.update_layout(
        xaxis_title="Marca",
        yaxis_title="Frecuencia",
        title_font_size=30,
        xaxis_tickangle=45
    )

    # Mostrar el gráfico
    fig.show()
    
def grafico_proporcion_tipo_piel(df_cosmeticos): 
    # Calcular la proporción de tipos de piel
    tipo_piel_data = df_cosmeticos['Tipo_piel'].value_counts(normalize=True).reset_index()
    tipo_piel_data.columns = ['Tipo_piel', 'Proporción']

    # Crear el gráfico de pastel interactivo
    fig = px.pie(
        tipo_piel_data,
        names='Tipo_piel',
        values='Proporción',
        title="Proporción de productos por Tipos de Piel",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )

    # Personalizar el diseño
    fig.update_traces(
        textinfo='none',  # Quitar etiquetas numéricas de las porciones
        hovertemplate='%{label}: %{percent}',  # Mostrar valores en porcentaje al pasar el mouse
    )

    fig.update_layout(title_font_size=16)

    # Mostrar el gráfico
    fig.show()

def grafico_densidad_columna(df_cosmeticos, columna): 
    # Gráfico de densidad para la columna
    sns.kdeplot(data=df_cosmeticos, x=columna, fill=True, color='orange')
    plt.title("Densidad de "+ columna, fontsize=14)
    plt.xlabel(columna)
    plt.show()