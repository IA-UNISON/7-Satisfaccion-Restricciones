#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
csp.py
------------

Implementación de los algoritmos más clásicos para el problema
de satisfacción de restricciones. Se define formalmente el
problema de satisfacción de restricciones y se desarrollan los
algoritmos para solucionar el problema por búsqueda.

En particular se implementan los algoritmos de forward checking y
el de arco consistencia. Así como el algoritmo de min-conflics.

En este modulo no es necesario modificar nada.

"""

__author__ = 'juliowaissman'

from collections import deque
import random

class GrafoRestriccion(object):
    """
    Clase abstracta para hacer un grafo de restricción

    El grafo de restricción se representa por:

    1. dominio: Un diccionario cuyas llaves son las variables (vertices)
                del grafo de restricción, y cuyo valor es un conjunto
                (objeto set en python) con los valores que puede tomar.

    2. vecinos: Un diccionario cuyas llaves son las variables (vertices)
                del grafo de restricción, y cuyo valor es un conjunto
                (objeto set en python) con las variables con las que
                tiene restricciones binarias.

    3. restriccion: Un método que recibe dos variables y sus respectivos
                    valores y regresa True/False si la restricción se cumple
                    o no.

    """

    def __init__(self):
        """
        Inicializa las propiedades del grafo de restriccón

        """
        self.dominio = {}
        self.vecinos = {}
        self.backtracking = 0  # Solo para efectos de comparación

    def restriccion(self, xi_vi, xj_vj):
        """
        Verifica si se cumple la restriccion binaria entre las variables xi
        y xj cuando a estas se le asignan los valores vi y vj respectivamente.

        @param xi: El nombre de una variable
        @param vi: El valor que toma la variable xi (dentro de self.dominio[xi]
        @param xj: El nombre de una variable
        @param vj: El valor que toma la variable xi (dentro de self.dominio[xj]

        @return: True si se cumple la restricción

        """
        xi, vi = xi_vi
        xj, vj = xj_vj
        #FALTAESTO
        #raise NotImplementedError("Método a implementar")


def asignacion_grafo_restriccion(gr, ap={}, consist=1, traza=False):
    """
    Asigación de una solución al grafo de restriccion si existe
    por búsqueda primero en profundidad.

    Para utilizarlo con un objeto tipo GrafoRestriccion gr:
    >>> asignacion = asignacion_grafo_restriccion(gr)

    @param gr: Un objeto tipo GrafoRestriccion
    @param ap: Un diccionario con una asignación parcial
    @param consist: Un valor 0, 1 o 2 para máximo grado de consistencia
    @param dmax: Máxima profundidad de recursión, solo por seguridad
    @param traza: Si True muestra el proceso de asignación

    @return: Una asignación completa (diccionario con variable:valor)
             o None si la asignación no es posible.

    """

    #  Checa si la asignación completa y devuelve el resultado de ser el caso
    if set(ap.keys()) == set(gr.dominio.keys()):
        return ap.copy()

    # Selección de variables, el código viene más adelante
    var = selecciona_variable(gr, ap)

    # Los valores se ordenan antes de probarlos
    for val in ordena_valores(gr, ap, var):

        # Función con efecto colateral, en dominio
        # si no es None, se tiene los valores que se
        # redujeron del dominio del objeto gr. Al salir
        # del ciclo for, se debe de restaurar el dominio
        dominio_reducido = consistencia(gr, ap, var, val, consist)

        if dominio_reducido is not None:
            # Se realiza la asignación de esta variable
            ap[var] = val

            # Solo para efectos de impresión
            if traza:
                print(((len(ap) - 1) * '\t') + "{} = {}".format(var, val))

            # Se manda llamar en forma recursiva (búsqueda en profundidad)
            apn = asignacion_grafo_restriccion(gr, ap, consist, traza)

            # Restaura el dominio
            for v in dominio_reducido.keys():
                gr.dominio[v] = gr.dominio[v].union(dominio_reducido[v])

            # Si la asignación es completa revuelve el resultado
            if apn is not None:
                return apn
            del ap[var]
    gr.backtracking += 1
    return None


def selecciona_variable(gr, ap):
    """
    Selecciona la variable a explorar, para usar dentro de
    la función asignacion_grafo_restriccion

    @param gr: Objeto tipo GrafoRestriccion
    @param ap: Un diccionario con una asignación parcial

    @return: Una variable de gr.dominio.keys()

    """
    # Si no hay variables en la asignación parcial, se usa el grado heurístico
    if len(ap) == 0:
        return max(gr.dominio.keys(), key=lambda v: len(gr.vecinos[v]))
    # Si hay variables, entonces se selecciona
    # la variable con el dominio más pequeño
    return min([var for var in gr.dominio.keys() if var not in ap],
               key=lambda v: len(gr.dominio[v]))


def ordena_valores(gr, ap, xi):
    """
    Ordena los valores del dominio de una variable de acuerdo
    a los que restringen menos los dominios de las variables
    vecinas. Para ser usada dentro de la función
    asignacion_grafo_restriccion.

    @param gr: Objeto tipo GrafoRestriccion
    @param ap: Un diccionario con una asignación parcial
    @param xi: La variable a ordenar los valores

    @return: Un generador con los valores de gr.dominio[xi] ordenados

    """
    def conflictos(vi):
        return sum((1 for xj in gr.vecinos[xi] if xj not in ap
                    for vj in gr.dominio[xj]
                    if gr.restriccion((xi, vi), (xj, vj))))
    return sorted(list(gr.dominio[xi]), key=conflictos, reverse=True)


def consistencia(gr, ap, xi, vi, tipo):
    """
    Calcula la consistencia y reduce el dominio de las variables, de
    acuerdo al grado de la consistencia. Si la consistencia es:

        0: Reduce el dominio de la variable en cuestión
        1: Reduce el dominio de la variable en cuestion
           y las variables vecinas que tengan valores que
           se reduzcan con ella.
        2: Reduce los valores de todas las variables que tengan
           como vecino una variable que redujo su valor. Para
           esto se debe usar el algoritmo AC-3.

    @param gr: Objeto tipo GrafoRestriccion
    @param ap: Un diccionario con una asignación parcial
    @param xi: La variable a ordenar los valores
    @param vi: Un valor que puede tomar xi

    @return: Un diccionario con el dominio que se redujo (como efecto
             colateral), a gr.dominio

    """
    # Primero reducimos el dominio de la variable de interes si no tiene
    # conflictos con la asignación previa.
    dom_red = {}
    for (xj, vj) in ap.items():
        if xj in gr.vecinos[xi] and not gr.restriccion((xi, vi), (xj, vj)):
            return None
    dom_red[xi] = {v for v in gr.dominio[xi] if v != vi}
    gr.dominio[xi] = {vi}

    # Tipo 1: lo claramente sensato
    # Se ve raro la forma en que lo hice pero es para dejar mas fácil
    # el desarrollo del algoritmo de AC-3,  y dejar claras las diferencias.
    if tipo == 1:
        pendientes = deque([(xj, xi) for xj in gr.vecinos[xi] if xj not in ap])
        while pendientes:
            xa, xb = pendientes.popleft()
            temp = reduceAC3(xa, xb, gr)
            if temp:
                if not gr.dominio[xa]:
                    gr.dominio[xa] = temp
                    for v in dom_red.keys():
                        gr.dominio[v] = gr.dominio[v].union(dom_red[v])
                    return None
                if xa not in dom_red:
                    dom_red[xa] = set({})
                    dom_red[xa] = dom_red[xa].union(temp)


    # Tipo 2: lo ya no tan claramente sensato
    # Al no estar muy bien codificado desde el punto de vista de eficiencia
    # puede tardar mas (el doble) que la consistencia tipo 1 pero debe de
    # generar mucho menos backtrackings.
    #
    # Por ejemplo, para las 4 reinas deben de ser 0 backtrackings y para las
    # 101 reina, al rededor de 4
    if tipo == 2:
        # Initial domains are made consistent with unary constraints.
        # 'worklist' contains all arcs we wish to prove consistent or not.
        pendientes = deque([(xj, xi) for xj in gr.vecinos[xi] if xj not in ap])
        while pendientes:
            x, y = pendientes.popleft()
            temp = reduceAC3(x, y, gr)
            if temp:
                if not gr.dominio[x]:
                    gr.dominio[x] = temp
                    for v in dom_red.keys():
                        gr.dominio[v] = gr.dominio[v].union(dom_red[v])
                    return None
                if x not in dom_red:
                    dom_red[x] = set({}) #se esta agregando la llave x en el diccionario
                dom_red[x] = dom_red[x].union(temp)
                for z in gr.vecinos[x]:
                   if z != y:
                     pendientes.append([z, x])
    return dom_red

def reduceAC3(xa, xb, gr):
    reduccion = set([])
    valores_xa = list(gr.dominio[xa])
    for va in valores_xa:
        for vb in gr.dominio[xb]:
            if gr.restriccion((xa, va), (xb, vb)):
                break
        else:
            reduccion.add(va)
            gr.dominio[xa].discard(va)
    return reduccion


def min_conflictos(gr, rep=1, maxit=1):
    for _ in range(maxit):
        a = minimos_conflictos(gr, rep)
        if a is not None:
            return a
    return None


def minimos_conflictos(gr, rep=1):
    """
    The M IN -C ONFLICTS algorithm for solving CSPs by local search. The initial
    state may be chosen randomly or by a greedy assignment process that chooses a minimal-
    conflict value for each variable in turn. The C ONFLICTS function counts the number of
    constraints violated by a particular value, given the rest of the current assignment."""

    current={}
    for i in gr.dominio:
        #se elije una posicion aleatoria en el tablero de las n-reinas
        aux=random.randint(0,len(gr.dominio[0])-1)
        current[i]=aux

    for j in range(rep):
        #elijo una llave al azar del diccionario current
        #print("current inicial: ",current)
        var=random.randint(0,len(gr.dominio)-1)
        print(current)
        #shouffle entre las llaves de asignacion
        #si es solucion entonces se devuelve esta
        if isSolucion(var,current,gr):
            return current
        #si tiene conflictos entonces se va a minimizar la asignacion a traves de minimizar los conflictos de las reinas en los renglones
        min=conflictos(var,current,gr)
        #despues solo se le da como nueva solucion para la asignacion actual
        current[var]=min
        #print("current final: ", current)
    return None

def isSolucion(var,current,gr):
    aux = 0
    for i in range(0,len(gr.dominio)):
        #se checa si la llave actual tiene conflictos con todas las remas reinas en el tablero
        print(var)
        if not gr.restriccion((current[var],var),(current[i],i)):
            aux+=1
                #return False
    print("aux",aux)
    if(aux!=0):
        return False
    else:
        print("es solucion")
        return True

def conflictos(var,current,gr):
    l=[]
    for i in range(len(gr.dominio)):
            #inicializo un contador para checar el numero de conflictos de la reina actual
            num_restriccion = 0
            for k in range(len(gr.dominio)):
                #print((current[var],var),(current[i],i))
                if not gr.restriccion((current[var],k),(current[i],i)) and i!=k:
                    num_restriccion+=1
            l.append(num_restriccion)
    print(l)
            #se guarda el numero de restricciones de la la posicion de la reina
    menor = l[0]
    for i in range(0,len(l)):
      if l[i]<menor:
        menor=i

    return menor