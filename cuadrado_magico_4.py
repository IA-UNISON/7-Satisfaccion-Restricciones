#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
cuadrado_magico_4.py
--------------------
En este módulo hay que desarrollar un modelo para la generación de un cuadrado
mágico de 4 x 4. Un cuadrado mágico es una matriz cuadrada cuyas entradas son
todas diferentes, de forma que la suma de los elementos de cada columna, de
cada renglon y de las dos diagonales principales den el mismo número.
Una vez establecido el problema, hay que resolverlo con cualquiera de los
métodos de solución de problemas de satisfacción de restricciones
desarrollados, y comprobar que el resultado es efectivamente un cuadrado mágico
de 4 x 4.
"""

__author__ = 'Lizeth Soto Félix'

import csp

class CuadradoMagico(csp.GrafoRestriccion):

    def __init__(self):
        """
        Inicializa el sudoku

        """
        super().__init__()

        for var in range(4):
            self.dominio[var] = set(range(4))
            self.vecinos[var] = {i for i in range(4) if i != var}

    def restriccion(self, xi_vi, xj_vj):
        """
        El mero chuqui. Por favor comenta tu código correctamente

        """
        xi, vi = xi_vi
        xj, vj = xj_vj
        
        return vi!=vj

def imprime_cuadrado(asignacion):
    """
    Imprime un sudoku en pantalla en forma más o menos graciosa. Esta
    función solo sirve para la tarea y para la revisión de la
    tarea. No modificarla por ningun motivo.

    """
    """
    s = [asignacion[i] for i in range(4)]
    rayita = '\n-------------+----------------+---------------\n'
    c = ''
    for i in range(9):
        c += ' '.join(str(s[9 * i + j]) +
                      ("  |  " if j % 3 == 2 and j < 7 else "   ")
                      for j in range(9))
        c += rayita if i % 3 == 2 and i < 7 else '\n'
    print(c)
    """

if __name__ == "__main__":
