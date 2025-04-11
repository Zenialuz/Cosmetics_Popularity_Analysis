# Importando librerías necesarias
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
import os

def connect_and_get_html(url):
    # ------------- Configurando Selenium -------------------------
    # Configuración de opciones para el navegador
    # Se utiliza ChromeDriverManager para instalar y gestionar el controlador de Chrome automáticamente. 
    
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Ejecutar en modo headless (opcional)
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    html = False # Inicializamos html como False para manejar el caso de error
    
    # Obteniendo la URL
    driver.get(url)
    
    # Verificando si existe el div con la clase "message info empty"
    try:
        empty_message = driver.find_element(By.CLASS_NAME, "message.info.empty")
        print(f"No hay productos en la página: {url}")
        driver.quit()
        return False
    except NoSuchElementException:
        # Si no se encuentra el div "message info empty", continuar con el scraping
        pass
    
    for attempt in range(3):  # Intentar hasta 3 veces
        try:
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            driver.get(url)
            
            try:
                # Configurar WebDriverWait con sondeo personalizado e ignorar excepciones
                wait = WebDriverWait(driver, 15, poll_frequency=0.2, ignored_exceptions=[NoSuchElementException])
                
                # Esperar hasta que el elemento dinámico esté presente
                element = wait.until(
                    EC.presence_of_element_located((By.CLASS_NAME, "pr-stars"))
                )
                print("Elemento encontrado:", element.get_attribute("style"))
                
                # Obtener el HTML renderizado
                html = driver.page_source
            except TimeoutException:
                print("El elemento 'pr-stars' no se cargó en el tiempo esperado.")
                driver.quit()
                return False
            finally:
                driver.quit()
            
            break  # Salir del bucle si tiene éxito
        except Exception as e:
            print(f"Error en intento {attempt + 1}: {e}")
            time.sleep(5)  # Esperar antes de reintentar
        finally:
            driver.quit()

    return html

def scraping_pagina(url, output_df, categoria, tipo_piel, zona_aplicacion):
    
    # Conectar y obtener el HTML de la página
    html = connect_and_get_html(url)
    
    if not html:
        print(f"No se pudo obtener el HTML de la página: {url}")
        return output_df        
    
    # Usar BeautifulSoup para analizar el HTML
    soup = BeautifulSoup(html, "html.parser")
    
    # Buscar todos los <li> dentro de un <ul>
    lista_items = soup.find_all("li")
    
    # Listas para almacenar los datos extraídos
    marcas_producto = []
    descripciones_producto = []
    calificaciones_producto = []
    total_calificadores = []
    precios_producto = []
    categorias_producto = []
    tipos_piel = []
    zonas_aplicacion = []
    
    for li in lista_items:
        # Buscar <form> dentro del <li>
        form = li.find("form")
        if form:
            
            categorias_producto.append(categoria)
            tipos_piel.append(tipo_piel)
            zonas_aplicacion.append(zona_aplicacion)
            
            # Buscar <div> con la clase específica dentro del <form>
            div = form.find("div", class_="text-sm font-bold uppercase")
           
            marcas_producto.append(div.get_text(strip=True) if div else None)  # Extraer el texto del <div> o agregar un valor nulo si no existe
            
            # Buscar <a> con la clase específica dentro del <form>
            a = form.find("a", class_="product-item-link inline-block text-sm leading-4")
            descripciones_producto.append(a.get_text(strip=True) if a else None)  # Extraer el texto del <a> o agregar un valor nulo si no existe
            
            # Buscar <span> con la clase específica para precios
            span_precio = form.find("span", class_="price-wrapper")
            precios_producto.append(span_precio.get_text(strip=True) if span_precio else None)  # Extraer el texto del <span> o agregar un valor nulo si no existe
    
            # Buscar <div> con la clase específica para calificaciones
            div2 = form.find("div", class_="pr-stars")
            if div2:
                calificaciones_producto.append(div2.get("style"))  # Extraer el atributo 'style'
                span = div2.find("span")
                total_calificadores.append(span.get_text(strip=True) if span else None)
            else:
                calificaciones_producto.append(None)  # Si no hay <div>, agregar un valor nulo
                total_calificadores.append(None)
            
            
    # Crear un DataFrame con las columnas
    precios_producto = [precio.replace("€", "").replace(",", ".").strip() if precio else None for precio in precios_producto]
    df = pd.DataFrame({
        "marca": marcas_producto,
        "descripcion": descripciones_producto,
        "calificacion": calificaciones_producto,
        "total_calificadores": total_calificadores,
        "precio": precios_producto,
        "categoria": categorias_producto,
        "tipo_piel": tipos_piel,
        "zona_aplicacion": zonas_aplicacion
    })
    
    #Concatenamos los resultados de la página actual con los resultados de las páginas anteriores
    output_df = pd.concat([output_df, df], ignore_index=True)
    return output_df


def sraping_webSite(categorias, tipos_de_piel, zonas_aplicacion, output_csv):
    output_df = pd.DataFrame(columns=["marca", "descripcion", "calificacion", "total_calificadores", "precio", "categoria", "tipo_piel","zona_aplicacion"])
    
    
    # Recorrer las categorías y tipos de piel
    for categoria, url_categoria in categorias:
        print(f"\nCategoría: {categoria}")
        
        for tipo_piel, codigo in tipos_de_piel:
            print(f"\n  Tipo de piel: {tipo_piel}")
            for zona, codigo_zona in zonas_aplicacion:
                print(f"\n   Zona de aplicación: {zona}")
                
                for pagina in range(1, 3):  # Cambia el rango según el número de páginas que se va recorrer
                    # Concatenar el código del tipo de piel como parámetro en la URL
                    url_con_parametro = f"{url_categoria}?tipo_piel={codigo}&zona_cara={codigo_zona}&p={pagina}"
                    print(f"    URL: {url_con_parametro}")
            
                    output_df = scraping_pagina(url_con_parametro, output_df, categoria, tipo_piel, zona)
                
        if output_df is None or output_df.empty:
            print(f"Advertencia: No se encontraron datos para la categoría {categoria}.")
        else:             
            output_df.to_csv(output_csv, mode='w', header=True, index=False, encoding="utf-8")
            print(f"Datos exportados a {output_csv}")
        
    return output_df    

def carga_csv(data_csv):
    
    # Verificar si el archivo CSV existe
    if not os.path.exists(data_csv):
        raise FileNotFoundError(f"El archivo {data_csv} no existe.")
    
    # Cargar el archivo CSV en un DataFrame
    df_cosmeticos = pd.read_csv(data_csv, sep=",", encoding="utf-8")
    print("------------------------------------------------------")
    print(f"Se han cargado {len(df_cosmeticos)} filas del archivo CSV.")
    print("------------------------------------------------------")
    return df_cosmeticos