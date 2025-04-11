
def exploracion_data(df_cosmeticos):
    print("\n------------------------------------")
    print("Descripción de los datos")
    df_cosmeticos.describe()

def exploracion_por_categoria(df_cosmeticos): 
    # Segmentación por categoría
    for categoria, grupo in df_cosmeticos.groupby('categoria'):
        print("\n------------------------------------")
        print(f"Análisis para la categoría: {categoria}")
        print("\n------------------------------------")
        print(grupo[['calificacion', 'precio']].describe())