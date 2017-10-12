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
        self.a = 0
        for var in range(n):
            self.dominio[var] = set(range(n))
            self.vecinos[var] = set(i for i in range(n) if i != var)

    def restriccion(self, xi_vi, xj_vj):
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
        # self.a += 1
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


def prueba_reinas(n, metodo):
    print("\n" + '-' * 20 + '\n Para {} reinas\n'.format(n) + '_' * 20)
    g_r = Nreinas(n)
    asignación = metodo(g_r)
    if n < 20:
        Nreinas.muestra_asignación(asignación)
    else:
        print([asignación[i] for i in range(n)])
    print("Y se realizaron {} backtrackings".format(g_r.backtracking))


if __name__ == "__main__":
    # Utilizando 1 consistencia
    prueba_reinas(4, lambda gr: csp.asignacion_grafo_restriccion(gr, consist=1, traza=True))
    prueba_reinas(8, lambda gr: csp.asignacion_grafo_restriccion(gr, consist=1, traza=True))
    prueba_reinas(16, lambda gr: csp.asignacion_grafo_restriccion(gr, consist=1, traza=True))
    prueba_reinas(50, lambda gr: csp.asignacion_grafo_restriccion(gr, consist=1, traza=False))
    prueba_reinas(101, lambda gr: csp.asignacion_grafo_restriccion(gr, consist=1, traza=False))
    # Utilizando consistencia
    # =============================================================================
    # 25 puntos: Probar y comentar los resultados del métdo de arco consistencia
    # =============================================================================
    prueba_reinas(4, lambda gr: csp.asignacion_grafo_restriccion(gr, consist=2, traza=True))
    prueba_reinas(8, lambda gr: csp.asignacion_grafo_restriccion(gr, consist=2, traza=True))
    prueba_reinas(16, lambda gr: csp.asignacion_grafo_restriccion(gr, consist=2, traza=True))
    prueba_reinas(50, lambda gr: csp.asignacion_grafo_restriccion(gr, consist=2, traza=False))
    prueba_reinas(101, lambda gr: csp.asignacion_grafo_restriccion(gr, consist=2, traza=False))

    '''
    El algoritmo de consistencia 2 efectivamente hace que se tengan que revisar
    menos nodos solo realizando 4 backtracks para el problema de tamaño 101 (vs
    los 25 de la consistencia 1). Sin embargo, el AC-3 tiene una complejidad
    mas alta que la consistencia 1 (O(nd^3) donde d es el dominio mas grande
    segun wikipedia), asi que al menos en este problema la consistencia 1 igual
    sale ganando.
    '''

    # Utilizando minimos conflictos
    # =============================================================================
    # 25 puntos: Probar y comentar los resultados del métdo de mínios conflictos
    # =============================================================================
    prueba_reinas(4, csp.min_conflictos)
    prueba_reinas(8, csp.min_conflictos)
    prueba_reinas(16, csp.min_conflictos)
    prueba_reinas(51, csp.min_conflictos)
    prueba_reinas(101, csp.min_conflictos)

    '''
    Los minimos conflictos en general fueron mas rapidos para el problema de
    las n reinas (lo opuesto se encontro para el sudoku), y se encontro que 10
    repeticiones de minimos conflictos con 1000 repeticiones fue el parametro
    adecuado para resolver hasta el problema de 101 reinas en un buen tiempo.
    '''
