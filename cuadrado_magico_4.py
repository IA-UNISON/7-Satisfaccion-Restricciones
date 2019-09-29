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

__author__ = 'Miguel Romero valdés'


# Inserta tu código aquí

import csp

class CuadroMagico(csp.GrafoRestriccion):

"""Magic square constant: n(n^2+1)/2"""

    def __init__(self):

        super().__init__()
        for var in range(4*4):
            self.dominio[var] = set(range(1, 4**4 + 1))
            self.vecinos[var] = {i for i in range(4*4) if i != var}
            #MSC: Magic Square Constant
            self.MSC = 34

    #Fin constructor


    def restriccion(self, xi_vi, xj_vj):

        xi, vi = xi_vi
        xj, vj = xj_vj
        

        return vi != vj

    #Fin funcion restriccion



if __name__ == "__main__":


    

        
                   
