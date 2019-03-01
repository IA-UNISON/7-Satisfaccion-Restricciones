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

__author__ = 'Ricardo E. Alvarado Mata'

import csp


class CuadradoMagico4x4(csp.GrafoRestriccion):

    def __init__(self):
        super().__init__()

        self.dominio = {i: range(1,17) for i in range(16)}

        self.vecinos = {}
        for var in range(16):
            self.vecinos[var] = set()
            for i in range(4):
                ren = i+(var//9)*9
                col = i*9+(var%9)

                if ren != var:
                    self.vecinos[var].add(ren)
                if col != var:
                    self.vecinos[var].add(col)
                if var % 5 == 0 and i != var:
                    self.vecinos[var].add(i*5)
                if var % 3 == 0 and i != var:
                    self.vecinos[var].add(i*3)
            
    def restriccion(self, xi_vi, xj_vj):
        x_i, v_i = xi_vi
        x_j, v_j = xj_vj

        return v_i != v_j


# Inserta tu código aquí
