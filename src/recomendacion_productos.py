import pandas as pd
import sqlite3

def get_categoria_producto(ruta_bd):
    # Conexión a la base de datos SQLite
    conexion = sqlite3.connect(ruta_bd)

    # Leer la tabla de categorías
    df_categorias = pd.read_sql_query("SELECT * FROM dim_categoria", conexion)

    conexion.close()
    
    return df_categorias

def get_tipos_producto(ruta_bd):
    # Conexión a la base de datos SQLite
    conexion = sqlite3.connect(ruta_bd)

    # Leer la tabla de tipos de producto
    df_tipos_producto = pd.read_sql_query("SELECT * FROM dim_tipo_producto", conexion)

    conexion.close()
    
    return df_tipos_producto
def get_zona_aplicacion(ruta_bd):
    # Conexión a la base de datos SQLite
    conexion = sqlite3.connect(ruta_bd)

    # Leer la tabla de zonas de aplicación
    df_zonas_aplicacion = pd.read_sql_query("SELECT * FROM dim_zona_aplicacion", conexion)

    conexion.close()
    
    return df_zonas_aplicacion

def top10_productos(ruta_bd, grupo_tipo_piel, categoria, tipo_producto, zona_aplicacion):
# Conexión a la base de datos SQLite
    conexion = sqlite3.connect(ruta_bd)

    df_cosmeticos = pd.read_sql_query("SELECT * FROM staging_data WHERE Categoria = '" + categoria + "' AND Tipo_producto = '" + tipo_producto + "' AND zona_aplicacion = '" + zona_aplicacion + "'", conexion)

    conexion.close()
    
    # Obtener los top 10 productos con mayor calificación final para el grupo de tipo de piel especificado
    df_top_productos = df_cosmeticos[df_cosmeticos['Grupo_tipo_piel'] == grupo_tipo_piel].nlargest(10, 'Calificacion_final')
    df_top_productos['Descripcion'] = df_top_productos.apply(
        lambda row: f'<a href="{row["Url_producto"]}" target="_blank">{row["Descripcion"]}</a>', axis=1
    )
    df_top_productos = df_top_productos[['Marca', 'Descripcion', 'Categoria','Tipo_piel', 'Zona_aplicacion','Calificacion', 'Total_calificadores', 'Calificacion_final','Tipo_producto', 'Precio_Euros']]
    
    return df_top_productos

