#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
sudoku.py
------------

Los Sudokus son unos juegos de origen Japones. El juego tiene un
tablero de 9 x 9 casillas.  En cada casilla se debe asignar un número
1, 2, 3, 4, 5, 6, 7, 8 o 9.

La idea principal de juego es establecer los valores de los números en
las casillas no asignadas anteriormente si se considera que:

    a) Las casillas horizontales deben tener números diferentes entre si
    b) Las casillas verticales deben tener números diferentes entre si
    c) Las casillas que pertenecen al mismo grupo deben tener números
       diferentes entre si.

Sea (r1, c1) el renglon y la columna de una casilla y (r2, c2) el
renglon y la columna de otra casilla, se dice que las casillas
pertenecen al mismo grupo si y solo si r1/3 == r2/3 y c1/3 == c2/3
donde / es la división entera (por ejemplo 4/3 = 1 o 8/3 = 2).  Esto
aplica si se considera 0 como la primer posición.

Para más información sobre sudokus, pueden googlearlo, buscarlos en
wikipedia o comprar un librito de sudokus de 8 pesos (cuidado, se
puede perder mucho tiempo resolviendo sudokus).


Para revisar la tarea es necesario seguir las siguientes
instrucciones:

Un Sudoku se inicializa como una lista de 81 valores donde los valores
se encuentran de la manera siguiente:

    0   1   2 |  3   4   5 |  6   7   8
    9  10  11 | 12  13  14 | 15  16  17
   18  19  20 | 21  22  23 | 24  25  26
   -----------+------------+------------
   27  28  29 | 30  31  32 | 33  34  35
   36  37  38 | 39  40  41 | 42  43  44
   45  46  47 | 48  49  50 | 51  52  53
   -----------+------------+------------
   54  55  56 | 57  58  59 | 60  61  62
   63  64  65 | 66  67  68 | 69  70  71
   72  73  74 | 75  76  77 | 78  79  80

    k//9 #da las y
    k%9  #da las x
    [[y*9 + i for i in range(9) if i != x]+
     [i*9 + x for i in range(9) if i != y]+
     [i+(x//3)*3 + j*9+(y//3)*27 for i in range(3) for j in range(3)]]

hasta llegar a la posición 81.

Los valores que puede tener la lista son del 0 al 9. Si tiene un 0
entonces es que el valor es desconocido.

"""

__author__ = 'juliowaissman'


import csp


class Sudoku(csp.GrafoRestriccion):
    """
    Esta es la clase que tienen que desarrollar y comentar. Las
    variables están dadas desde 0 hasta 81 (un vector) tal como dice
    arriba. No modificar nada de lo escrito solamente agregar su
    código.

    """

    def __init__(self, pos_ini):
        """
        Inicializa el sudoku

        """
        super().__init__()

        self.dominio = {i: [val] if val > 0 else list(range(1, 10))
                        for (i, val) in enumerate(pos_ini)}

        vecinos = {}
        # =================================================================
        #  25 puntos: INSERTAR SU CÓDIGO AQUI (para vecinos)
        # =================================================================
        for k in self.dominio.keys():
            x=k%9  #da las x
            y=k//9 #da las y
            a=[[y*9 + i for i in range(9) if i != x]+
            [i*9 + x for i in range(9) if i != y]+
            [i+(x//3)*3 + j*9+(y//3)*27 for i in range(3)for j in range(3)]]
            vecinos[k] = list(set(a[0])-set([k]))
        self.vecinos = vecinos
        if not vecinos:
            raise NotImplementedError("Faltan los vecinos")

    def restricción(self, xi_vi, xj_vj):
        """
        El mero chuqui. Por favor comenta tu código correctamente

        """
        xi, vi = xi_vi
        xj, vj = xj_vj
        return vi != vj
        # =================================================================
        #  25 puntos: INSERTAR SU CÓDIGO AQUI
        # (restricciones entre variables vecinas)
        # =================================================================
        raise NotImplementedError("Implementa la restricción binaria")


def imprime_sdk(asignación):
    """
    Imprime un sudoku en pantalla en forma más o menos graciosa. Esta
    función solo sirve para la tarea y para la revisión de la
    tarea. No modificarla por ningun motivo.

    """
    s = [asignación[i] for i in range(81)]
    rayita = '\n-------------+----------------+---------------\n'
    c = ''
    for i in range(9):
        c += ' '.join(str(s[9 * i + j]) +
                      ("  |  " if j % 3 == 2 and j < 7 else "   ")
                      for j in range(9))
        c += rayita if i % 3 == 2 and i < 7 else '\n'
    print(c)


if __name__ == "__main__":
    # =========================================================================
    # Una forma de verificar si el código que escribiste es correcto
    # es verificando que la solución sea satisfactoria para estos dos
    # sudokus.
    # =========================================================================

    s1 =   [8, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 3, 6, 0, 0, 0, 0, 0,
            0, 7, 0, 0, 9, 0, 2, 0, 0,
                0, 5, 0, 0, 0, 7, 0, 0, 0,
            0, 0, 0, 0, 4, 5, 7, 0, 0,
            0, 0, 0, 1, 0, 0, 0, 3, 0,
            0, 0, 1, 0, 0, 0, 0, 6, 8,
            0, 0, 8, 5, 0, 0, 0, 1, 0,
            0, 9, 0, 0, 0, 0, 4, 0, 0]

    imprime_sdk(s1)
    print("Solucionando un Sudoku dificil")
    sudoku1 = Sudoku(s1)
    sol1 = csp.asignacion_grafo_restriccion(sudoku1)
    imprime_sdk(sol1)

    s2 = [4, 0, 0, 0, 0, 0, 8, 0, 5,
          0, 3, 0, 0, 0, 0, 0, 0, 0,
          0, 0, 0, 7, 0, 0, 0, 0, 0,
          0, 2, 0, 0, 0, 0, 0, 6, 0,
          0, 0, 0, 0, 8, 0, 4, 0, 0,
          0, 0, 0, 0, 1, 0, 0, 0, 0,
          0, 0, 0, 6, 0, 3, 0, 7, 0,
          5, 0, 0, 2, 0, 0, 0, 0, 0,
          1, 0, 4, 0, 0, 0, 0, 0, 0]

    imprime_sdk(s2)
    sudoku2 = Sudoku(s2)
    print("Y otro tambien dificil")
    sol2 = csp.asignacion_grafo_restriccion(sudoku2)
    imprime_sdk(sol2)
