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

from pyproj import Proj
import shapely.geometry
from shapely.geometry import MultiPoint
from shapely.geometry.polygon import Polygon

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
            ' min y : ' + str(self.y_min) + \
            ' max x : ' + str(self.x_max) + \
            ' max y : ' + str(self.y_max)
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
        self.proj = Proj(proj='utm',zone=27,ellps='WGS84')
        self.nodata_value =-9999
        

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
        
        #se proyecta las esquinas a 200 metros para que la grilla temga una mayor
        #extensión
#        top_corner, bottom_corner = self.normalizar_tamano()
#        
#        x.append(top_corner.x) 
#        y.append(top_corner.y) 
#        z.append(-1) 
#        self.ids.append(-1)
#        
#        x.append(bottom_corner.x) 
#        y.append(bottom_corner.y) 
#        z.append(-1) 
#        self.ids.append(-1)
#        
#        # se inicializa el array
#        self.x = numpy.array(x, dtype=numpy.float)
#        self.y = numpy.array(y, dtype=numpy.float)
#        self.z = numpy.array(z, dtype=numpy.float)
        
    def normalizar_tamano (self):
        """
        """
        bounds = self.get_bounds()
        
        p1 = shapely.geometry.Point(self.proj(bounds.x_min, bounds.y_min))
        p2 = shapely.geometry.Point(self.proj(bounds.x_min, bounds.y_max))
        p3 = shapely.geometry.Point(self.proj(bounds.x_max, bounds.y_max))
        
        dist_v = p1.distance(p2)
        dist_h = p2.distance(p3)
        
        if dist_v > dist_h :
            d_v = 0
            d_h = float(dist_v)*1.0 - float(dist_h)*1.0
            
        elif dist_h >  dist_v:
            d_h = 0
            d_v = float(dist_h)*1.0 - float(dist_v)*1.0
        else :
            d_v = 0
            d_h = 0
            
        x_y_min = Point({"x" :bounds.x_min, "y" :bounds.y_min});
        x_y_max = Point({"x" :bounds.x_max, "y" :bounds.y_max});
        
        #print "#1 "+ str(d_h)+" : "+ str(d_v)
        delta_h = 0 
        delta_v = 0
        
        if d_h > 0 :
            delta_h += float(d_h/2)
            
        elif d_v > 0 :
            delta_v += float(d_v/2)
    
        xy_min = x_y_min.project(delta_v, 270);
        xy_min = xy_min.project(delta_h, 180);
        
        xy_max = x_y_max.project(delta_v, 90);
        xy_max = xy_max.project(delta_h, 0)
        
        return xy_min, xy_max


    def get_bounds(self):
        """
        Este método se encarga de obtener la extensión de la grilla de
        puntos.

        @return: La extensión de la grilla de puntos.
        @rtype: Bounds
        """
        bounds = Bounds()
        bounds.parse_array(self.x, self.y)
        #print bounds
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

    def to_raster(self, cols, rows):
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
        x = numpy.flipud(self.x.reshape((cols, rows)))
        y = numpy.flipud(self.y.reshape((cols, rows)))
        # se obtiene la extensión del grid
        bounds = self.get_bounds()
        # Se calcula el size de la celda    
        x_min = y_min = 0.0
        x_max = y_max = self.nodata_value
        
        values =""
        # Se construye la matriz con las alturas
        for i in range(rows):
            values += "\n"
            for j in range(cols):
                if x_min > x[i][j] :
                    x_min = x[i][j]
                elif x_max <  x[i][j] :
                    x_max = x[i][j]
                
                if y_min > y[i][j] :
                    y_min = y[i][j]
                elif y_max <  y[i][j] :
                    y_max = y[i][j]
                    
                values += str(z[i][j]) + " "
        
        x_min = float('{0:.4f}'.format(x_min))
        y_min = float('{0:.4f}'.format(y_min))
        
        #Se calcula el tamaño de la celda
        size_y = abs((y_max - y_min) / (cols * 1.0))
        size_x = abs((x_max - x_min) / (cols * 1.0))
        #print str(size_x) + " : " + str(size_y)
        size = size_y
        if size_x > size_y:
            size = size_x
        size = size + (size)/(cols)
        # Se construye la cabecera del raster
        out = "ncols\t" + str(cols)
        out += "\nnrows\t" + str(rows)
        out += "\nxllcorner\t" + str(x_min)
        out += "\nyllcorner\t" + str(y_min)
        out += "\ncellsize\t" + '{0:.10f}'.format(size)
        out += "\nNODATA_value\t" + str(self.nodata_value)
        #se añade el value
        out += values;
        # se retorna el raster como un string
        return out
    
    def convex_hull(self, data) :
        """
        """
        pts = []
        # se separan los datos en array indepedientes
        for i in range(len(data)):
            pts.append(self.proj(data[i]['x'], data[i]['y']))
        polygon = MultiPoint(pts).convex_hull
        for i in range(len(self.x)):
            point = shapely.geometry.Point(self.proj(self.x[i],self.y[i]))
            dist = point.distance(polygon)
            #print dist
            if int(dist) > 200 :
                self.z[i] = self.nodata_value
        
    
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
        self.proj = Proj(proj='utm',zone=27,ellps='WGS84')

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
        angle = math.atan2(deltaY, deltaX) * 180 / math.pi
        if angle >= 90:
            angle = 360 - abs(angle - 90)
        else:
            angle = abs(angle - 90)
        return angle

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"


if __name__ == "__main__":
    p = {"x": -57.343086004255, "y": -25.387185928441}
    src = Point(p)
    for angle in [0, 30, 60, 90, 120, 160, 180, 200, 245, 270, 330, 360]:
        des = src.project(100, angle)
        a = src.angle_to(des)
        #print str(angle) + " ==? " + str(a)
