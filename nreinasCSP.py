#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
nreinasCSP.py



"""

__author__ = 'luis fernando'


import csp

import time #para comparar tiempos

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


def prueba_reinas(n, metodo, tipo=1, imprimir=False):
    print("\n" + '-' * 20 + '\n Para {} reinas\n'.format(n) + '_' * 20)
    g_r = Nreinas(n)
    asignacion = metodo(g_r, ap={}, consist=tipo, traza=imprimir)
    if imprimir:
        Nreinas.muestra_asignacion(asignacion)
    else:
        print([asignacion[i] for i in range(n)])
    print("Y se realizaron {} backtrackings".format(g_r.backtracking))


if __name__ == "__main__":

    reinas = [4, 6, 16, 50, 60, 100, 101]
    def prueba_cons(tipo):
        for reina in reinas:
            t_inicial = time.time()
            prueba_reinas(reina, csp.asignacion_grafo_restriccion, imprimir=False, tipo=tipo)
            t_final = time.time()
            print("Tiempo: {}\n".format(t_final - t_inicial))

    # Utilizando 1 consistencia
    #print("Utilizando 1 consistencia\n")
    #prueba_cons(1)

    # Utilizando consistencia
    #print("\nUtilizando AC-3 (2 consistencia)\n")
    #prueba_cons(2)
    # ==========================================================================
    # Probar y comentar los resultados del métdo de arco consistencia
    # ==========================================================================

    # Utilizando minimos conflictos
    # ==========================================================================
    # Probar y comentar los resultados del métdo de mínios conflictos
    # ==========================================================================

    def prueba_min(reinas, metodo, imprimir = True):
        for reina in reinas:
            g_r = Nreinas(reina)

            t_inicial = time.time()
            asignacion = metodo(g_r, 1000, 100)
            t_final = time.time()

            if asignacion is not None:
                if imprimir:
                    Nreinas.muestra_asignacion(asignacion)
                else:
                    print([asignacion[i] for i in range(n)])
                print("Y se realizaron {} backtrackings".format(g_r.backtracking))
            else:
                print("El algoritmo no encontro asignacion")

            print("Tiempo: {}\n".format(t_final - t_inicial))


    reinas = [4, 8, 16, 51, 101, 1000]
    prueba_min(reinas, csp.min_conflictos)
    # prueba_reinas(8, csp.min_conflictos)
    # prueba_reinas(16, csp.min_conflictos)
    # prueba_reinas(51, csp.min_conflictos)
    # prueba_reinas(101, csp.min_conflictos)
    # prueba_reinas(1000, csp.min_conflictos)

"""
Diferencias al utilizar 1 consistencia y al utilizar arco consistencia.

Comparando los numeros de backtracking:

N   Tipo 1  Tipo 2
4   2       0
8   21      1
16  223     47
50  611     92
60  0       0
100 58      4
101 15      4

Comparando el tiempo de ejecucion:

N   Tipo 1  Tipo 2
4   5e-4    2e-4
8   3e-3    1e-3
16  0.02    0.05
50  0.6     1.7
60  1.27    2.83
100 9.35    21.4
101 9.2     22.4

Tienen un comportamiento interesante que inicialmente no me esperaba. La 1-consistencia solo
aumenta en numero de backtrackings hasta que llega a mas de 600 para 50 reinas a comparacion de
las menos de 100 para el AC-3 y el tiempo de ambos es practicamente el mismo hasta ese punto.
Despues en 60 reinas ambos algoritmos necesitan 0 bacltracings y se va notando que AC-3 empieza a
tardar mas que la 1-consistencia. En el caso de 100 reinas el primer caso ocupa 58 backtrackings
mientras que en AC-3 solo ocupa 4 pero el tiempo que tarda es mas del doble que la 1-consistencia.
Finalmente lo que queda por notar es que la unica diferencia entre 100 y 101 reinas es que
1-consistencia disminuye su numero de backtracking necesario.

Ya que en los dos tipos de consistencia se encuentran las soluciones al problema, el de menor
tiempo para todos los casos fue la 1 consistencia y deberia ser la preferida para estas reinas.


Minimos coflictos:
Hastas ahora minimos conflictos ha sido el peor algoritmo de los de esta tarea para solucionar el
problema de las reinas. Solo el caso de 4 reinas daba soluciones al problema y tardaba mas que ac-3,
para los demas casos no pude encotrar soluciones y me gustaria pensar que no es culpa de la
implementacion de mi algoritmo (no he podido encontrar el error si es que existe). Lo que si es que
quiza si no inicializara al azar la asignacion es posible que mejorara el algoritmo.
"""

