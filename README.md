# Cosmetics_Popularity_Analysis

Analysis of Popularity and Usage of Cosmetic Products

  

## Proceso de Instalacion

  

* Importar este repositorio con git clone

* Crear un enviromnent en base al archivo environment.yml con el siguiente comando:
	* `conda env create -f environment.yml -n Analisis_Cosmeticos`
* Activar el entorno con el comando:
	* `conda activate Analisis_Cosmeticos`
* Antes de ejecutar revisar las variables globales de rutas de exportación de archivos scripts y base de datos en el archivo mai.py
* Ejecutar el programa principal desde bash con el comando: `pyton main.py`

## Descripción del programa

Este programa realiza las siguientes tareas:

### Extracción:
Realiza la extracción de datos de productos cosméticos para el cuidado de la piel de la web de primor usando selenium
Luego exporta los datos a un archivo .csv que es importado a un dataframe para su posterior análisis

### Exploración
Realiza una exploración de la data cruda importada para analizar los datos a limpiar y transformas

### Limpieza y transformación
Elimina los datos nulos y convierte los datos numéricos al formato adecuado para poder realizar un análisis estadístico adecuado.

### Visualizaciones
A partir de los datos se generan visualizaciones de:
* distribución de los datos numéricos
* Matriz de correlación
* Frecuencia de marcas
* Densidad de datos en columnas numéricas
* Proporción de tipos de piel
``
### Inferencia Estadística
También se han realizado pruebas de hipótesis de las variables para verificar hipótesis nulas y alternativas de:
* Semejanza en calificaciones de dos categorías de productos
* Correlación entre precio y calificación de los productos

### Carga de Datos a un Modelo Estrella en SQLite
El programa realiza los siguientes pasos para generar el modelo estrella  y cargar los datos.
* Crea la base de datos en SQLite y copia el dataframe a una tabla staging
* Genera un archivo .sql con las instrucciones para crear las tablas, las correlaciones del modelo estrella y cargar los datos a partir de la tabla staging
* Ejecuta el script .sql para generar el modelo estrella y cargar los datos que servirán para crear las visualizaciones en Power BI


### Visualización en PowerBI

Las visualizaciones se realizaron en PowerBI se puede descargar el archivo en la ruta: [Visualizaciones/Análisis_productos_piel_Primor.pbix](https://github.com/Zenialuz/Cosmetics_Popularity_Analysis/tree/main/Visualizaciones  "Visualizaciones/Análisis_productos_piel_Primor.pbix")