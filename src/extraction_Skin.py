
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import os
import csv
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from PIL import Image
from io import BytesIO
import html

def scrapear_imagenes_istock(url, initial_page=1, max_pages=5, carpeta_destino="images", archivo_csv="imagenes_dataset.csv", tipo_piel=""):
   
    # Configurar opciones de Chrome en modo headless
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=chrome_options)

    # base_url = "https://www.istockphoto.com/es/search/more-like-this/1010039320?assettype=image&page={}"
    base_url = url
    
    # Verificar si el archivo ya existe
    archivo_existe = os.path.exists(archivo_csv)

    if not os.path.exists(carpeta_destino):
        os.makedirs(carpeta_destino)

    with open(archivo_csv, mode="a", newline='', encoding="utf-8") as f:
        fieldnames = ["image_url", "filename", "description", "tipo_piel"]
        writer = csv.DictWriter(f, fieldnames=fieldnames, quotechar='"', quoting=csv.QUOTE_ALL)
        
        # Si el archivo no existía, escribir la cabecera
        if not archivo_existe:
            writer.writeheader()
     
    for page in range(initial_page, initial_page + max_pages):
        url = base_url.format(page)
        print(f"Procesando la página {page}: {url}...")
        driver.get(url)
        time.sleep(5)
        html_rendered = driver.page_source
        soup = BeautifulSoup(html_rendered, "html.parser")
        images = soup.find_all("img", class_="PnVbv5qRe5ya18jbe2Gt")
        print(f"Página {page}: se encontraron {len(images)} imágenes.")

        for idx, img in enumerate(images):
            src_raw = img.get("src")
            if not src_raw:
                print(f"Imagen {idx} en página {page}: sin 'src'.")
                continue

            img_url = html.unescape(src_raw)
            if not img_url.startswith("http"):
                img_url = urljoin(url, img_url)

            alt_text = img.get("alt", "")
            if ".svg" in img_url:
                print(f"Imagen {idx} en página {page}: es un SVG, omitida.")
                continue

            try:
                print(f"Descargando imagen {idx} en página {page}: {img_url}...")
                img_response = requests.get(img_url)
                if img_response.status_code == 200:
                    image = Image.open(BytesIO(img_response.content)).convert("RGB")
                    image = image.resize((500, 500))
                    filename = f"imagen_{page}_{idx}.jpg"
                    file_path = os.path.join(carpeta_destino, filename)
                    image.save(file_path, "JPEG")
                    print(f"Imagen guardada: {filename}")
                        

                    with open(archivo_csv, mode="a", newline='', encoding="utf-8") as f:
                        writer = csv.DictWriter(f, fieldnames=["image_url", "filename", "description", "tipo_piel"], quotechar='"', quoting=csv.QUOTE_ALL)
                        writer.writerow({
                            "image_url": img_url,
                            "filename": filename,
                            "description": alt_text,
                            "tipo_piel" : tipo_piel
                        })
                else:
                    print(f"Error descargando imagen: {img_url} - Código: {img_response.status_code}")
            except Exception as e:
                print(f"Error procesando imagen: {img_url} - Error: {e}")

    driver.quit()
    print(f"Proceso completado. Imágenes guardadas en '{carpeta_destino}' y datos en '{archivo_csv}'.")


