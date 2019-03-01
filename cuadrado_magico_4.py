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
import itertools
class CuadradoMagico(csp.GrafoRestriccion):

    def __init__(self):
        """
        Inicializa el chuki magico

        """
        super().__init__()

        for var in range(16):
            self.dominio[var] = set(range(1,20))
            self.vecinos[var] = {i for i in range(26) if i != var}
        for var in range(10):
            self.dominio[var+16] = set(itertools.combinations(range(1,20), 4))
            self.vecinos[var+16] = {i for i in range(26) if i != var+16}
    def restriccion(self, xi_vi, xj_vj):
        """
        No hay nada que comentar, me rindo :(

        """
        
        xi, vi = xi_vi
        xj, vj = xj_vj
        print(xi,xj)
        if xi <= 15:
            if xj<=15:
                if vi==vj:
                    #print("repeti ese numero")
                    return False
            else:
                renglon, columna = obtener_renglon_columna(xi)
                if renglon == xj-16:
                    if vi != vj[xi//4]:
                        print(vi,vj[xi//4])
                        #print("no esta donde va")
                        return False
                if columna == xj-20:
                    if vi != vj[xi%4]:
                        #print("no esta donde va")
                        return False
                if esta_en_diagonal_enfrente(xi) and xj == 24:
                    print(xi)
                    if vi != vj[xi//5]:
                        return False
                if esta_en_diagonal_atras(xi) and xj == 25:
                    if vi != vj[(xi-3)//3]:
                        return False
        if xj <= 15:
            if xi<=15:
                if vi==vj:
                    return False
            else:
                renglon, columna = obtener_renglon_columna(xj)
                if renglon == xi-16:
                    if vj != vi[xj//4]:
                        #print("no esta donde va")
                        return False
                if columna == xi-20:
                    if vj != vi[xj%4]:
                        #print("no esta donde va")
                        return False
                if esta_en_diagonal_enfrente(xj) and xi == 24:
                    if vj != vi[xj//5]:
                        return False
                if esta_en_diagonal_atras(xj) and xj == 25:
                    if vj != vi[(xj-3)//3]:
                        return False
        if xj > 15 and xi > 15:
            if sum(vj) != sum(vi):
                #print("las sumas no son iguales")
                return False
            

        return True
      
def obtener_renglon_columna(i):
    renglon = i//4
    columna = i - 4*renglon
    return renglon, columna
    
def esta_en_diagonal_enfrente(i):
    de = 1 if i is 0 or i is 5 or i is 10 or i is 15 else 0
    return de
    
def esta_en_diagonal_atras(i):
    da = 1 if i is 3 or i is 6 or i is 9 or i is 12 else 0
    return da


def imprime_cuadrado(asignacion):

    s = [asignacion[i] for i in range(4)]
    rayita = '\n-------------+----------------+---------------\n'
    c = ''
    for i in range(9):
        c += ' '.join(str(s[9 * i + j]) +
                      ("  |  " if j % 3 == 2 and j < 7 else "   ")
                      for j in range(9))
        c += rayita if i % 3 == 2 and i < 7 else '\n'
    print(c)
    
#def resolver_cuadrado(CuadradoMagico):
 #   for _ in range(50)
if __name__ == "__main__":
    cuadrado = CuadradoMagico()
    sol = csp.asignacion_grafo_restriccion(cuadrado,consist= 2)
    print(sol)
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            