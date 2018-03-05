#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
nreinasCSP.py



"""

__author__ = 'juliowaissman'


import csp
import time


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
            self.dominio[var] = set(range(n))
            self.vecinos[var] = {i for i in range(n) if i != var}

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
        xi, vi = xi_vi
        xj, vj = xj_vj
        return vi != vj and abs(vi - vj) != abs(xi - xj)

    @staticmethod
    def muestra_asignacion(asignacion):
        """
        Muestra la asignación del problema de las N reinas en forma de
        tablerito.

        """
        n = len(asignacion)
        interlinea = "+" + "-+" * n
        print(interlinea)
        for i in range(n):
            linea = '|'
            for j in range(n):
                linea += 'X|' if j == asignacion[i] else ' |'
            print(linea)
            print(interlinea)


def prueba_reinas(búqueda, n, metodo, tipo=1, traza=False):
    # Reporte resultados 1 y 2 consistencias
    
    # Efectivamente se demora más con la 2 consistencia pero genera una cantidad menor de backtrackings.
    # Para los diferentes casos los resultados en grafos de restricción son:
    # 4 Reinas. 1-consistencia: 2 backtrackings, 0 segundos. 2-consistencia: 0 backtrackings, 0 segundos
    # 8 Reinas. 1-consistencia: 21 backtrackings, 0.01 segundos. 2-consistencia: 1 backtrackings, 0.01 segundos
    # 16 Reinas. 1-consistencia: 223 backtrackings, 0.06 segundos. 2-consistencia: 47 backtrackings, 0.09 segundos
    # 50 Reinas. 1-consistencia: 611 backtrackings, 1.30 segundos. 2-consistencia: 92 backtrackings, 2.82 segundos
    # 100 Reinas. 1-consistencia: 15 backtrackings, 20.26 segundos. 2-consistencia: 4 backtrackings, 44.46 segundos
    # 
    # Para mínimos conflictos:
    # 4 Rainas. 0.1 segundos
    # 8 Reinas. 0.03 segundos
    # 16 Reinas. 0.18 segundos
    # 51 Reinas. 17.87 segundos
    # 101 Reinas 112.93 segundos pero sin resultados concluyentes.
    # El tiempo incrementa demasiado para los minimos conflictos y para los casos de 51 o más reinas
    # requeririan de un numero mayor de iteraciones a mi parecer pero esto tomaría mucho mas tiempo del
    # actual.
    g_r = Nreinas(n)

    tiempo_inicial = time.time()
    tiempo_final = 0
    if búqueda == 'min_con':
        print("\n" + '-' * 20 + '\n Para {} reinas con mínimos conflictos\n'.format(n) + '_' * 20)
        asignacion = metodo(g_r)
        tiempo_final = time.time()
    else:
        print("\n" + '-' * 20 + '\n Para {} reinas con grafo de restricción\n'.format(n) + '_' * 20)
        asignacion = metodo(g_r, ap={}, consist=tipo, traza=traza)
        tiempo_final = time.time()

    print("{:*^25.2f} segunos".format(tiempo_final - tiempo_inicial))

    if n < 20:
        if asignacion is not None:
           Nreinas.muestra_asignacion(asignacion)
        else:
            print('No hay resultado concluyente')
    else:
        if asignacion is not None:
            print([asignacion[i] for i in range(n)])
        else:
            print('No hay resultado concluyente')
    
    print("Y se realizaron {} backtrackings".format(g_r.backtracking))


if __name__ == "__main__":

    # Utilizando 1 consistencia
    # prueba_reinas('gr', 4, csp.asignacion_grafo_restriccion, traza=True, tipo=1)
    # prueba_reinas('gr', 8, csp.asignacion_grafo_restriccion, traza=True, tipo=1)
    # prueba_reinas('gr', 16, csp.asignacion_grafo_restriccion, traza=True, tipo=1)
    prueba_reinas('gr', 50, csp.asignacion_grafo_restriccion, tipo=1)
    # prueba_reinas('gr', 101, csp.asignacion_grafo_restriccion, tipo=1)

    # Utilizando consistencia
    # ==========================================================================
    # Probar y comentar los resultados del métdo de arco consistencia
    # ==========================================================================
    # prueba_reinas('gr', 4, csp.asignacion_grafo_restriccion, traza=True, tipo=2)
    # prueba_reinas('gr', 8, csp.asignacion_grafo_restriccion, traza=True, tipo=2)
    # prueba_reinas('gr', 16, csp.asignacion_grafo_restriccion, traza=True, tipo=2)
    prueba_reinas('gr', 50, csp.asignacion_grafo_restriccion, tipo=2)
    # prueba_reinas('gr', 101, csp.asignacion_grafo_restriccion, tipo=2)

    # Utilizando minimos conflictos
    # ==========================================================================
    # Probar y comentar los resultados del métdo de mínios conflictos
    # ==========================================================================
    # prueba_reinas('min_con', 4, csp.min_conflictos)
    # prueba_reinas('min_con', 8, csp.min_conflictos)
    # prueba_reinas('min_con', 16, csp.min_conflictos)
    # prueba_reinas('min_con', 51, csp.min_conflictos)
    prueba_reinas('min_con', 101, csp.min_conflictos)
    # prueba_reinas('min_con', 1000, csp.min_conflictos)
