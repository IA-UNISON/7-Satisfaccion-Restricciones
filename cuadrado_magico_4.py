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

import csp
#import numpy as np

__author__ = 'Irving Borboa'

class CuadradoMagico(csp.GrafoRestriccion):

    def __init__(self, n=4):
        super().__init__()
        for var in range(n):
            self.dominio[var] = set(range(16))
            self.vecinos[var] = {i for i in range(n) if i != var}
            
    def restricción(self,  xi_vi, xj_vj):
        xi, vi = xi_vi
        xj, vj = xj_vj
        #if vi != 
        


