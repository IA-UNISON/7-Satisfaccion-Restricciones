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

from collections import deque, defaultdict
import random
from pprint import pprint


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
        self.respaldos = []
        self.backtracking = 0  # Solo para efectos de comparación

    def respaldar_dominio(self):
        respaldo = self.copiar_dominio()
        self.respaldos.append(respaldo)

    def restaurar_dominio(self):
        respaldo = self.respaldos.pop()
        self.dominio = respaldo

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
        raise NotImplementedError("Método a implementar")


def asignacion_grafo_restriccion(gr, ap=None, consist=1, traza=False):
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
    if ap is None:
        ap = {}

    # print('a profundidad', len(ap))

    if len(ap) == len(gr.dominio):
        return ap.copy()

    var = selecciona_variable(gr, ap)
    for val in ordena_valores(gr, ap, var):
        consistente, reducciones = consistencia(gr, ap, var, val, consist)
        if consistente:
            ap[var] = val
            if traza:
                print(((len(ap) - 1) * '\t') + "{} = {}".format(var, val))
            result = asignacion_grafo_restriccion(gr, ap, consist, traza)
            if result:
                return result
            del ap[var]
        for x, d in reducciones.items():
            gr.dominio[x] |= d
    gr.backtracking += 1
    return None


def selecciona_variable(gr, ap):
    if len(ap) == 0:
        return max(gr.dominio.keys(), key=lambda v: gr.vecinos[v])
    return min([var for var in gr.dominio.keys() if var not in ap],
               key=lambda v: len(gr.dominio[v]))


def ordena_valores(gr, ap, xi):
    def conflictos(vi):
        return sum((1 for xj in gr.vecinos[xi] if xj not in ap
                    for vj in gr.dominio[xj]
                    if gr.restriccion((xi, vi), (xj, vj))))
    return sorted(gr.dominio[xi], key=conflictos, reverse=True)


def consistencia(gr, ap, xi, vi, tipo):
    reducciones = defaultdict(set)

    for x, v in ap.items():
        if x in gr.vecinos[xi] and not gr.restriccion((xi, vi), (x, v)):
            return False, reducciones

    reducciones[xi] = gr.dominio[xi] - {vi}
    gr.dominio[xi] = {vi}

    if tipo == 1:
        for x in gr.vecinos[xi]:
            if (x not in ap and
                revisar(gr, reducciones, x, xi) and
                not gr.dominio[x]):
                return False, reducciones

    if tipo == 2:
        # ================================================
        #    Implementar el algoritmo de AC3
        #    y probarlo con las n-reinas
        # ================================================
        cola = deque((x, y) for x in gr.dominio for y in gr.vecinos[x])
        while cola:
            x, y = cola.popleft()
            if revisar(gr, reducciones, x, y):
                if not gr.dominio[x]:
                    return False, reducciones
                cola.extend((z, x) for z in gr.vecinos[x] if z != y)
    return True, reducciones


def revisar(gr, reducciones, x, y):
    r = set(v for v in gr.dominio[x]
            if not any(gr.restriccion((x, v), (y, w)) for w in gr.dominio[y]))

    gr.dominio[x] -= r
    reducciones[x] |= r

    return len(r) != 0


def min_conflictos(gr, rep=1000, maxit=10):
    for i in range(maxit):
        a = minimos_conflictos(gr, rep)
        if a is not None:
            return a
    return None


def calcular_n_conflictos(gr, asignacion, x, v):
    return sum(1 for xi in gr.vecinos[x] if not gr.restriccion((x, v), (xi, asignacion[xi])))


def minimos_conflictos(gr, rep=100):
    # ================================================
    #    Implementar el algoritmo de minimos conflictos
    #    y probarlo con las n-reinas
    # ================================================
    a = {x: random.choice(list(v)) for (x, v) in gr.dominio.items()}
    for _ in range(rep):
        conflictos = {x: calcular_n_conflictos(gr, a, x, a[x]) for x in a}

        if not sum(conflictos.values()):
            return a

        x = random.choice([i for i in conflictos if conflictos[i]])

        x_c = {v: calcular_n_conflictos(gr, a, x, v) for v in gr.dominio[x]}
        c_min = min(x_c.values())
        a[x] = random.choice([v for v in x_c if x_c[v] == c_min])
    return None
