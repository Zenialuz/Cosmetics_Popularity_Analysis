import sqlite3
import os

def cargar_df_a_staging(ruta_bd, df_cosmeticos, tabla_destino):
    
    # Extraer solo la parte del path correspondiente a las carpetas (sin el archivo)
    folder_path = os.path.dirname(ruta_bd)

    # Crear las carpetas si no existen
    os.makedirs(folder_path, exist_ok=True)
    
    # Validar si la base de datos ya existe la eliminará
    if os.path.exists(ruta_bd): 
        os.remove(ruta_bd)
        print(f"Base de datos {ruta_bd} eliminada porque ya existía.")
    
    # Conexión a la base de datos SQLite
    conexion = sqlite3.connect(ruta_bd)

    # Guardar el dataframe completo tal como está
    df_cosmeticos.to_sql(tabla_destino, conexion, if_exists='replace', index=False)
    
    conexion.close()
    print(f"Datos cargados en la tabla {tabla_destino} de la base de datos {ruta_bd}")

def script_generar_mondelo_y_carga_datos(ruta_script_sql): 
    sql_script = """
    -- TABLA DE DIMENSIÓN: MARCA
    CREATE TABLE dim_marca (
        id_marca INTEGER PRIMARY KEY,
        marca VARCHAR(255)
    );
    INSERT INTO dim_marca (marca, id_marca)
    SELECT marca, ROW_NUMBER() OVER () AS id_marca
    FROM (
        SELECT DISTINCT Marca AS marca
        FROM staging_data
    ) AS t;

    -- TABLA DE DIMENSIÓN: CATEGORÍA
    CREATE TABLE dim_categoria (
        id_categoria INTEGER PRIMARY KEY,
        categoria VARCHAR(255)
    );
    INSERT INTO dim_categoria (categoria, id_categoria)
    SELECT categoria, ROW_NUMBER() OVER () AS id_categoria
    FROM (
        SELECT DISTINCT Categoria AS categoria
        FROM staging_data
    ) AS t;
    
    
    -- TABLA DE DIMENSIÓN: GRUPO TIPO DE PIEL
    CREATE TABLE dim_grupo_tipo_piel (
        id_grupo_tipo_piel INTEGER PRIMARY KEY,
        grupo_tipo_piel VARCHAR(255)
    );
    INSERT INTO dim_grupo_tipo_piel (grupo_tipo_piel, id_grupo_tipo_piel)
    SELECT grupo_tipo_piel, ROW_NUMBER() OVER () AS id_grupo_tipo_piel
    FROM (
        SELECT DISTINCT Grupo_Tipo_piel AS grupo_tipo_piel
        FROM staging_data
    ) AS t;
    
    -- TABLA DE DIMENSIÓN: TIPO DE PIEL
    CREATE TABLE dim_tipo_piel (
        id_tipo_piel INTEGER PRIMARY KEY,
        id_grupo_tipo_piel INTEGER,
        tipo_piel VARCHAR(255),
        FOREIGN KEY (id_grupo_tipo_piel) REFERENCES dim_grupo_tipo_piel(id_grupo_tipo_piel)
    );
    INSERT INTO dim_tipo_piel (tipo_piel, id_tipo_piel, id_grupo_tipo_piel)
    SELECT tipo_piel, ROW_NUMBER() OVER () AS id_tipo_piel, id_grupo_tipo_piel
    FROM (
        SELECT DISTINCT st.Tipo_piel AS tipo_piel, gtp.id_grupo_tipo_piel
        FROM staging_data AS st
        JOIN dim_grupo_tipo_piel AS gtp ON st.Grupo_Tipo_piel = gtp.grupo_tipo_piel
    ) AS t;

    -- TABLA DE DIMENSIÓN: ZONA DE APLICACIÓN
    CREATE TABLE dim_zona_aplicacion (
        id_zona INTEGER PRIMARY KEY,
        zona_aplicacion VARCHAR(255)
    );
    INSERT INTO dim_zona_aplicacion (zona_aplicacion, id_zona)
    SELECT zona_aplicacion, ROW_NUMBER() OVER () AS id_zona
    FROM (
        SELECT DISTINCT Zona_aplicacion AS zona_aplicacion
        FROM staging_data
    ) AS t;

    -- TABLA DE DIMENSIÓN: PRODUCTO
    CREATE TABLE dim_producto (
        id_producto INTEGER PRIMARY KEY,
        nombre_producto VARCHAR(255)
    );
    INSERT INTO dim_producto (nombre_producto, id_producto)
    SELECT nombre_producto, ROW_NUMBER() OVER () AS id_producto
    FROM (
        SELECT DISTINCT Descripcion AS nombre_producto
        FROM staging_data
    ) AS t;
    
    -- TABLA DE DIMENSIÓN: TIPO DE PRODUCTO
    CREATE TABLE dim_tipo_producto (
        id_tipo_producto INTEGER PRIMARY KEY,
        tipo_producto VARCHAR(255)
        );
    INSERT INTO dim_tipo_producto (tipo_producto, id_tipo_producto)
    SELECT tipo_producto, ROW_NUMBER() OVER () AS id_tipo_producto
    FROM (
        SELECT DISTINCT Tipo_producto AS tipo_producto
        FROM staging_data
    ) AS t;

    -- TABLA DE HECHOS: PRODUCTOS
    CREATE TABLE hechos_productos (
        id_marca INTEGER,
        id_categoria INTEGER,
        id_tipo_piel INTEGER,
        id_zona INTEGER,
        id_producto INTEGER,
        id_tipo_producto INTEGER,
        Calificacion REAL,
        Total_calificadores INTEGER,
        Calificacion_final REAL,
        Precio_Euros REAL,
        FOREIGN KEY (id_marca) REFERENCES dim_marca(id_marca),
        FOREIGN KEY (id_categoria) REFERENCES dim_categoria(id_categoria),
        FOREIGN KEY (id_tipo_piel) REFERENCES dim_tipo_piel(id_tipo_piel),
        FOREIGN KEY (id_zona) REFERENCES dim_zona_aplicacion(id_zona),
        FOREIGN KEY (id_producto) REFERENCES dim_producto(id_producto),
        FOREIGN KEY (id_tipo_producto) REFERENCES dim_tipo_producto(id_tipo_producto)
    );

    -- INSERTAR DATOS EN LA TABLA DE HECHOS
    INSERT INTO hechos_productos (
        id_marca, id_categoria, id_tipo_piel, id_zona, id_producto, id_tipo_producto,
        Calificacion, Total_calificadores, Calificacion_final, Precio_Euros
    )
    SELECT
        m.id_marca,
        c.id_categoria,
        tp.id_tipo_piel,
        z.id_zona,
        d.id_producto,
        t.id_tipo_producto,
        r.Calificacion,
        r.Total_calificadores,
        r.Calificacion_final,
        r.Precio_Euros
    FROM staging_data r
    JOIN dim_marca m ON r.Marca = m.marca
    JOIN dim_categoria c ON r.Categoria = c.categoria
    JOIN dim_tipo_piel tp ON r.Tipo_piel = tp.tipo_piel
    JOIN dim_zona_aplicacion z ON r.Zona_aplicacion = z.zona_aplicacion
    JOIN dim_producto d ON r.Descripcion = d.nombre_producto
    JOIN dim_tipo_producto t ON r.Tipo_producto = t.tipo_producto;

    """
     # Extraer solo la parte del path correspondiente a las carpetas (sin el archivo)
    folder_path = os.path.dirname(ruta_script_sql)

    # Crear las carpetas si no existen
    os.makedirs(folder_path, exist_ok=True)
    
    with open(ruta_script_sql, 'w', encoding='utf-8') as f:
        f.write(sql_script)
    
    print(f"Script SQL generado en {ruta_script_sql}")
    
    
def generar_modelo_a_partir_de_sql(ruta_bd, ruta_script_sql):
    
    # validamos si existe la base de datos
    
    
    # Conexión a la base de datos SQLite
    conexion = sqlite3.connect(ruta_bd)
    with open(ruta_script_sql, 'r', encoding='utf-8') as f:
        sql = f.read()

    cursor = conexion.cursor()
    cursor.executescript(sql)
    conexion.commit()
    conexion.close()
    print("------------------------------------------------------")
    print(f"Modelo generado y datos cargados en la base de datos {ruta_bd} desde el script {ruta_script_sql}")
    print("------------------------------------------------------")