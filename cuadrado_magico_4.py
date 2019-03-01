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

__author__ = 'Brayan Durazo'


class CuadroMagico(csp.GrafoRestriccion):
    
    def __init__(self):
        super().__init__()
        self.dominio = list()
    
    
    def restriccion(self, xi_vi, xj_vj):
        return None

    def muestra_asignacion(asignacion):
        return None


    def prueba_cuadromagico(n, metodo, tipo=1, traza=False):
        return None
