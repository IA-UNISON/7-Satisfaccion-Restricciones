#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
nreinasCSP.py



"""

__author__ = 'Adrian Emilio Vazquez Icedo'


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

#Cambie unas cosas por que me probocaba errores
def prueba_reinas(n, metodo, tipo=0, traza=False):
    print("\n" + '-' * 20 + '\n Para {} reinas\n'.format(n) + '_' * 20)
    g_r = Nreinas(n)
    if tipo>0:
        asignacion = metodo(g_r, ap={}, consist=tipo, traza=traza)
    else:
        asignacion = metodo(g_r)
        
    if asignacion is not None:   
        if n < 20:
            Nreinas.muestra_asignacion(asignacion)
        else:
            print([asignacion[i] for i in range(n)])
        print("Y se realizaron {} backtrackings".format(g_r.backtracking))
    else: 
        print('No se pudo :(')


if __name__ == "__main__":

    #Utilizando 1 consistencia
    #prueba_reinas(4, csp.asignacion_grafo_restriccion, traza=True, tipo=1)
    prueba_reinas(8, csp.asignacion_grafo_restriccion, traza=True, tipo=1)
    #prueba_reinas(16, csp.asignacion_grafo_restriccion, traza=True, tipo=1)
    #prueba_reinas(50, csp.asignacion_grafo_restriccion, tipo=1)
    #prueba_reinas(101, csp.asignacion_grafo_restriccion, tipo=1)

    # Utilizando consistencia
    # ==========================================================================
    # Probar y comentar los resultados del métdo de arco consistencia
    # ==========================================================================
    # 4: 1-consistencia=2 backtrackings 2-consistencia=0 backtrackings
    # 8: 1-consistencia=21 backtrackings 2-consistencia=1 backtrackings
    # 16: 1-consistencia=223 backtrackings 2-consistencia=47 backtrackings
    # 50: 1-consistencia=611 backtrackings 2-consistencia=92 backtrackings
    # 101: 1-consistencia=15 backtrackings 2-consistencia=4 backtrackings
    #
    # El 2-consistencia da mejores resultados que el 1-consistencia debido a que
    # realiza menos backtrackings lo que implica que realiza una menor busqueda
    # por lo cual es un metodo mas efectivo.  
    #
    #===========================================================================
    #prueba_reinas(4, csp.asignacion_grafo_restriccion, traza=True, tipo=2)
    prueba_reinas(8, csp.asignacion_grafo_restriccion, traza=True, tipo=2)
    #prueba_reinas(16, csp.asignacion_grafo_restriccion, traza=True, tipo=2)
    #prueba_reinas(50, csp.asignacion_grafo_restriccion, tipo=2)
    #prueba_reinas(101, csp.asignacion_grafo_restriccion, tipo=2)

    # Utilizando minimos conflictos
    # ==========================================================================
    # Probar y comentar los resultados del métdo de mínios conflictos
    # 
    # Para 4, 8, 16 y 51 se logra alcanzar la solucion y con un tiempo aceptable 
    # pero para 101 el tiempo ya se vuelve algo a considerar y para 1000 considero 
    # que es mucho tiempo. Para intentar conseguir siempre una solucion se debera 
    # aumentar el numero de iteraciones pero seria un gran impacto al tiempo que
    # tardara este algoritmo, por lo que es mejor utilizar los algoritmos con 
    # grafos.
    # ==========================================================================
    #prueba_reinas(4, csp.min_conflictos)
    prueba_reinas(8, csp.min_conflictos)
    #prueba_reinas(16, csp.min_conflictos)
    #prueba_reinas(51, csp.min_conflictos)
    #prueba_reinas(101, csp.min_conflictos)
    #prueba_reinas(1000, csp.min_conflictos)
