#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Este módulo contiene las clases que son utilizadas para representar los
distintos metodos de interpolación.

@autors Maximiliano Báez
@contact mxbg.py@gmail.com
"""

import numpy as np
import math

class Interpotalion :

    def simple_idw(self, src, grid, p=1.7):
        """
        Representa el método de interpolación de Ponderación de la inversa
        de la distancia (IDW), este estima los puntos del modelo realizando
        una asignación de pesos a los datos del entorno en función inversa
        a la distancia que los separa del punto en cuestión.

        @type  src : Grid
        @param src : La grilla de puntos de observación.

        @type  grid : Grid
        @param grid : La grilla de puntos autogenerados que se desea
                interpolar.

        @type  p : Float
        @param p : Es el parámetro del exponente que controla que tan
                rápido los pesos de los puntos tienden a cero (al
                aumentar su valor) conforme aumenta la distancia del
                sitio de interpolación.

        @rtype ndarray
        @return Un array con los valores calculados para la altura (Z)
                que corresponden a los puntos interpolados.
        """
        dist = src.distance_to(grid)

        # In IDW, weights are 1 / distance
        weights = 1.0 / (dist ** p)

        # Make weights sum to one
        weights /= weights.sum(axis=0)
        # Multiply the weights for each interpolated point by all observed Z-values
        zi = np.dot(weights.T, src.z)
        return zi


    def voronoi (self, src, grid):
        """
        """
        grid_len = len(grid)
        z_list = [];
        for i in range(len(grid)):
            dmin = math.hypot(grid_len-1, grid_len-1)
            z = 0;
            for j in range(len(src)):
                d = math.hypot(src.x[j]-grid.x[i], src.y[j]-grid.y[i])
                if d < dmin:
                    dmin = d
                    z = src.z[j]
            #se añade la altura estimada
            z_list.insert(i, z);
        return np.array(z_list, dtype=np.float)
