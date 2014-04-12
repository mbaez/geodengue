#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Este módulo contiene las clases que representa los objetos utilizados para
procesamiento espacial.

@autors Maximiliano Báez
@contact mxbg.py@gmail.com
"""

import numpy
import math
import cmath
import types


class Bounds:

    """
    Clase para representar la extensión de los puntos. La extensión de se
    encuentra compuesta por un conjunto de puntos
        x_min : El minimo valor de x
        x_max : El máximo valor de x
        y_min : El minimo valor de y
        y_max : El máximo valor de y
    """

    def __init__(self, x_min=0, x_max=0, y_min=0, y_max=0):
        self.x_min = x_min
        self.y_min = y_min
        self.x_max = x_max
        self.y_max = y_max

    def parse_array(self, x_array, y_array):
        """
        Este método se encarga de obtener el par de valores min y max
        correspondiente a cada array y setear los valores a los atributos
        de la clase.

        @type  x_array : Array
        @param x_array : Lista de puntos correspondientes al eje x

        @type  y_array : Array
        @param y_array : Lista de puntos correspondientes al eje y
        """
        if len(x_array) == len(y_array) and len(x_array) > 0:
            self.x_min = x_array.min()
            self.y_min = y_array.min()
            self.x_max = x_array.max()
            self.y_max = y_array.max()

    def __str__(self):
        to_str = 'min x : ' + str(self.x_min) + \
            'min y : ' + str(self.y_min) + \
            'max x : ' + str(self.x_max) + \
            'max y : ' + str(self.y_max)
        return to_str


class Grid:

    """
    Clase para representar la grilla de puntos en 3 dimensiones (x,y,z). Un
    grilla esta compuesta por n puntos.
    """

    def __init__(self, x=[], y=[], z=[]):
        self.x = x
        self.y = y
        self.z = z

    def parse(self, data):
        """
        Este método se encarga de transformar un diccionario y inicializar
        el grid.

        @param data: El diccionario con lo s datos a procesar.
        @type data : Dictionaries
        """
        x, y, z, ids = [], [], [], []
        # se separan los datos en array indepedientes
        for i in range(len(data)):
            x.append(data[i]['x'])
            y.append(data[i]['y'])
            z.append(data[i]['cantidad'])
            ids.append(data[i]['id'])

        # se inicializa el array
        self.x = numpy.array(x, dtype=numpy.float)
        self.y = numpy.array(y, dtype=numpy.float)
        self.z = numpy.array(z, dtype=numpy.float)
        self.ids = ids

    def get_bounds(self):
        """
        Este método se encarga de obtener la extensión de la grilla de
        puntos.

        @return: La extensión de la grilla de puntos.
        @rtype: Bounds
        """
        bounds = Bounds()
        bounds.parse_array(self.x, self.y)
        print bounds
        return bounds

    def extend(self, cols, rows):
        """
        Este método se encarga de generar un grid con `col*rows` puntos.
        Los puntos generados son equidistantes entre sí.

        @param cols : La cantidad de columnas del nuevo grid.
        @type  cols : Integer

        @param rows : La cantidad de filas del nuevo grid.
        @type  rows : Integer

        @return: La grilla generada con los nuevos puntos.
        @rtype: Grid
        """
        bounds = self.get_bounds()
        xi = numpy.linspace(bounds.x_min, bounds.x_max, cols)
        yi = numpy.linspace(bounds.y_min, bounds.y_max, rows)
        # genera la matriz de coordenadas
        xi, yi = numpy.meshgrid(xi, yi)
        # Copia los subarrays en un un array de una dimensión
        xi, yi = xi.flatten(), yi.flatten()
        # se retorna el nuevo grid generado.
        return Grid(xi, yi)

    def distance_to(self, grid):
        """
        Calcula la distancia entre los puntos pertenecientes a grilla
        actual y la grilla especificada.

        @param grid : La grilla de puntos entre la que se
        @type  grid : Grid

        @return: La matriz de distancia entre la grilla de puntos.
        @rtype: ndarray
        """
        obs = numpy.vstack((self.x, self.y)).T
        interp = numpy.vstack((grid.x, grid.y)).T

        # Make a distance matrix between pairwise observations
        # Note: from <http://stackoverflow.com/questions/1871536>
        # (Yay for ufuncs!)
        d0 = numpy.subtract.outer(obs[:, 0], interp[:, 0])
        d1 = numpy.subtract.outer(obs[:, 1], interp[:, 1])
        # Given the “legs” of a right triangle, return its hypotenuse.
        return numpy.hypot(d0, d1)

    def to_raster(self, cols, rows, nodata_value=-9999):
        """
        Se encarga de generar un capa raster en el formato
        <a href="http://en.wikipedia.org/wiki/Esri_grid">Esri grid.</a>

        @param cols : La cantidad de columnas de la matriz
        @type  cols : Integer

        @param rows : La cantidad de filas de la matiz
        @type  rows : Integer

        @return: Un string que representa la capa raster en el formato
                de esri grid.
        @rtype: String

        """
        # se gira la matriz
        z = numpy.flipud(self.z.reshape((cols, rows)))
        # se obtiene la extensión del grid
        bounds = self.get_bounds()
        # Se calcula el size de la celda
        size = float(abs((bounds.y_max - bounds.y_min) / (cols)))
        print size
        size = abs((bounds.y_max - bounds.y_min) / (cols))
        print size
        # Se construye la cabecera del raster
        out = "ncols\t" + str(cols)
        out += "\nnrows\t" + str(rows)
        out += "\nxllcorner\t" + str(bounds.x_min)
        out += "\nyllcorner\t" + str(bounds.y_min)
        out += "\ncellsize\t" + str(size)
        out += "\nNODATA_value\t" + str(nodata_value)
        # Se construye la matriz con las alturas
        for i in range(rows):
            out += "\n"
            for j in range(cols):
                out += str(z[i][j]) + " "
        # se retorna el raster como un string
        return out

    def to_dict(self, args):
        """
        Este metodo se encarga de generar un diccionario de los atributos
        de la clase.
        """
        grid = []
        x = self.x.tolist()
        y = self.y.tolist()
        z = self.z.tolist()
        for i in range(len(x)):
            point = {'x': x[i], 'y': y[i], 'cantidad': z[i]}
            data = dict(point.items() + args.items())
            grid.append(data)

        return grid

    def __len__(self):
        return len(self.x)

    def __str__(self):
        import geojson
        grid = []
        xx = self.x.tolist()
        yy = self.y.tolist()
        zz = self.z.tolist()
        for i in range(len(xx)):
            point = geojson.Point([xx[i], yy[i]])
            feature = geojson.Feature(i, point, {'cantidad': zz[i]})
            grid.append(feature)
        coll = geojson.FeatureCollection(grid)
        return geojson.dumps(coll)


class Point:

    """
    Esta clase define la geometría de un punto y las operaciones que se
    pueden realizar sobre el mismo.
    """
    @property
    def x(self):
        """Coordenada X"""
        return self.__x

    @x.setter
    def x(self, value):
        self.__x = value

    @property
    def y(self):
        """Coordenada Y"""
        return self.__y

    @y.setter
    def y(self, value):
        self.__y = value

    def to_metter(self, delta):
        """
        Se encarga de traducir la diferencia de las distancias a metros

        @param delta : El número que se desea traducir a metros.
        @type  delta : Float

        @return: La distancia en metros.
        @rtype: Float
        """
        return 100000.0 * delta

    def to_units(self, delta):
        """
        Se encarga de traducir de metros a unidades

        @param delta : El número que se desea traducir a unidades.
        @type  delta : Float

        @return: La distancia en unidades.
        @rtype: Float
        """
        return delta / 100000.0

    def __init__(self, args):
        self.__x = args.get('x', 0)
        self.__y = args.get('y', 0)

    def distance_to(self, point):
        """
        Halla la distancia entre 2 puntos utilizando el teorema de
        pitagoras aplicado a la geometría de triangulos.


        @param point : El punto destino
        @type  point : Point

        @return: La distancia en metros.
        @rtype: Float
        """
        if type(point) is types.DictType:
            point = Point(point)

        #~ Se encuentra la distancia de la latitud o distancia entre los
        #~ puntos  x
        d_lat = (point.x - self.x)
        #~ Se encuentra la distancia de la longitud o distancia entre los
        #~ puntos y
        d_lng = (point.y - self.y)

        #~  se realiza una suma de las potencias
        suma_potencias = (d_lat * d_lat) + (d_lng * d_lng)
        resultado = math.sqrt(suma_potencias)

        return self.to_metter(resultado)

    def move(self, distance, angle=0):
        """
        Proyecta el punto sobre una linea que forma un angulo 'angle' sobre
        el eje horizontal. El punto se proyecta a una distancia 'distance'
        del punto de origen. El punto proyectado pasar a ser la nueva
        ubicación.

        @param distance : La distancia en metros
        @type  distance : Float

        @param angle : El angulo en grados
        @type  angle : Float
        """
        point = self.project(distance, angle)
        self.x = point.x
        self.y = point.y

    def project(self, distance, angle=0):
        """
        Proyecta el punto sobre una linea que forma un angulo 'angle' sobre
        el eje horizontal. El punto se proyecta a una distancia 'distance'
        del punto de origen.

        @param distance : La distancia en metros
        @type  distance : Float

        @param angle : El angulo en grados
        @type  angle : Float

        @return: El punto proyectado
        @rtype: Point
        """
        # convert bearing to arithmetic angle in radians
        angle = 90 - angle
        if angle < - 180:
            angle = 360 + angle

        #~ se traduce la distancia en metros a unidades
        distance = self.to_units(distance)
        #~ se traduce el angulo en radianes
        angle = math.radians(angle)
        start = complex(self.x, self.y)
        #~ se genera una recta
        movement = cmath.rect(distance, angle)
        #~ se proyecta el punto
        end = start + movement

        args = {}
        args["x"] = end.real
        args["y"] = end.imag
        #~ se genera un punto
        return Point(args)

    def clone(self):
        """
        Se encarga de clonar el punto actual

        @return: El punto clon del punto actual
        @rtype: Point
        """
        point = {}
        point["x"] = self.x
        point["y"] = self.y
        return Point(point)

    def angle_to(self, point):
        """
        Se encarga de calcular el angulo entre 2 puntos según se describe en
        el siguiente post de stackoverflow
        http://stackoverflow.com/questions/7586063/how-to-calculate-the-angle-between-a-line-and-the-horizontal-axis

        @param point : El punto destino
        @type  point : Point
        """
        # First find the difference between the start point and the end point.
        deltaY = point.y - self.y
        deltaX = point.x - self.x
        # Then calculate the angle.
        angleInDegrees = math.atan2(deltaY, deltaX) * 180 / math.pi
        return angleInDegrees

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"


if __name__ == "__main__":
    p1 = {"x": -57.6581, "y": -25.2928}
    p2 = {"x": -57.343086004255, "y": -25.387185928441}
    p3 = {"x": -57.343086, "y": -25.387186}
    src = Point(p2)
    des = Point(p3)
    #~ des = src.project(100,90);
    print str(des.x) + " " + str(des.y)

    print src.distance_to(des)
