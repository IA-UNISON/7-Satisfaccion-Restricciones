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

    def restricción(self, xi_vi, xj_vj):
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

    if set(ap.keys()) == set(gr.dominio.keys()):
        #  Asignación completa
        return ap.copy()

    var = selecciona_variable(gr, ap)

    for val in ordena_valores(gr, ap, var):

        dominio = consistencia(gr, ap, var, val, consist)

        if dominio is not None:
            for variable in dominio:
                for valor in dominio[variable]:
                    gr.dominio[variable].remove(valor)
            ap[var] = val

            if traza:
                print(((len(ap) - 1) * '\t') + "{} = {}".format(var, val))

            apn = asignacion_grafo_restriccion(gr, ap, consist, traza)

            for variable in dominio:
                gr.dominio[variable] += dominio[variable]

            if apn is not None:
                return apn
            del ap[var]
    gr.backtracking += 1
    return None


def selecciona_variable(gr, ap):
    if len(ap) == 0:
        return max(gr.dominio.keys(), key=lambda v: gr.vecinos[v])
    return min([var for var in gr.dominio.keys() if var not in ap],
               key=lambda v: len(gr.dominio[v]))


def ordena_valores(gr, ap, xi):
    def conflictos(vi):
        acc = 0
        for xj in gr.vecinos[xi]:
            if xi not in ap:
                for vj in gr.dominio[xj]:
                    if not gr.restricción((xi, vi), (xj, vj)):
                        acc += 1
        return acc
    return sorted(gr.dominio[xi], key=conflictos, reverse=True)


def consistencia(gr, ap, xi, vi, tipo):
    if tipo == 0:
        for (xj, vj) in ap.iteritems():
            if xj in gr.vecinos[xi] and not gr.restricción((xi, vi), (xj, vj)):
                return None
        return {}

    dominio = {}
    if tipo == 1:
        for xj in gr.vecinos[xi]:
            if xj not in ap:
                dominio[xj] = []
                for vj in gr.dominio[xj]:
                    if not gr.restricción((xi, vi), (xj, vj)):
                        dominio[xj].append(vj)
                if len(dominio[xj]) == len(gr.dominio[xj]):
                    return None
        return dominio
    '''
    ESTE CODIGO DE WIKIPEDIA ES PERFECTO FACIL DE ENTENDERE Y MUY INTITUIVO
    APARTE DE ESTO EL PSEUDOCODIGO QUE SE MANEJA ES PRACTICAMENTE POCOS CAMBIOS
    A LA SINTAXIS DE PYTHON 2
    DEJO EL CODIGO Y LA REFERENCIA PARA FUTURAS GENERACIONES
    https://en.wikipedia.org/wiki/AC-3_algorithm
   Input:
   A set of variables X
   A set of domains D(x) for each variable x in X. D(x) contains vx0, vx1... vxn, the possible values of x
   A set of unary constraints R1(x) on variable x that must be satisfied
   A set of binary constraints R2(x, y) on variables x and y that must be satisfied

 Output:
   Arc consistent domains for each variable.

 function ac3 (X, D, R1, R2)
 // Initial domains are made consistent with unary constraints.
     for each x in X
         D(x) := { vx in D(x) | R1(x) }
     // 'worklist' contains all arcs we wish to prove consistent or not.
     worklist := { (x, y) | there exists a relation R2(x, y) or a relation R2(y, x) }

     do
         select any arc (x, y) from worklist
         worklist := worklist - (x, y)
         if arc-reduce (x, y)
             if D(x) is empty
                 return failure
             else
                 worklist := worklist + { (z, x) | z != y and there exists a relation R2(x, z) or a relation R2(z, x) }
     while worklist not empty

 function arc-reduce (x, y)
     bool change = false
     for each vx in D(x)
         find a value vy in D(y) such that vx and vy satisfy the constraint R2(x, y)
         if there is no such vy {
             D(x) := D(x) - vx
             change := true
         }
     return change'''
    if tipo == 2:
        worklist = {(j, xi) for j in gr.vecinos[xi]}
        dominio[xi] = set(gr.dominio[xi]) - {vi}
        while worklist:
            i, j = worklist.pop()
            #si no se puede reducir el arco continuamos con el siguiente
            if arc_reduce(gr, dominio, i, j):
                if dominio[i] and not set(gr.dominio[i]) - dominio[i]:
                    return None
                else:
                    worklist |= {(i, k) for k in gr.vecinos[i] if k != j }
        return dominio

def arc_reduce(gr, dominio, x, y):
    change = False
    remove = set()
    dominio_x = set(gr.dominio[x]) - (dominio[x] if x in dominio else remove)
    #produce todo el dominio de x y aqui abajo se procesa la reduccion
    for vx in dominio_x:
        flag = False
        dominio_y = set(gr.dominio[y]) - (dominio[y] if y in dominio else set())
        #produce todo el dominio de y y aqui abajo se procesa la reduccion
        for vy in dominio_y:
            if gr.restricción((x, vx), (y, vy)):
                flag = True
                break
        if not flag:
            remove.add(vx)
            change = True
    if change:
        dominio[x] = dominio[x] | remove if x in dominio else remove
        #aqui remuevo todo lo necesario del dominio
    return change


def min_conflictos(gr, rep=100, maxit=100):
    for _ in range(maxit):
        a = minimos_conflictos(gr, rep)
        if a is not None:
            return a
    return None


def minimos_conflictos(gr, rep=100):
    # ================================================
    #    Implementar el algoritmo de minimos conflictos
    #    y probarlo con las n-reinas
    # ================================================
    import random
    a = {i: random.choice(list(gr.dominio[i])) for i in gr.dominio}
    b = []
    for i in a.keys():
        for x in gr.vecinos[i]:#yo se que esto es muy poco elegante
            if not gr.restricción((i,a[i]), (x, a[x])):
                b.append(i)
                break
    for _ in range(rep):
        if not b:
            return a
        i = b.pop()
        #print(i)
        def contar_conflictos(gr, ap, xi, vi):
            #se imaginan que esta funcion la hubiera puesto antes y que generara
            #me diera listas de conflictos en lugar del numero de conflictos?
            #me hubiera ahorrado lineas de codigo y dolores de cabez
            acc = 0
            for xj in gr.vecinos[xi]:
                if not gr.restricción((xi, vi), (xj, ap[xj])):
                    acc += 1
            #print(acc)
            return acc
        a[i] = min(gr.dominio[i],key=lambda x:contar_conflictos(gr, a, i, x))
        #print(a[i])
        conflictos_de_i = []
        for x in gr.vecinos[i]:#esto tampoco es elegante porque es practicamente lo mismo de arriba
            if not gr.restricción((i, a[i]), (x,a[x])):
                conflictos_de_i.append(x)
        if conflictos_de_i:
            b.insert(0, i)
            for j in conflictos_de_i:
                if j not in b:
                    b.append(j)
    return a
    raise NotImplementedError("Minimos conflictos  a implementar")
