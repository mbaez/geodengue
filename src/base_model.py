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


import numpy

class Grid :
    """
    Clase para representar la grilla de puntos en 3 dimensiones (x,y,z). Un
    grilla esta compuesta por n puntos.
    """
    def __init__ (self, x=[], y=[], z=[]) :
        self.x = x;
        self.y = y;
        self.z = z;

    def parse (self, data) :
        """
        Este método se encarga de transformar un diccionario y inicializar
        el grid.

        @type data : Dictionaries
        @param data: El diccionario con lo s datos a procesar.

        """
        x,y,z =[],[],[];
        # se separan los datos en array indepedientes
        for i in range(len(data)):
            #~ print data[i]
            x.append(data[i]['x']);
            y.append(data[i]['y']);
            z.append(data[i]['cantidad']);

        # se inicializa el array
        self.x = numpy.array(x, dtype=numpy.float)
        self.y = numpy.array(y, dtype=numpy.float)
        self.z = numpy.array(z, dtype=numpy.float)

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

    def extend (self, cols, rows) :
        """
        Este método se encarga de generar un grid con `col*rows` puntos.
        Los puntos generados son equidistantes entre sí.

        @type  cols : Integer
        @param cols : La cantidad de columnas del nuevo grid.

        @type  rows : Integer
        @param rows : La cantidad de filas del nuevo grid.

        @rtype  : Grid
        @return : La grilla generada con los nuevos puntos.

        """
        bounds = self.get_bounds();
        xi = numpy.linspace(bounds.x_min, bounds.x_max, cols);
        yi = numpy.linspace(bounds.y_min, bounds.y_max, rows);
        #genera la matriz de coordenadas
        xi, yi = numpy.meshgrid(xi, yi)
        # Copia los subarrays en un un array de una dimensión
        xi, yi = xi.flatten(), yi.flatten();
        #se retorna el nuevo grid generado.
        return Grid(xi, yi);

    def distanceTo(self,grid):
        """
        Calcula la distancia entre los puntos pertenecientes a grilla
        actual y la grilla especificada.

        @type  grid : Grid
        @param grid : La grilla de puntos entre la que se

        @rtype ndarray
        @return La matriz de distancia entre la grilla de puntos.
        """
        obs = numpy.vstack((self.x, self.y)).T
        interp = numpy.vstack((grid.x, grid.y)).T

        # Make a distance matrix between pairwise observations
        # Note: from <http://stackoverflow.com/questions/1871536>
        # (Yay for ufuncs!)
        d0 = numpy.subtract.outer(obs[:,0], interp[:,0])
        d1 = numpy.subtract.outer(obs[:,1], interp[:,1])
        #Given the “legs” of a right triangle, return its hypotenuse.
        return numpy.hypot(d0, d1)

    def to_dict(self, args) :
        grid = []
        x = self.x.tolist();
        y = self.y.tolist();
        z = self.z.tolist();
        for i in range(len(x)):
            point = {'x' :x[i], 'y': y[i], 'cantidad':z[i]}
            data = dict(point.items() + args.items())
            grid.append(data)

        return grid

    def __str__(self):
        import geojson
        grid = [];
        xx = self.x.tolist();
        yy = self.y.tolist();
        zz = self.z.tolist();
        for i in range(len(xx)):
            point = geojson.Point([xx[i], yy[i]]);
            feature =  geojson.Feature(i, point,{'cantidad':zz[i]});
            #point = { 'x' : xx[i],'y' : yy[i],'z' : zz[i] };
            grid.append(feature);
        coll = geojson.FeatureCollection(grid)
        return geojson.dumps(coll);

class GridPolygon :
    def __init__(self, points) :
        self.points = points

    def __str__(self):
        import geojson
        grid = [];
        for i in range(len(self.points)) :
            polygon = geojson.Polygon(self.points[i])
            feature =  geojson.Feature(i, polygon,{});
            #point = { 'x' : xx[i],'y' : yy[i],'z' : zz[i] };
            grid.append(feature);
        coll = geojson.FeatureCollection(grid)
        return geojson.dumps(coll);
