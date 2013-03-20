#! /usr/bin/env python
# -*- coding: utf-8 -*-

#Se impotan los modulos.
from base_model import *
from db_manager import *
from interpolation import *
__author__ = "Maximiliano Báez"
__mail__ = "mxbg.py@gmail.com"

def import_csv (filename):
    import csv
    import numpy as np
    x,y,z,c =[],[],[],[];
    with open(filename, 'rb') as f:
        mycsv = csv.reader(f,delimiter=',')
        for row in mycsv:
            z.append(float(row[1]))
            x.append(float(row[2]))
            y.append(float(row[3]))
            c.append([float(row[1]),float(row[2])])

    return np.array(x, dtype=np.float),\
            np.array(y,dtype=np.float),\
            np.array(z,dtype=np.float),\
            np.array(c,dtype=np.float)

class GisController :

    def __init__(self):
        pass;

    def method_idw (self, id_muestras=1, cols=100, rows=100) :
        #~ print "obteniendo los datos"
        #x, y, z, c = import_csv('data/larvitrampas.csv')
        dao = PuntosControlModel()
        data = dao.get_by(id_muestras);
        #~ print "construyendo la grilla"
        #~ print data
        muestras = Grid();
        muestras.parse(data);
        #genera los n puntos
        #~ print "generando los puntos a interpolar"
        grid = muestras.extend(cols, rows);
        alg = Interpotalion()
        # Calculate IDW
        #~ print "Interpolando idw"
        interpolated_grid = alg.simple_idw(muestras,grid)
        #interpolated_grid = interpolated_grid.reshape(cols, rows)
        grid.z = interpolated_grid
        detalles = {
            'id_muestra' : id_muestras,
            'descripcion': 'Método utilizado SIMPLE IDW'
        }
        self.__persist_grid__(grid, detalles);
        #~ print "done."
        return grid;

    def __persist_grid__(self, grid, args) :
           cabecera = InterpolacionModel()
           detalle = PuntosInterpoladosModel()
           # se persite la cabecera
           cursor = cabecera.persist(args);
           # se obtiene el id de la cabecera recién persitida
           id_cabecera = cursor.fetchone()[0];
           # se consturye el dic con parametros extras
           params = {'id_interpolacion' : id_cabecera}
           # se persite los detalles
           detalle.persist(grid.to_dict(params))

    def method_voronoi (self) :
        print "obteniendo los datos"
        x, y, z, c = import_csv('data/larvitrampas.csv')
        muestras = Grid(x, y, z);
        #genera los n puntos
        alg = Interpotalion()
        # Calculate IDW
        print "Interpolando voronoi"
        grid = GridPolygon(alg.voronoi(muestras))
        #~ print grid
        print "done."
        return grid;

if __name__ == "__main__":
    gis = GisController();
    resp = gis.method_idw();
    print "parsing"
    print "end.."
