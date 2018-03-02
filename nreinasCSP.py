#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
nreinasCSP.py



"""

__author__ = 'juliowaissman'

from time import time
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


def prueba_reinas(n, metodo, tipo=1, traza=False):
    """
    Prueba una gráfica de restricciones o mínimos conflictos para resolver
    n reinas.

    @param metodo: Cadena que indica qué método probar. Puede ser "grafo" para
    gráficas de restricción o "minimos" para mínimos conflictos.
    @param tipo: Tipo de consistencia. Solo aplica para gráficas de restricción.
    @param traza: Indica si se imprime la traza de la asignación parcial. Solo aplica
    para gráficas de restricción.
    """
    print("\n" + '-' * 20 + '\n Para {} reinas\n'.format(n) + '_' * 20)
    g_r = Nreinas(n)

    if metodo == "grafo":
        t_inicial = time()
        asignacion = csp.asignacion_grafo_restriccion(g_r, ap={}, consist=tipo, traza=traza)
        t_final = time()
    elif metodo == "minimos":
        t_inicial = time()
        asignacion = csp.min_conflictos(g_r)
        t_final = time()
    else:
        raise ValueError("El método especificado no existe.")

    if asignacion is not None:
        if n < 20:
            Nreinas.muestra_asignacion(asignacion)
        else:
            print([asignacion[i] for i in range(n)])
        print("Se realizaron {} backtrackings.".format(g_r.backtracking))
        print("Y tardó {} segundos.".format(t_final - t_inicial))
    else:
        print("El algoritmo falló.")
        print("Y tardó {} segundos en fallar.".format(t_final - t_inicial))

if __name__ == "__main__":

    # Utilizando 1 consistencia
    prueba_reinas(4, "grafo", traza=True, tipo=1)
    prueba_reinas(8, "grafo", traza=True, tipo=1)
    prueba_reinas(16, "grafo", traza=True, tipo=1)
    prueba_reinas(50, "grafo", tipo=1)
    prueba_reinas(101, "grafo", tipo=1)

    # Utilizando consistencia
    # ==========================================================================
    # Probar y comentar los resultados del método de arco consistencia
    # ==========================================================================
    prueba_reinas(4, "grafo", traza=True, tipo=2)
    prueba_reinas(8, "grafo", traza=True, tipo=2)
    prueba_reinas(16, "grafo", traza=True, tipo=2)
    prueba_reinas(50, "grafo", tipo=2)
    prueba_reinas(101, "grafo", tipo=2)

    ############################################################################
    ## Dos cosas se ven claramente al probar los dos tipos de consistencia:
    ## 1. AC-3 hace muchos menos backtracking, una fracción de los que hace la
    ##    1-consistencia.
    ## 2. AC-3 si hace que la asignación de valores tarde al menos el doble del
    ##    tiempo que tarda con la 1-consistencia. Eso al menos con la implementación
    ##    predeterminada de las consistencias.
    ############################################################################

    # Utilizando minimos conflictos
    # ==========================================================================
    # Probar y comentar los resultados del método de mínimos conflictos
    # ==========================================================================
    prueba_reinas(4, "minimos")
    prueba_reinas(8, "minimos")
    prueba_reinas(16, "minimos")
    prueba_reinas(51, "minimos")
    prueba_reinas(101, "minimos")
    prueba_reinas(1000, "minimos")

    ############################################################################
    ## Mínimos conflictos no es muy bueno para satisfacer las restricciones del
    ## problema. Como la reasignación de variables es aleatoria, no hay garantía
    ## de que al final logre corregir todos los conflictos con los que la asignación
    ## aleatoria comienza.
    ## Hasta en casos pequeños como el de 4 y 8 reinas tarda considerablemente más
    ## que revisar consistencias.
    ############################################################################
