import pandas as pd
import numpy as np


def limpieza_datos(df_cosmeticos):
    # Mostrar información del DataFrame antes de la limpieza
    print("\n------------------------------------------------------")
    print("Información del DataFrame antes de la limpieza:")
    print("------------------------------------------------------")
    df_cosmeticos.info()
    
    # Nos aseguramos de trabajar sobre una copia del dataframe original
    df_cosmeticos = df_cosmeticos.copy()
    
    # Eliminar filas donde 'calificacion' o 'total_calificadores' son nulos:
    df_cosmeticos = df_cosmeticos.dropna(subset=['calificacion', 'total_calificadores'])

    # Convertir la columna "precio" a tipo numérico
    df_cosmeticos["precio"] = pd.to_numeric(df_cosmeticos["precio"], errors="coerce")
    
    # Eliminar filas con valores nulos en la columna "precio"
    df_cosmeticos.dropna(subset=["precio"])
    
    # Convertir url a texto
    df_cosmeticos['url_producto'] = df_cosmeticos['url_producto'].astype(str)
    #eliminar columna url_prouducto en caso exista
    if 'url_prouducto' in df_cosmeticos.columns:
        df_cosmeticos = df_cosmeticos.drop(columns=['url_prouducto'])
    
    # Limpiando la columna 'calificacion'
    df_cosmeticos['calificacion'] = df_cosmeticos['calificacion'].str.replace(r'^--stars:', '', regex=True).astype(float)

    # Limpiando la columna 'total_calificadores'
    df_cosmeticos['total_calificadores'] = df_cosmeticos['total_calificadores'].str.replace(r'[()]', '', regex=True)
    
    # Eliminando filas dulplicadas
    df_cosmeticos = df_cosmeticos.drop_duplicates()
    
    # Verificar el resultado
    print("\n------------------------------------------------------")
    print("Información del DataFrame después de la limpieza:")
    print("------------------------------------------------------")
    df_cosmeticos.info()
    
    return df_cosmeticos

def transformacion_datos(df_cosmeticos):
    
    # Capitalizar la primera letra de los nombres de las columnas
    df_cosmeticos.columns = df_cosmeticos.columns.str.capitalize()

    # renombrando la columna 'Precio' a 'Precio (€)'
    df_cosmeticos = df_cosmeticos.rename(columns={'Precio': 'Precio_Euros'})

    # Convirtiendo las columnas numéricas a los tipos de datos adecuados
    df_cosmeticos['Calificacion'] = df_cosmeticos['Calificacion'].astype(float)
    df_cosmeticos['Precio_Euros'] = df_cosmeticos['Precio_Euros'].astype(float)
    df_cosmeticos['Total_calificadores'] = df_cosmeticos['Total_calificadores'].astype(int)
    df_cosmeticos = get_calificacion_final(df_cosmeticos)
    
    print("\n------------------------------------------------------")
    print("Información del DataFrame después de la transformación:")
    print("------------------------------------------------------")
    df_cosmeticos.info()    
    
    return df_cosmeticos

# Transformación de datos para calcular la calificación ponderada Bayesiana

def get_calificacion_final(df_cosmeticos):
   
    # Promedio global de todas las calificaciones
    C = df_cosmeticos['Calificacion'].mean()

    # Mínimo de votos para ser considerado "confiable"
    #m = df_cosmeticos['Total_calificadores'].quantile(0.90)  # puedes ajustar este valor
    m=100
    print(f"m = {m}")

    
    # Crear nueva columna con la calificación final usando lambda
    df_cosmeticos['Calificacion_final'] = df_cosmeticos.apply(
        lambda row: weighted_rating(row, m, C), axis=1
    )


    # Ajustar la calificación final con un factor logarítmico para suavizar el efecto de los votos
    # Esto ayuda a evitar que productos con pocos votos tengan una calificación final muy alta
    df_cosmeticos['Calificacion_final'] = df_cosmeticos['Calificacion_final'] * np.log10(df_cosmeticos['Total_calificadores'] + 1)

    # Ajustando las calificacioenes finales para que estén en un rango de 0 a 5
    # Obtener el valor máximo de la columna Calificacion_final
    max_val = df_cosmeticos['Calificacion_final'].max()

    # Normalizar la columna al rango 0–5
    df_cosmeticos['Calificacion_final'] = (df_cosmeticos['Calificacion_final'] / max_val) * 5


    # Obtener las cremas top ordenadas por la calificación final
    top_creams = df_cosmeticos.sort_values(by='Calificacion_final', ascending=False)

    
    return df_cosmeticos

# Función para calcular la calificación ponderada Bayesiana
def weighted_rating(row, m, C):
    v = row['Total_calificadores']
    R = row['Calificacion']
    return (v / (v + m)) * R + (m / (v + m)) * C