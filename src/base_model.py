#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Este módulo contiene las clases que representa los objetos bases que son
utilizados para realizar las operaciones correspondientes.
"""
__author__ = "Maximiliano Báez"
__mail__ = "mxbg.py@gmail.com"
class Bounds :
"""
Clase para representar la extensión de los puntos. La extensión de se
encuentra compuesta por un conjunto de puntos
    x_min : El minimo valor de x
    x_max : El máximo valor de x
    y_min : El minimo valor de y
    y_max : El máximo valor de y
"""
    def __init__(self, x_min=0, x_max=0, y_min=0, y_max=0):
        self.x_min = x_min;
        self.y_min = y_min;
        self.x_max = x_max;
        self.y_max = y_max;

    def parse_array (self, x_array, y_array):
        """
        Este método se encarga de obtener el par de valores min y max
        correspondiente a cada array y setear los valores a los atributos
        de la clase.

        @type  x_array : Array
        @param x_array : Lista de puntos correspondientes al eje x

        @type  y_array : Array
        @param y_array : Lista de puntos correspondientes al eje y
        """
        self.x_min = x_array.min();
        self.y_min = y_array.min();
        self.x_max = x_array.max();
        self.y_max = y_array.max();


class Grid :
"""
Clase para representar la grilla de puntos en 3 dimensiones (x,y,z). Un
grilla esta compuesta por n puntos.
"""
    def __init__ (self, x=[], y=[], z=[]) :
        self.x = x;
        self.y = y;
        self.z = z;

    def get_bounds(self):
        """
        Este método se encarga de obtener la extensión de la grilla de
        puntos.

        @rtype  : Bounds
        @return : La extensión de la grilla de puntos.
        """
        bounds = Bounds();
        bounds.parse_array(self.x, self.y);
        return bounds;
