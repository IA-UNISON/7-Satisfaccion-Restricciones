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
        raise NotImplementedError("AC-3  a implementar")
        #================================================
        #   Implementar el algoritmo de AC3
        #   y probarlo con las n-reinas
        #================================================
        
"""# Constraint Propagation with AC-3
def AC3(csp, queue=None, removals=None):
    if queue is None:
        queue = [(Xi, Xk) for Xi in csp.vars for Xk in csp.neighbors[Xi]]
    csp.support_pruning()
    while queue:
        (Xi, Xj) = queue.pop()
        if revise(csp, Xi, Xj, removals):
            if not csp.curr_domains[Xi]:
                return False
            for Xk in csp.neighbors[Xi]:
                if Xk != Xi:
                    queue.append((Xk, Xi))
    return True
    
def revise(csp, Xi, Xj, removals):
    "Return true if we remove a value."
    revised = False
    for x in csp.curr_domains[Xi][:]:
        # If Xi=x conflicts with Xj=y for every possible y, eliminate Xi=x
        if every(lambda y: not csp.constraints(Xi, x, Xj, y),
                 csp.curr_domains[Xj]):
            csp.prune(Xi, x, removals)
            revised = True
    return revised
"""
def revise(csp, Xi, Xj, removals):
    "Return true if we remove a value."
    revised = False
    for x in csp.curr_domains[Xi][:]:
        # If Xi=x conflicts with Xj=y for every possible y, eliminate Xi=x
        if every(lambda y: not csp.constraints(Xi, x, Xj, y),
                 csp.curr_domains[Xj]):
            csp.prune(Xi, x, removals)
            revised = True
    return revised


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

    asignacion = {var: random.choice(gr.dominio[var]) for var in gr.dominio.keys()}

    suma_conflictos = lambda xi, vi: sum([1 for xj in gr.vecinos[xi]
                                          if not gr.restriccion_binaria((xi, vi), (xj, asignacion[xj]))])

    for _ in range(rep):
        gr.backtracking += 1
        conflictos = {xi: suma_conflictos(xi, vi) for (xi, vi) in asignacion.iteritems()}

        if sum(conflictos.values()) == 0:
            return asignacion

        xi = random.choice([var for var in conflictos if conflictos[var] > 0])
        for vi in gr.dominio[xi]:
            c_acc = suma_conflictos(xi, vi)
            if c_acc < conflictos[xi] or (c_acc == conflictos[xi] and random.random() > 0.5):
                asignacion[xi] = vi
                conflictos[xi] = c_acc
    return None

    #raise NotImplementedError("Minimos conflictos  a implementar")
