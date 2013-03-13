#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Este módulo contiene las clases que son utilizadas para representar los
distintos metodos de interpolación.
"""
__author__ = "Maximiliano Báez"
__mail__ = "mxbg.py@gmail.com"

import numpy as np
from scipy.interpolate import Rbf

class Idw :

    def simple_idw(self, src, grid, p=2):
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
        print weights.T
        # Multiply the weights for each interpolated point by all observed Z-values
        zi = np.dot(weights.T, src.z)
        return zi

    def linear_rbf(self, x, y, z, xi, yi):
        dist = self.distance_matrix(x,y, xi,yi)

        # Mutual pariwise distances between observations
        internal_dist = self.distance_matrix(x,y, x,y)

        # Now solve for the weights such that mistfit at the observations is minimized
        weights = np.linalg.solve(internal_dist, z)

        # Multiply the weights for each interpolated point by the distances
        zi =  np.dot(dist.T, weights)
        return zi
