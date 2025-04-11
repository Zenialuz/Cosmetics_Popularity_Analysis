import pandas as pd


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
    
    # Limpiando la columna 'calificacion'
    df_cosmeticos['calificacion'] = df_cosmeticos['calificacion'].str.replace(r'^--stars:', '', regex=True).astype(float)

    # Limpiando la columna 'total_calificadores'
    df_cosmeticos['total_calificadores'] = df_cosmeticos['total_calificadores'].str.replace(r'[()]', '', regex=True)
    
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
    
    print("\n------------------------------------------------------")
    print("Información del DataFrame después de la transformación:")
    print("------------------------------------------------------")
    df_cosmeticos.info()    
    
    return df_cosmeticos