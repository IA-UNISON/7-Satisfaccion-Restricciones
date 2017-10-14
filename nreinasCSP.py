#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
nreinasCSP.py
------------


"""

__author__ = 'juliowaissman'


import csp


class Nreinas(csp.GrafoRestriccion):
    """
    El problema de las n-reinas.

    Esta clase permite instanciar un problema de n reinas, sea n un
    numero entero mayor a 3 (para 3 y para 2 no existe solución al
    problema).

    """

    def __init__(self, n=4):
        """
        Inicializa las n--reinas para n reinas, por lo que:

            dominio[i] = [0, 1, 2, ..., n-1]
            vecinos[i] = [0, 1, 2, ..., n-1] menos la misma i.

            ¡Recuerda que dominio[i] y vecinos[i] son diccionarios y no listas!

        """
        super().__init__()
        for var in range(n):
            self.dominio[var] = list(range(n))
            self.vecinos[var] = [i for i in range(n) if i != var]

    def restricción(self, xi_vi, xj_vj):
        """
        Verifica si se cumple la restriccion binaria entre las variables xi
        y xj cuando a estas se le asignan los valores vi y vj respectivamente.

        La restriccion binaria entre dos reinas, las cuales se comen
        si estan en la misma posición o en una diagonal. En esos casos
        hay que devolver False (esto es, no se cumplió con la
        restricción).

        @param xi: El nombre de una variable
        @param vi: El valor que toma la variable xi (dentro de self.dominio[xi]
        @param xj: El nombre de una variable
        @param vj: El valor que toma la variable xi (dentro de self.dominio[xj]

        @return: True si se cumple la restricción

        """
        xi, vi = xi_vi
        xj, vj = xj_vj
        return vi != vj and abs(vi - vj) != abs(xi - xj)

    @staticmethod
    def muestra_asignación(asignación):
        """
        Muestra la asignación del problema de las N reinas en forma de
        tablerito.

        """
        n = len(asignación)
        interlinea = "+" + "-+" * n
        print(interlinea)
        for i in range(n):
            linea = '|'
            for j in range(n):
                linea += 'X|' if j == asignación[i] else ' |'
            print(linea)
            print(interlinea)


def prueba_reinas(n, metodo, tipo=1, traza=False, dibujar = True):
    print("\n" + '-' * 20 + '\n Para {} reinas\n'.format(n) + '_' * 20)
    g_r = Nreinas(n)
    asignación = metodo(g_r, ap={}, consist=tipo, traza=traza)
    if dibujar:
        Nreinas.muestra_asignación(asignación)
    else:
        print([asignación[i] for i in range(n)])

    print("Y se realizaron {} backtrackings".format(g_r.backtracking))
def prueba_reinas2(n, metodo, dibujar=True):
    print("\n" + '-' * 20 + '\n Para {} reinas\n'.format(n) + '_' * 20)
    g_r = Nreinas(n)
    asignación = metodo(g_r)
    if dibujar:
        Nreinas.muestra_asignación(asignación)
    else:
        print([asignación[i] for i in range(n)])

if __name__ == "__main__":

    # Utilizando 1 consistencia
    import time

    '''
    start = time.time()
    prueba_reinas(4, csp.asignacion_grafo_restriccion, traza=True, tipo=1)
    end = time.time()
    print(end - start, " segundos 1 cons 4 reinas")
    prueba_reinas(8, csp.asignacion_grafo_restriccion, traza=True, tipo=1)
    start = time.time()
    print(start - end, " segundos 1 cons 8 reinas")
    prueba_reinas(16, csp.asignacion_grafo_restriccion, tipo=1)
    end = time.time()
    print(end-start , " segudno 1 cons 16 reinas")
    prueba_reinas(50, csp.asignacion_grafo_restriccion, tipo=1)
    start = time.time()
    print(start-end, " segundos 1 cons 50 reinas")
    prueba_reinas(101, csp.asignacion_grafo_restriccion, tipo=1)
    4  0.00111s y 2  backtracking
    8  0.00300s y 19 backtracking
    16 0.02501s y 55 backtracking
    50 1.17935s y 16 backtracking
    101 NO RESULTADOS TIEMPO ACEPTABLE
    '''
    # Utilizando consistencia
    #=============================================================================
    # 25 puntos: Probar y comentar los resultados del métdo de arco consistencia
    #=============================================================================
    #prueba_reinas(4, csp.asignacion_grafo_restriccion, traza=True, tipo=2)
    #
    prueba_reinas(8, csp.asignacion_grafo_restriccion, traza=True, tipo=2)
    # prueba_reinas(16, csp.asignacion_grafo_restriccion, tipo=2)
    # prueba_reinas(50, csp.asignacion_grafo_restriccion, tipo=2)
    # prueba_reinas(101, csp.asignacion_grafo_restriccion, tipo=2)
    '''
    start = time.time()
    prueba_reinas(4, csp.asignacion_grafo_restriccion, traza=True, tipo=2)
    end = time.time()
    print(end - start, " segundos 2 cons 4 reinas")
    prueba_reinas(8, csp.asignacion_grafo_restriccion, traza=True, tipo=2)
    start = time.time()
    print(start - end, " segundos 2 cons 8 reinas")
    prueba_reinas(16, csp.asignacion_grafo_restriccion, tipo=2)
    end = time.time()
    print(end-start , " segudno 2 cons 16 reinas")
    prueba_reinas(50, csp.asignacion_grafo_restriccion, tipo=2)
    start = time.time()
    print(start-end, " segundos 2 cons 50 reinas")
    prueba_reinas(101, csp.asignacion_grafo_restriccion, tipo=2)
    4  0.00132s y 0  backtracking
    8  0.01000s y 8  backtracking
    16 0.05503s y 6  backtracking
    50  NO RESULTADOS TIEMPO ACEPTABLE
    101 NO RESULTADOS TIEMPO ACEPTABLE

    Generamos menos backtracking pero al costo de que el tiempo de computo
    es mucho mas lento que con consistencia sencilla
    '''
    # Utilizando minimos conflictos
    #=============================================================================
    # 25 puntos: Probar y comentar los resultados del métdo de mínios conflictos
    #=============================================================================
    '''
    start = time.time()
    prueba_reinas2(4, csp.min_conflictos)
    end = time.time()
    print(end-start, "s 4 reinas")
    prueba_reinas2(8, csp.minimos_conflictos)
    start = time.time()
    print(start-end,"s 8 reinas")
    prueba_reinas2(16, csp.min_conflictos)
    end = time.time()
    print(end-start, "s 16 reinas")
    prueba_reinas2(51, csp.min_conflictos)
    start = time.time()
    print(start-end,"s 8 reinas")
    prueba_reinas2(101, csp.min_conflictos)
    end = time.time()
    print(end-start, "s 101 reinas")
    prueba_reinas2(1000, csp.min_conflictos)
    start = time.time()
    print(start-end,"s 1000 reinas")
    4       0.02001s
    8       0.00800s
    16      0.02953s
    51      0.26118s
    101     1.02535s
    1000    NO RESULTADOS TIEMPO ACEPTABLE

    Este metodo para este problema es mucho mas veloz
    '''
