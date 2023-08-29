import pandas as pd
from datetime import datetime
from ydata_profiling import ProfileReport

'''

Parte 1:
--------
    - Crear una columna nueva (ejemplo nombre tipo_ocupacion) e indicar la cantidad de personas con y sin ocupación.
    
    En base al dataset provisto cree una columna 'empleo_sl' que se base en la situacion laboral provista.
    Sin embargo, la mitad de los registros son: 'Sin_situacion_declarada'.
    Por lo que en base a los ingresos rellene esa categoría en la columna 'empleo_i'

'''

#----- Cargamos el dataset ---------------------------------------------------------------------------------------------------------------------

print('\n')

df1 = pd.read_csv('./raw data/Tabla1_ejercicio_N3.csv', sep=';')                            # cargamos el dataset
df1 = df1.drop_duplicates()                                                                 # eliminar duplicados

print(df1, '\n')                                                                            # visualizamos el dataset
print(df1.dtypes, '\n')                                                                     # verificar los tipos de datos
print(df1.isnull().sum(), '\n')                                                             # cantidad de null * col

#----- Creamos un EDA con pandas-profiling -----------------------------------------------------------------------------------------------------

profile = ProfileReport(df1)                                                                # generamos un EDA con pandas_profiling
profile.to_file("EDA.html")                                                                 # exportamos el reporte en HTML

'''

Conclusiones:
-------------
    El dataset no contenía valores nulos ni valores duplicados...

    - La empresa tiene el doble de clientes femeninas que masculinos.
    - La mayoria de sus clientes tienen mas de 40 años, aproximadamente del doble de sus clientes son mayores de 40 años en comparacion con los menores de 40 años. Aunque disminuyen coinsiderablemente luego de los 60 años.
    - El minimo ingreso es 5 mil y el maximo 850 mil. Lo que comprueba que hay clientes que tienen ingresos mas no trabajo. y la media es de 48 mil.
    - Hay una correlacion considerable entre sexo y edad. puede deverse a que los clientes de cierta edad sean hombres mientras que los de otra edad sean mujeres.

'''

#----- Empleo según la columna situacion_lab ---------------------------------------------------------------------------------------------------

df1['empleo_sl'] = df1['situacion_lab']                                                     # duplicamos 'situacion_lab' en 'empleo_sl' que contendra 0 y 1 

reemplazos = {                                                                              # creamos la variable reemplazos con las distintas variables a reemplazar por 0(desempleo) o 1(empleo)
    'Desempleado_o_plansocial': 0,                                                          # Desempleado_o_plansocial, como dice la palabra es desempleo
    'Jubilado': 0,                                                                          # Jubilado, no trabaja, por ende desempleo.
    'Autonomo_Monotributista': 1,                                                           # Autonomo o Monotributista, trabajan incluso siendo emprendedores, es trabajo
    'Relacion_dependencia': 1,                                                              # Relacion_dependencia, empleo por definicion
    'Sin_situacion_declarada': None                                                         # Sin_situacion_declarada, lo seteamos como null para rellenar en base a los ingresos
}

df1['empleo_sl'] = df1['empleo_sl'].replace(reemplazos)                                     # reemplazamos las categorias por empleo o desempleo
df1['empleo_sl'] = pd.to_numeric(df1['empleo_sl'], errors='coerce').astype(pd.Int64Dtype()) # Convertir la columna a tipo entero ignorando nulos

#----- Empleo según la columna ingresos --------------------------------------------------------------------------------------------------------

median = df1['ingreso'].median()                                                            # obtenemos la mediana de la columna 'ingreso'
print('El ingreso medio es de: ', int(median), '\n')                                        # imprimimos el ingreso medio                   

def Empleo_i(i):                                                                            # creamos una función para transformar los valores en 'empleo_i'
    if i < median / 2:
        return 0
    else:
        return 1

df1['empleo_i'] = df1.apply(lambda row: Empleo_i(row['ingreso']) if pd.isnull(row['empleo_sl']) else row['empleo_sl'], axis=1)  # aplicamos la función Empleo_i a la columna 'empleo_i' solo si los valores en 'empleo_sl' son nulos

#----- Cantidad de clientes con empleo y desempleados ------------------------------------------------------------------------------------------

cantidad_empleo = (df1['empleo_i'] == 1).sum()                                              # contamos los empleados en empleo_i
cantidad_desempleo = (df1['empleo_i'] == 0).sum()                                           # contamos los desempleados en empleo_i
print("Cantidad de clientes con empleo:", cantidad_empleo)                                  # imprimimos la cantidad de empleados
print("Cantidad de clientes desempleados:", cantidad_desempleo, '\n')                       # imprimimos la cantidad de desempleados

#----- Creamos la columna rango_etario ---------------------------------------------------------------------------------------------------------

def calcular_rango_etario(edad):                                                            # creamos una función para calcular el rango etario por décadas
    return f"{(edad // 10) * 10}-{((edad // 10) * 10) + 9}"                                 # redondeamos la edad a la década inferior
df1['rango_etario'] = df1['edad'].apply(calcular_rango_etario)                              # aplicamos la función

#----- Exportamos el dataset limpio ------------------------------------------------------------------------------------------------------------

df1.set_index('pers_id', inplace=True)                                                      # establecemos la columna 'Id' como índice
df1.to_csv('./data/Tabla1.csv')                                                             # exportamos el dataset en csv a /data
print(df1, '\n')                                                                            # imprimimos el dataset


#-----------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------
'''

Parte 2:
--------
    Teniendo en cuenta el periodo más reciente disponible para cada persona, crear una función que reciba como inputs:
        - Parámetro 1: datos input.
        - Parámetro 2: estadístico que se va a calcular.
        - Parámetro 3: variable a la que se va a aplicar el estadístico.
        - Parámetro 4: variable con la cual se va a agrupar.
    
    Y calcular:
        - Score promedio y mediana según categoría ocupacional.
        - Ingreso y Score máximo y promedio según sexo.

'''

#----- Cargar el 2do dataset -------------------------------------------------------------------------------------------------------------------

df2 = pd.read_csv('./raw data/Tabla2_ejercicio_N3.csv', sep=';')                            # cargamos el dataset
df2 = df2.drop_duplicates()                                                                 # eliminamos duplicados

print(df2, '\n')                                                                            # visualizamos el dataset
print(df2.dtypes, '\n')                                                                     # verificar los tipos de datos
print(df2.isnull().sum(), '\n')                                                             # cantidad de null * col

#----- Limpiar el 2do dataset ------------------------------------------------------------------------------------------------------------------

df2['periodo'] = df2['periodo'].astype(str)                                                 # convertimos 'periodo' en str
df2['periodo'] = df2['periodo'].apply(lambda x: datetime.strptime(x, '%Y%m'))               # convertimos 'periodo' a datetime

df2 = df2.sort_values(by=['pers_id', 'periodo'], ascending=[True, False])                   # ordenamos el df por 'pers_id' y 'periodo' en orden descendente
df2 = df2.groupby('pers_id').first().reset_index()                                          # mantenemos solo la primera fila para cada 'pers_id'

#----- Exportamos el 2do dataset ---------------------------------------------------------------------------------------------------------------

df2.set_index('pers_id', inplace=True)                                                      # establecemos la columna 'Id' como índice
df2.to_csv('./data/Tabla2.csv')                                                             # exportamos el dataset en csv a /data
print(df2, '\n')                                                                            # imprimimos el dataset

#----- Unimos los 2 datasets -------------------------------------------------------------------------------------------------------------------

df = pd.merge(df1, df2, on='pers_id', how='right')                                          # unimos los df con un 'right join' debido a que se nos pide: 'Teniendo en cuenta el periodo más reciente disponible'. Es decir, teniendo en cuenta el periodo.
df = df.drop('empleo_sl', axis=1)                                                           # eliminamos la columna 'empleo_sl'
df.rename(columns={'empleo_i': 'empleo'}, inplace=True)                                     # renombramos la columna 'empleo_i' a 'empleo'
df.to_csv('./data/Tabla.csv')                                                               # exportamos el dataset en csv a /data
print(df, '\n')                                                                             # imprimimos el dataset

#----- Creamos un 'dashboard' con pandas-profiling -----------------------------------------------------------------------------------------------------

profile = ProfileReport(df)                                                                 # generamos un dashboard con pandas_profiling
profile.to_file("./docs/conclusiones.html")                                                 # exportamos el reporte en HTML

#----- Crear la funcion solicitada -------------------------------------------------------------------------------------------------------------

def Calcular_Estadisticas(df, est, var1, var2):                                             # creamos la funcion que calculara los metodos estadisticos
    """
    funcion capaz de calcular metodos estadisticos por columna y valores agrupados en un dataset.

    Args:
        df (DataFrame): DataFrame con los datos.
        est (str): estadistico a calular ['mean', 'median', 'sum', 'std', 'var', 'count', 'sem', 'max', 'min'].
        var1 (str): variable a la que se va a aplicar el estadistico.
        var2 (str): variable con la cual se va a agrupar.
        bins (int or list of int, optional): Parámetro para binning (por ejemplo, para agrupar edades por décadas).

    Returns:
        DataFrame: Resultados de las estadísticas calculadas.
    """
    if est not in ['mean', 'median', 'sum', 'std', 'var', 'count', 'sem', 'max', 'min']:                                        # si el parametro 'est' no un estadistico correcto, retorna error
        raise ValueError("Estadístico debe ser: 'mean', 'median', 'sum', 'std', 'var', 'count', 'sem', 'max' o 'min'")

    if (var1 and var2) not in ['sexo', 'edad', 'rango_etario', 'ingreso', 'situacion_lab', 'empleo', 'periodo', 'score']:                       # si las variables no son las del dataset, retorna error
        raise ValueError("Las variables deben ser: 'sexo', 'edad', 'ingreso', 'situacion_lab', 'empleo', 'periodo' o 'score'")

    if var1 == var2:                                                                        # si las variables son iguales, retorna error
        raise ValueError("Las variables no pueden ser iguales")

    if est == 'max':                                                                        # calculamos el maximo
        grouped_data = df.groupby(var2)[var1].max().reset_index()
    elif est == 'min':                                                                      # calculamos el minimo
        grouped_data = df.groupby(var2)[var1].min().reset_index()
    else:                                                                                   # calculamos el estadistico seleccionado
        grouped_data = df.groupby(var2)[var1].agg([est]).reset_index()
    
    return grouped_data

#----- Obtener resultados ----------------------------------------------------------------------------------------------------------------------

result1 = Calcular_Estadisticas(df, 'mean', 'score', 'empleo')                              # calculamos el score promedio según empleo
result2 = Calcular_Estadisticas(df, 'median', 'score', 'empleo')                            # calculamos el score medio según empleo
result3 = Calcular_Estadisticas(df, 'max', 'ingreso', 'sexo')                               # calculamos el ingreso maximo según sexo
result4 = Calcular_Estadisticas(df, 'mean', 'ingreso', 'sexo')                              # calculamos el ingreso promedio según sexo
result5 = Calcular_Estadisticas(df, 'max', 'score', 'sexo')                                 # calculamos el score maximo según sexo
result6 = Calcular_Estadisticas(df, 'mean', 'score', 'sexo')                                # calculamos el score promedio según sexo
result7 = Calcular_Estadisticas(df, 'mean', 'edad', 'sexo')                                 # calculamos la edad promedio según sexo
result8 = Calcular_Estadisticas(df, 'mean', 'score', 'rango_etario')                        # calculamos el score promedio según rango_etario

print('score promedio según empleo:')
print(result1, '\n')                                                                        # imprimimos el score promedio según empleo
print('score medio según empleo:')
print(result2, '\n')                                                                        # imprimimos el score medio según empleo
print('ingreso maximo según sexo:')
print(result3, '\n')                                                                        # imprimimos el ingreso maximo según sexo
print('ingreso promedio según sexo:')
print(result4, '\n')                                                                        # imprimimos el ingreso promedio según sexo
print('score maximo según sexo:')
print(result5, '\n')                                                                        # imprimimos el score maximo según sexo
print('score promedio según sexo:')
print(result6, '\n')                                                                        # imprimimos el score promedio según sexo
print('edad promedio según sexo:')
print(result7, '\n')                                                                        # imprimimos la edad promedio según sexo
print('score promedio según rango_etario:')
print(result8, '\n')                                                                        # imprimimos el score promedio según rango_etario

#----- Las Conclusiones se encuentran en docs/conclusiones.md ----------------------------------------------------------------------------------