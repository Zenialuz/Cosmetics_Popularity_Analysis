from src.extraction import sraping_webSite, carga_csv
from src.exploration import exploracion_data, exploracion_por_categoria
from src.transformation import limpieza_datos
from src.transformation import transformacion_datos
from src.visualizacion import grafico_cajas_columna, correlacion_variables, grafico_frecuencia_marcas,grafico_proporcion_tipo_piel,grafico_densidad_columna
from src.loadModel import cargar_df_a_staging, script_generar_mondelo_y_carga_datos,generar_modelo_a_partir_de_sql
from src.inferencia import hipotesis_comparacion_categorias, hipotesis_correlacion_variables
from src.extraction_Skin import scrapear_imagenes_istock
from src.skin_type_classifier import train_model

###############################################
# Configuración de variables globales
###############################################

# Ruta de archivo para guardar y obtener los datos en csv
data_csv = "data/Primor/data_primor.csv"

nombre_bd = 'data/modelo_copo_nieve/modelo_copo_nieve.db'
nombre_tabla_staging = 'staging_data'
ruta_script_sql = 'data/modelo_copo_nieve/script_carga_datos_modelo_copo_nieve.sql'

# Lista de url de las categorías de productos
categorias = [
        ("Hidratantes y Nutrivas", "https://www.primor.eu/es_es/hidratantes-y-nutritivas-lujo"),
        ("Antiarrugas y antiedad", "https://www.primor.eu/es_es/antiarrugas-y-antiedad-lujo"),
        #("Contorno de Ojos", "https://www.primor.eu/es_es/contorno-de-ojos-lujo"),
        #("Tratamientos especificos", "https://www.primor.eu/es_es/tratamientos-especificos-lujo"),
        # ("limpiadoras tonicos", "https://www.primor.eu/es_es/limpiadoras-tonicos-lujo"),
        # ("labios balsamos y cuidados", "https://www.primor.eu/es_es/labios-balsamos-y-cuidados-lujo"),
        ("Antimanchas", "https://www.primor.eu/es_es/antimanchas-lujo")       
        # ("Tratamientos calmantes", "https://www.primor.eu/es_es/tratamientos-calmantes-y-para-piel-sensible")
    ]
categorias_comun = [
        ("Hidratantes y Nutrivas", "https://www.primor.eu/es_es/cremas-hidratantes-faciales"),
        ("Antiarrugas y antiedad", "https://www.primor.eu/es_es/cremas-antiarrugas-y-antiedad"),
        #("Contorno de Ojos", "https://www.primor.eu/es_es/cremas-contorno-de-ojos"),
        # ("Desmaquillantes", "https://www.primor.eu/es_es/desmaquillantes"),
        ("Antimanchas", "https://www.primor.eu/es_es/cremas-faciales-antimanchas")
        #("Serums", "https://www.primor.eu/es_es/serums"),
        # ("Limpieza facial", "https://www.primor.eu/es_es/limpieza-facial")
    ]

# Lista de parámetros de tipos de piel para construir la url de los productos
tipos_de_piel = [
        ("Normal", 66101),
        ("Deshidratada", 66094),
        # ("Sensible", 66110), 
        ("Todo tipo de piel", 66111),
        ("Madura", 66097),
        ("Muy seca", 66100),
        ("seca", 66107),
        ("Grasa", 66096)
        # ("Mixta", 66098),
        # ("Mixta a Grasa", 66099),
        # ("Normal a seca", 66104),
        # ("seca-muy seca", 66109),
        # ("seca - mixta", 66108),
        # ("atopica", 66092),
        # ("Delicadas", 66093),
        # ("Apagadas", 66091)
    ]

 # Lista de parámetros de zonas de aplicación para construir la url de los productos   
zonas_aplicacion = [        
        ("Rostro", 66325),
        ("Cuerpo", 66309)
        # ("Manos", 66315),
        # ("Ojos", 66319),
        # ("Cuello", 66308)     
    ]

url_imagenes_piel = [
        ("Madura", "https://www.istockphoto.com/es/search/more-like-this/1010039320?assettype=image&excludenudity=false&phrase=piel%20adulto%20mayor&page={}"),
        ("Grasa", "https://www.istockphoto.com/es/search/more-like-this/1010039320?assettype=image&excludenudity=false&phrase=piel%20grasa&page={}"),
        ("Sensible", "https://www.istockphoto.com/es/search/more-like-this/1010039320?assettype=image&excludenudity=false&phrase=piel%20sensible&page={}"),
        ("Seca", "https://www.istockphoto.com/es/search/more-like-this/1010039320?assettype=image&excludenudity=false&phrase=piel%20seca&page={}"),
        ("Deshidratada", "https://www.istockphoto.com/es/search/more-like-this/1010039320?assettype=image&excludenudity=false&phrase=piel%20deshidratada&page={}"),
        ("Normal", "https://www.istockphoto.com/es/search/more-like-this/1010039320?assettype=image&excludenudity=false&phrase=piel%20sana&page={}")
    ]
# Obtención de datos usando Selenium y BeautifulSoup para scrapear (Para ejecución de scraping descomentar la siguiente línea)
#df_primor = sraping_webSite(categorias, tipos_de_piel, zonas_aplicacion, data_csv, "lujo")
#print(df_primor.head(5))

#df_primor_comun = sraping_webSite(categorias_comun, tipos_de_piel, zonas_aplicacion, data_csv, "comun")
#print(df_primor_comun.head(5))

# Scraping de imágenes de iStock (Para ejecución de scraping descomentar la siguiente línea)

# for url_imagen in url_imagenes_piel:
#     tipo_piel = url_imagen[0]
#     url = url_imagen[1]
#     scrapear_imagenes_istock(url, initial_page=1, max_pages=2, carpeta_destino="images/" + tipo_piel, archivo_csv="data/imagenes/imagenes_dataset.csv", tipo_piel=tipo_piel)


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
grafico_cajas_columna(df_cosmeticos, "Calificacion_final")
grafico_cajas_columna(df_cosmeticos, "Precio_Euros")
correlacion_variables(df_cosmeticos)
grafico_frecuencia_marcas(df_cosmeticos)
grafico_proporcion_tipo_piel(df_cosmeticos)
grafico_densidad_columna(df_cosmeticos, "Calificacion")
grafico_densidad_columna(df_cosmeticos, "Total_calificadores")
grafico_densidad_columna(df_cosmeticos, "Calificacion_final")
grafico_densidad_columna(df_cosmeticos, "Precio_Euros")

# Inferencia Estadistica
hipotesis_comparacion_categorias(df_cosmeticos)
hipotesis_correlacion_variables(df_cosmeticos)

#Carga de datos en base de datos
cargar_df_a_staging(nombre_bd,df_cosmeticos,nombre_tabla_staging)
script_generar_mondelo_y_carga_datos(ruta_script_sql)
generar_modelo_a_partir_de_sql(nombre_bd, ruta_script_sql)

# Entrenamiento del modelo de clasificación de tipos de piel
train_model()