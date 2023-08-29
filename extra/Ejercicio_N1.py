# Programar una función que reciba como input una lista de 12 números y calcule la resta de cada número contra todos los numeros anteriores. El output de la función debe ser la mayor diferencia encontrada y si es <= 0, devuelve 0.

# Inputs
lst=[50,1,27,0,20,40,0,0,0,0,0,0]
lst2=[12,11,10,9,8,7,6,5,4,3,2,1]
lst3=[1,70,5,70,87,0,0,0,0,6,1,81]

# Resultados
# 40 0 86

#----- Ejercicio resuelto en vivo --------------------------------------------------------------------------------------------------------------

def mayor_diferencia1(lst):
    '''debolvera la mayor diferencia entre la lista

    Args:
        lst ([int]): lista que contiene numeros

    Returns:
        m (int): Maxima diferencia hayada
    '''

    lis_l = len(lst)                                # Calcula la longitud de la lista 'lst' y almacena el valor en la variable 'lis_l'

    m = 0                                           # Inicializa la variable 'm' con el valor 0, que se usará para almacenar la mayor diferencia encontrada

    for i in range(1, lis_l, 1):                    # Itera a través de los índices de la lista 'lst', comenzando desde el segundo elemento (índice 1)
        
        for j in range(0, i, 1):                    # Itera a través de los índices anteriores a 'i' (índices 0 a 'i-1')
            dif = lst[i] - lst[j]                   # Calcula la diferencia entre el elemento en el índice 'i' y el elemento en el índice 'j'
            
            if dif > m:
                m = dif                             # Si la diferencia calculada es mayor que el valor actual de 'm', actualiza 'm' con la nueva diferencia
    return m                                        # Devuelve el valor máximo de diferencia encontrado en el bucle

print('40: ', mayor_diferencia1(lst))               # imprimimos el resultado 1
print('0: ', mayor_diferencia1(lst2))               # imprimimos el resultado 2
print('86: ', mayor_diferencia1(lst3), '\n')        # imprimimos el resultado 3

#----- Ejercicio resuelto ----------------------------------------------------------------------------------------------------------------------

def mayor_diferencia2(lst):
    '''Devuelve la mayor diferencia entre la lista

    Args:
        lst (list): Lista que contiene números

    Returns:
        max_diff (int): Maxima diferencia hayada
    '''

    max_diff = 0                                    # inicializamos la mayor diferencia como 0
    min_num = lst[0]                                # inicializamos el valor mínimo con el primer número de la lista
    
    for num in lst[1:]:                             # iteramos a través de los números de la lista, comenzando desde el segundo número
        diff = num - min_num                        # calculamos la diferencia con el valor mínimo actual

        if diff > max_diff:                         # Si la diferencia calculada es mayor que la mayor diferencia actual, actualizamos max_diff
            max_diff = diff

        if num < min_num:                           # Si el número actual es menor que el valor mínimo actual, actualizamos min_num
            min_num = num

    return max_diff                                 # Devolvemos la mayor diferencia

print('40: ', mayor_diferencia2(lst))               # imprimimos el resultado 1
print('0: ', mayor_diferencia2(lst2))               # imprimimos el resultado 2
print('86: ', mayor_diferencia2(lst3))              # imprimimos el resultado 3
