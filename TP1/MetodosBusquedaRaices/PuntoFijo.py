import sys
from TP1.MetodosBusquedaRaices.Biseccion import biseccion
from sympy import *
import math


# Debe recibir una funcion dada en expresion de simpy, con variable x
def funcion_es_continua_en_intervalo(f, variable_ppal, intervalo):

    esContinua = true

    for i in range(intervalo[0], intervalo[1]):
        try:
            limite_der = limit(f, variable_ppal, i, '+')
            limite_izq = limit(f, variable_ppal, i, '-')
            f_evaluable = lambdify(symbols('x'),f)
            f_evaluada = f_evaluable(i)
            limite  = limit(f, variable_ppal, i)

            if(
                    limite_der != limite_izq or
                    f_evaluada != limite
            ):
                esContinua = false
        except:
            print("Oops! Ocurrio un problema al buscar continuidad", sys.exc_info()[0])
            esContinua = false
    return  esContinua


def funcion_contenida_intervalo(g, variable_ppal, intervalo, distancia_entre_x):
    i = intervalo[0]
    g_evaluable = lambdify(variable_ppal, g)
    esta_contenida = true
    while i <= intervalo[1]:

        if(g_evaluable(i) <  intervalo[0] or g_evaluable(i) > intervalo[1]):
            esta_contenida = false
            break
        i += distancia_entre_x

    return esta_contenida



def derivada_acotada_en_intervalo(g, variable_ppal, intervalo, distancia_entre_x):
    esta_acotada = true
    g_prima = g(variable_ppal).diff(variable_ppal)
    g_prima_evaluabe = lambdify(variable_ppal,g_prima)
    i = intervalo[0]
    cota_mayor = - math.inf
    cota_menor = math.inf

    while i <= intervalo[1]:
        valor = g_prima_evaluabe(i)
        if(valor > cota_mayor):
            cota_mayor = valor
        if(valor < cota_menor):
            cota_menor = valor
        if(max(abs(cota_menor), abs(cota_mayor) > 1 or max(abs(cota_menor), abs(cota_mayor) < 0 ))):
            esta_acotada = false
            break
        i += distancia_entre_x

    return esta_acotada



def existe_unico_p_fijo(g,variable_ppal, intervalo):

    if not(funcion_es_continua_en_intervalo(g, variable_ppal, intervalo) or
           funcion_contenida_intervalo(g, variable_ppal, intervalo, 0.5) or
           derivada_acotada_en_intervalo(g, variable_ppal, intervalo, 0.5)
    ):
        return false
    else:
        return true

def obtener_g(f):
    x = symbols('x')
    expresion = x - sympify(f)
    return expresion

def punto_fijo_rec(g, semilla, tolerancia, iteraciones) -> object:

    Pn = g(semilla)
    if abs(Pn <= tolerancia or iteraciones == 0):
        return semilla

    return punto_fijo_rec(g, Pn, tolerancia, iteraciones - 1)

def punto_fijo(f, intervalo, tolerancia, iteraciones):

    g = obtener_g(f)
    if(existe_unico_p_fijo(g,symbols('x'),intervalo)):
        semilla = biseccion(lambdify(symbols('x'), g), intervalo, tolerancia,2)
        print("La raiz hallada como semilla es: " + str(semilla))
        return punto_fijo_rec(lambdify(symbols('x'),g), semilla, tolerancia, iteraciones)
    else:
        return "No es posible aplicar punto fijo dada la falta de existencia y/o unicidad del punto fijo"


if __name__ == "__main__":

    print("la raiz hallada con p fijo es: " +  str(punto_fijo("1/x", (-1,1, 2), 1e-2, 200)))