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
    """
    Representa el método de interpolación de Ponderación de la inversa de
    la distancia (IDW), este estima los puntos del modelo realizando una
    asignación de pesos a los datos del entorno en función inversa a la
    distancia que los separa del punto en cuestión.
    """
    def simple_idw(self, x, y, z, xi, yi):
        dist = self.distance_matrix(x,y, xi,yi)

        # In IDW, weights are 1 / distance
        weights = 1.0 / dist

        # Make weights sum to one
        weights /= weights.sum(axis=0)

        # Multiply the weights for each interpolated point by all observed Z-values
        zi = np.dot(weights.T, z)
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


    def scipy_idw(self, x, y, z, xi, yi):
        interp = Rbf(x, y, z, function='linear')
        return interp(xi, yi)

    def distance_matrix(self,x0, y0, x1, y1):
        obs = np.vstack((x0, y0)).T
        interp = np.vstack((x1, y1)).T

        # Make a distance matrix between pairwise observations
        # Note: from <http://stackoverflow.com/questions/1871536>
        # (Yay for ufuncs!)
        d0 = np.subtract.outer(obs[:,0], interp[:,0])
        d1 = np.subtract.outer(obs[:,1], interp[:,1])

        return np.hypot(d0, d1)
