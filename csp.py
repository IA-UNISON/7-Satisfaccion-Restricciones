#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
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


class GrafoRestriccion(object):
    """
    Clase abstracta para hacer un grafo de restricción 

    """

    def __init__(self):
        """
        Inicializa las propiedades del grafo de restriccón

        """
        self.dominio = {}
        self.vecinos = {}
        self.backtracking = 0  # Solo para efectos de comparación

    def restriccion(self, (xi, vi), (xj, vj)):
        """
        Verifica si se cumple la restriccion binaria entre las variables xi
        y xj cuando a estas se le asignan los valores vi y vj respectivamente.

        @param xi: El nombre de una variable
        @param vi: El valor que toma la variable xi (dentro de self.dominio[xi]
        @param xj: El nombre de una variable
        @param vj: El valor que toma la variable xi (dentro de self.dominio[xj]

        @return: True si se cumple la restricción

        """ 
        raise NotImplementedError("Método a implementar")

def asignacion_grafo_restriccion(gr, ap={}, consist=1, dmax=None, traza=False) :
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
    if dmax == None:  #  Ajusta la máxima produndidad de búsqueda
        dmax = len(gr.dominio) 
    
    if traza:
        print (len(gr.dominio) - dmax) * '\t', ap

    if set(ap.keys()) == set(gr.dominio.keys()):  #  Asignación completa
        return ap.copy()
    
    var = selecciona_variable(gr, ap)

    for val in ordena_valores(gr, ap, var):

        dominio = consistencia(gr, ap, var, val, consist)

        if dominio is not None:
            for variable in dominio:
                for valor in dominio[variable]:
                    gr.dominio[variable].remove(valor)
            ap[var] = val
            
            apn = asignacion_grafo_restriccion(gr, ap, consist, dmax - 1, traza)

            if apn is not None:
                return apn
            else:
                del ap[var]
                for variable in dominio:
                    gr.dominio[variable] += dominio[variable] 
    gr.backtracking += 1
    return None

def selecciona_variable(gr, ap):
    if len(ap) == 0:
        return max(gr.dominio.keys(), key=lambda v:gr.vecinos[v])
    return min([var for var in gr.dominio.keys() if var not in ap],
               key=lambda v:len(gr.dominio[v]))
    
def ordena_valores(gr, ap, xi):
    def conflictos(vi):
        acc = 0
        for xj in gr.vecinos[xi]:
            if xi not in ap:
                for vj in gr.dominio[xj]:
                    if not gr.restriccion((xi, vi), (xj, vj)):
                        acc += 1
        return acc
    return sorted(gr.dominio[xi], key=conflictos, reverse=True)

def consistencia(gr, ap, xi, vi, tipo):
    if tipo == 0:
        for (xj, vj) in ap.iteritems():
            if xj in gr.vecinos[xi] and not gr.restriccion((xi, vi), (xj, vj)):
                return None
        return {}

    dominio = {}
    if tipo == 1:
        for xj in gr.vecinos[xi]:
            if xj not in ap:
                dominio[xj] = []
                for vj in gr.dominio[xj]:
                    if not gr.restriccion((xi, vi), (xj, vj)):
                        dominio[xj].append(vj)
                if len(dominio[xj]) == len(gr.dominio[xj]):
                    return None
        return dominio
    if tipo == 2:
        for xj in gr.vecinos[xi]:
            if xj not in ap:
                dominio[xj] = []
                for vj in gr.dominio[xj]:
                    if not gr.restriccion((xi, vi), (xj, vj)):
                        dominio[xj].append(vj)
                if len(dominio[xj]) == len(gr.dominio[xj]):
                    return None
        return dominio
        raise NotImplementedError("AC-3  a implementar")
        #================================================
        #   Implementar el algoritmo de AC3
        #   y probarlo con las n-reinas
        #================================================

def min_conflictos(gr, rep=100, maxit=100):
    for _ in xrange(maxit):
        a = minimos_conflictos(gr, rep)
        if a is not None:
            return a
    return None

def minimos_conflictos(gr, rep=100):
    #================================================
    #   Implementar el algoritmo de minimos conflictos
    #   y probarlo con las n-reinas
    #================================================
    #variables = gr.vecinos[0] + gr.vecinos[1][0:1]
    asignacion = { var : var for var in gr.dominio[0] }
    print asignacion
    for i in xrange(rep):

        #Iteramos sobre las variables en la asignacion
        
        for variable in asignacion:

            #Definimos variables para determinar cuales son los valores con los menores conflictos

            conflicto_menor = -1
            dict_valores = {}

            #Iteramos sobre todos los valores posibles en el dominio de la variable actual

            for valor in gr.dominio[variable]:
                conflictos = 0
                #Verificamos las restricciones que tienen las variables con sus vecinos

                for vecino in gr.vecinos[variable]:
                    if not gr.restriccion((variable, valor), (vecino, asignacion[vecino])):
                        conflictos+=1
                #Actualizamos cual es el menor conflicto actual hasta ahora

                if(conflicto_menor == -1 or conflictos < conflicto_menor):
                    conflicto_menor = conflictos
                #Metemos los conflictos generados por cada vecino en un diccionario

                dict_valores[valor] =conflictos
            #selecciones los valores minimos de la lista de conflictos

            lista_valores = [y for y in dict_valores if dict_valores[y]==conflicto_menor]
            #asignamos un valor al azar entre las opciones disponibles

            asignacion[variable] = random.choice(lista_valores)

    return asignacion
    raise NotImplementedError("Minimos conflictos  a implementar")
