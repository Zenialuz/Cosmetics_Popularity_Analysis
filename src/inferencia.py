from scipy.stats import ttest_ind
from scipy.stats import pearsonr


def hipotesis_comparacion_categorias(df_cosmeticos):
    

    # Hipotesis planteada: Las calificaciones de los productos de las categorías 
    # "Hidratantes y Nutrivas" y "Antiarrugas y antiedad" son iguales.
    print("\n----------------------------------------------")
    print("Hipótesis nula: Las calificaciones son iguales.")
    print("Hipótesis alternativa: Las calificaciones son diferentes.")
    print("----------------------------------------------")
    cat1 = "Hidratantes y Nutrivas"
    cat2 = "Antiarrugas y antiedad"

    grupo1 = df_cosmeticos[df_cosmeticos["Categoria"] == cat1]["Calificacion"]
    grupo2 = df_cosmeticos[df_cosmeticos["Categoria"] == cat2]["Calificacion"]

    # Prueba t
    t_stat, p_value = ttest_ind(grupo1, grupo2, equal_var=False)  # Welch’s t-test

    print(f"t = {t_stat:.3f}, p = {p_value:.3f}")
    if p_value < 0.05:
        print("Rechazamos la hipótesis nula: hay diferencia significativa.")
    else:
        print("No se rechaza la hipótesis nula: no hay diferencia significativa.")
        

def hipotesis_correlacion_variables(df_cosmeticos):      

    # Validando, si las calificaciones de los productos dependen del precio
    # Hipostesis: "Las calificaciones estan relacionadas con los precios de los productos"
    print("\n----------------------------------------------")
    print("Hipótesis nula: Las calificacione están correlacionadas con los precios.")
    print("Hipótesis alternativa: Las calificacione no están correlacionadas con los precios.")
    print("----------------------------------------------")

    r, p = pearsonr(df_cosmeticos["Precio_Euros"], df_cosmeticos["Calificacion"])
    print(f"Coeficiente de correlación: r = {r:.3f}, p = {p:.3f}")

    if p < 0.05:
        print("Rechazamos H₀: hay una correlación significativa.")
    else:
        print("No se rechaza H₀: no hay correlación significativa.")   