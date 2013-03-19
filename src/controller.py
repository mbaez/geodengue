#! /usr/bin/env python
# -*- coding: utf-8 -*-

#Se impotan los modulos.
from base_model import *
from interpolation import *
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

    def method_idw (self, cols=100, rows=100) :
        #print "obteniendo los datos"
        x, y, z, c = import_csv('data/larvitrampas.csv')
        muestras = Grid(x, y, z);
        #genera los n puntos
        #print "generando los puntos a interpolar"
        grid = muestras.extend(cols, rows);
        alg = Interpotalion()
        # Calculate IDW
        #print "Interpolando idw"
        interpolated_grid = alg.simple_idw(muestras,grid)
        #interpolated_grid = interpolated_grid.reshape(cols, rows)
        grid.z = interpolated_grid
        #print "done."
        return grid;

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
    resp = gis.method_voronoi();
    print "parsing"
    print "" + str(resp)
    print "end.."

