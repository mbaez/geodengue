#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Este módulo contiene las clases que son utilizadas para representar los
distintos metodos de interpolación.
"""
__author__ = "Maximiliano Báez"
__mail__ = "mxbg.py@gmail.com"

import numpy as np
import math
from scipy.interpolate import Rbf

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
        dist = src.distanceTo(grid)

        # In IDW, weights are 1 / distance
        weights = 1.0 / (dist ** p)

        # Make weights sum to one
        weights /= weights.sum(axis=0)
        # Multiply the weights for each interpolated point by all observed Z-values
        zi = np.dot(weights.T, src.z)
        return zi

    def voronoi(self, src):
        poligon = []

        for i in range(len(src.y)):
            poligon.append([]);

        for y in range(len(src.y)):
            dmin = math.hypot(len(src.x)-1, len(src.y)-1)
            #~ print dmin
            j = -1
            for i in range(len(src.x)):
                d = math.hypot(src.x[i]-src.x[y], src.y[i]-src.y[y])
                print str(d) + ' < ' + str(dmin)
                if d < dmin:
                    dmin = d
                    j = i
            poligon[j].append([src.x[j],src.y[j]])
        return poligon

