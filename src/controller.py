#! /usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
# Se impotan los modulos.
from models import *
from db_manager import *
from interpolation import *
from simulador import *
from tutiempo import *
from geoserver import *

__author__ = "Maximiliano Báez"
__mail__ = "mxbg.py@gmail.com"


class GisController:

    def __init__(self, id_muestras=1):
        """
        Inicializa la clase, obtiene los datos correspondientes a la muestra
        indicada.

        @type id_muestras : Integer
        @param id_muestras : El identificador de la muestra.
        """
        print "obteniendo los datos"
        dao = PuntosControlModel()
        self.__id_muestra = id_muestras
        self.data = dao.get_by(id_muestras)
        self.layerDao = LayersDao()

    def method_idw(self, cols=300, rows=300):
        """
        Este método se encarga de interpolar el grid utilizando el método
        de idw.

        @type cols : Integer
        @param cols: La cantidad de columnas del grid

        @type rows : Integer
        @param rows: La cantidad de filas del grid

        @rtype  Grid
        @return El grid resultante de la interpolación de los puntos de
                control.
        """
        print "construyendo la grilla"
        #~ print data
        muestras = Grid()
        muestras.parse(self.data)
        # genera los n puntos
        print "generando los puntos a interpolar"
        grid = muestras.extend(cols, rows)
        alg = Interpotalion()
        # Calculate IDW
        print "Interpolando idw"
        interpolated_grid = alg.simple_idw(muestras, grid)
        grid.z = interpolated_grid
        #~ print "done."
        return grid

    def method_voronoi(self, cols=300, rows=300):
        """
        Se encarga de ejecutar el algoritmo de voronoi sobre los datos
        de la grilla.

        @type cols : Integer
        @param cols: La cantidad de columnas del grid

        @type rows : Integer
        @param rows: La cantidad de filas del grid

        @rtype  Grid
        @return El grid resultante de la interpolación de los puntos de
                control.
        """
        print "construyendo la grilla"
        #~ print data
        muestras = Grid()
        muestras.parse(self.data)
        grid = muestras.extend(cols, rows)
        # genera los n puntos
        alg = Interpotalion()
        # Calculate IDW
        print "Interpolando voronoi"
        interpolated_grid = alg.voronoi(muestras, grid)
        grid.z = interpolated_grid
        #~ print grid
        print "done."
        return grid

    def method_evolutive(self, cols=300, rows=300):
        """
        Este método se encarga de ejecutar el proceso evolutivo sobre los
        puntos de control de la muestra.

        @type cols : Integer
        @param cols: La cantidad de columnas del grid

        @type rows : Integer
        @param rows: La cantidad de filas del grid

        @rtype  Grid
        @return El grid resultante de la interpolación de los puntos de
                control.
        """
        print "obteniendo los datos climaticos"
        resp = {}
        clima = TuTiempo("Asuncion")
        periodo = clima.get_periodo()
        #~ print data
        evol = Simulador(periodo=periodo, poblacion=self.data)
        print "iniciando simulación"
        resp['poblacion'] = evol.start()
        resp['resumen'] = evol.poblacion.get_resumen()
        print "generando los puntos a interpolar"
        grid = resp['poblacion'].extend(cols, rows)
        alg = Interpotalion()
        # Calculate IDW
        print "Interpolando idw"
        interpolated_grid = alg.simple_idw(resp['poblacion'], grid)
        grid.z = interpolated_grid
        resp['grid'] = grid
        resp['poblacion'] = str(resp['poblacion'])
        return resp

    def to_geoserver(self, args):
        """
        Este método se encarga de traducir el grid a una capa raster que
        es publicada en el geoserver.

        @type grid : Grid
        @param grid: El grid que contiene los datos para publicar en el
                geoserver

        @type cols : Integer
        @param cols: La cantidad de columnas del grid

        @type rows : Integer
        @param rows: La cantidad de filas del grid

        @type suffix : String
        @param suffix: Identificador que forma parte del nombre del layer.

        @rtype  String
        @return El nombre del layer publicado en el geoserver.
        """
        grid = args.get('grid')
        cols = args.get('cols', 300)
        rows = args.get('rows', 300)
        store = args.get('layer_name')
        geo = Geoserver()
        #~ se crea el sotre para el layer
        geo.create_coverage_store(store)
        layer_name = "{0}.asc".format(store)
        print "tmp file.."
        #~ se mueve genera el layer en la carpeta temporal
        src_file = geo.tmp_buffer(store, grid.to_raster(cols, rows))
        #~ se añade el layer al geoserver
        print "uploading file.."
        geo.upload_file(src_file, layer_name)
        #~  se publica el layer
        print "publish file.."
        geo.publish_coverage(store)
        #~ se retorna el nombre del layer
        return store

    def gen_layer_name(self, args):
        """
        Se encarga de genear el nombre del layer
        @param args: Parametros utilizados para la generación de layers

        @keyword tipo: El tipo de layer a genear (inst|evol)
        """
        geo = Geoserver()
        args["id_muestra"] = self.__id_muestra
        return geo.gen_layer_name(args)

    def instantanea(self):
        """
        """
        print "verificando"
        layer_name = self.gen_layer_name({"tipo": "inst"})
        layer = self.layerDao.get_by(layer_name)
        if len(layer) == 1:
            return layer[0]
        else:
            layer = {
                "layer_name": layer_name,
                "id_muestra": self.__id_muestra,
                "fecha": "now()"
            }
            self.layerDao.persist(layer)
            print "starting..."
            data = {}
            data["grid"] = self.method_idw()
            data['layer_name'] = layer_name
            print "parsing"
            self.to_geoserver(data)
        return layer

    def evolucionar(self):
        """
        """
        print "verificando"
        layer_name = self.gen_layer_name({"tipo": "evol"})
        layer = self.layerDao.get_by(layer_name)
        if len(layer) == 1:
            return layer[0]
        else:
            layer = {
                "layer_name": layer_name,
                "id_muestra": self.__id_muestra,
                "fecha": "now()"
            }
            self.layerDao.persist(layer)
            print "starting..."
            data = self.method_evolutive()
            data['layer_name'] = layer_name
            print "parsing"
            self.to_geoserver(data)
            resp = {}
            resp['poblacion'] = data["poblacion"]
            resp['resumen'] = data["resumen"]
            resp['layer_name'] = layer_name
        return resp


class MuestrasController:

    def __init__(self):
        """
        Inicializa la clase muestras
        """
        self.dao = MuestraModel()

    def get_all_muestras(self):
        """
        Se encarga de obtener los datos de la tabla de muestras
        """
        return self.dao.get_all()


if __name__ == "__main__":
    gis = GisController(1)
    col = row = 300
    print "starting..."
    #~ resp = gis.method_voronoi(col,row);
    resp = gis.evolucionar()
    print resp
    # print "{x_min: -57.602724725986, ymin: -25.318104903934, x_max: -57.580130758362, y_max: -25.299749132232}"
    # resp = gis.method_evolutive()
    # print "parsing"
    #~ print resp
    #~ gis.plot(resp, col,row)
    #~ gis.to_file(resp,col,row)
    # layer = gis.to_geoserver(resp, col, row, "evol")
    # print layer
    #
    print "end.."
