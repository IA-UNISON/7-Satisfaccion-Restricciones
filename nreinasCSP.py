#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
nreinasCSP.py



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
    print("\n" + '-' * 20 + '\n Para {} reinas\n'.format(n) + '_' * 20)
    g_r = Nreinas(n)
    #asignacion = metodo(g_r, ap={}, consist=tipo, traza=traza)
    asignacion = metodo(g_r) #minimos conflictos
    if n < 20:
        Nreinas.muestra_asignacion(asignacion)
    else:
        print([asignacion[i] for i in range(n)])
    print("Y se realizaron {} backtrackings".format(g_r.backtracking))


if __name__ == "__main__":

    # Utilizando 1 consistencia
    #prueba_reinas(4, csp.asignacion_grafo_restriccion, traza=True, tipo=1)
    #prueba_reinas(8, csp.asignacion_grafo_restriccion, traza=True, tipo=1)
    #prueba_reinas(16, csp.asignacion_grafo_restriccion, traza=True, tipo=1)
    #prueba_reinas(50, csp.asignacion_grafo_restriccion, tipo=1)
    #prueba_reinas(101, csp.asignacion_grafo_restriccion, tipo=1)

    # Utilizando consistencia
    # ==========================================================================
    # Probar y comentar los resultados del métdo de arco consistencia
    # ==========================================================================
    #prueba_reinas(4, csp.asignacion_grafo_restriccion, traza=True, tipo=2)
    """ 
     Para 4 reinas
____________________
0 = 1
	1 = 3
		2 = 0
			3 = 2
+-+-+-+-+
| |X| | |
+-+-+-+-+
| | | |X|
+-+-+-+-+
|X| | | |
+-+-+-+-+
| | |X| |
+-+-+-+-+
Y se realizaron 0 backtrackings
    
    """
    #prueba_reinas(8, csp.asignacion_grafo_restriccion, traza=True, tipo=2)
    """
     Para 8 reinas
____________________
0 = 0
	1 = 3
0 = 1
0 = 3
	1 = 1
		2 = 4
			3 = 7
				4 = 5
					5 = 0
						6 = 2
							7 = 6
+-+-+-+-+-+-+-+-+
| | | |X| | | | |
+-+-+-+-+-+-+-+-+
| |X| | | | | | |
+-+-+-+-+-+-+-+-+
| | | | |X| | | |
+-+-+-+-+-+-+-+-+
| | | | | | | |X|
+-+-+-+-+-+-+-+-+
| | | | | |X| | |
+-+-+-+-+-+-+-+-+
|X| | | | | | | |
+-+-+-+-+-+-+-+-+
| | |X| | | | | |
+-+-+-+-+-+-+-+-+
| | | | | | |X| |
+-+-+-+-+-+-+-+-+
Y se realizaron 3 backtrackings
    """
    #prueba_reinas(16, csp.asignacion_grafo_restriccion, traza=True, tipo=2)
    """
     Para 16 reinas
    ____________________
    0 = 0
        1 = 3
            2 = 6
                7 = 15
                    3 = 9
                        6 = 1
                            5 = 10
                                8 = 2
                                    4 = 7
                                        9 = 5
                                    4 = 14
                                        11 = 8
                                    4 = 13
                                        10 = 11
                                    4 = 5
                                8 = 5
                                    11 = 14
                                        4 = 13
                                            9 = 2
                                    11 = 7
                                        4 = 13
                                    11 = 12
                                8 = 11
                                    10 = 4
                                    10 = 7
                                    10 = 8
                                        12 = 4
                            5 = 14
                                4 = 11
                                    8 = 13
                                        10 = 4
                                    8 = 2
                                        10 = 13
                                    8 = 5
                                4 = 5
                                    8 = 13
                                    8 = 2
                                4 = 7
                                    9 = 5
                                        8 = 2
                                        8 = 13
                                            10 = 8
                                    9 = 8
                                4 = 2
                                    8 = 13
                                    8 = 7
                            5 = 8
                                8 = 13
                                    10 = 4
                                        11 = 7
                                    10 = 7
                                        9 = 2
                                        9 = 10
                                        9 = 5
                                8 = 2
                                    10 = 7
                                        4 = 11
                                            9 = 14
                                                11 = 10
                                                    12 = 13
                                                        13 = 5
                                                            14 = 12
                                                                15 = 4
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |X| | | | | | | | | | | | | | | |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    | | | |X| | | | | | | | | | | | |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    | | | | | | |X| | | | | | | | | |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    | | | | | | | | | |X| | | | | | |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    | | | | | | | | | | | |X| | | | |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    | | | | | | | | |X| | | | | | | |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    | |X| | | | | | | | | | | | | | |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    | | | | | | | | | | | | | | | |X|
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    | | |X| | | | | | | | | | | | | |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    | | | | | | | | | | | | | | |X| |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    | | | | | | | |X| | | | | | | | |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    | | | | | | | | | | |X| | | | | |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    | | | | | | | | | | | | | |X| | |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    | | | | | |X| | | | | | | | | | |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    | | | | | | | | | | | | |X| | | |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    | | | | |X| | | | | | | | | | | |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    Y se realizaron 47 backtrackings
    """
    #prueba_reinas(50, csp.asignacion_grafo_restriccion, tipo=2)
    """
     Para 50 reinas
    ____________________
    [0, 3, 6, 17, 24, 45, 34, 49, 46, 25, 21, 19, 48, 9, 47, 20, 26, 15, 40, 43, 1, 27, 2, 13, 42, 44, 29, 10, 5, 22, 14, 7, 11, 8, 12, 4, 23, 31, 39, 36, 32, 30, 41, 38, 35, 18, 28, 33, 16, 37]
    Y se realizaron 92 backtrackings
    """
    #prueba_reinas(101, csp.asignacion_grafo_restriccion, tipo=2)
    """
     Para 101 reinas
____________________
[0, 3, 100, 7, 47, 55, 98, 62, 99, 97, 45, 1, 96, 60, 2, 57, 8, 50, 58, 95, 92, 89, 59, 54, 94, 34, 4, 93, 51, 28, 79, 44, 6, 91, 29, 43, 90, 76, 10, 5, 26, 42, 12, 87, 24, 13, 39, 9, 86, 83, 14, 49, 88, 85, 30, 66, 80, 41, 70, 11, 56, 21, 84, 17, 78, 23, 82, 77, 18, 25, 52, 22, 20, 32, 27, 81, 19, 64, 75, 73, 69, 15, 37, 40, 31, 48, 61, 16, 67, 72, 35, 68, 53, 74, 63, 36, 33, 46, 65, 38, 71]
Y se realizaron 4 backtrackings
    """
    # Utilizando minimos conflictos
    # ==========================================================================
    # Probar y comentar los resultados del métdo de mínios conflictos
    # ==========================================================================
    prueba_reinas(4, csp.min_conflictos)
    # prueba_reinas(8, csp.min_conflictos)
    # prueba_reinas(16, csp.min_conflictos)
    # prueba_reinas(51, csp.min_conflictos)
    # prueba_reinas(101, csp.min_conflictos)
    # prueba_reinas(1000, csp.min_conflictos)
