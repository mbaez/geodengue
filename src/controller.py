#! /usr/bin/env python
# -*- coding: utf-8 -*-
#~ import matplotlib
#~ import matplotlib.pyplot as plt
#~ import matplotlib.cm as cm
import numpy as np
#Se impotan los modulos.
from models import *
from db_manager import *
from interpolation import *
from simulador import *
__author__ = "Maximiliano Báez"
__mail__ = "mxbg.py@gmail.com"

class GisController :

    def __init__(self, id_muestras=1):
        print "obteniendo los datos"
        dao = PuntosControlModel()
        self.data = dao.get_by(id_muestras);

    def method_idw (self, cols=300, rows=300) :
        print "construyendo la grilla"
        #~ print data
        muestras = Grid();
        muestras.parse(self.data);
        #genera los n puntos
        print "generando los puntos a interpolar"
        grid = muestras.extend(cols, rows);
        alg = Interpotalion()
        # Calculate IDW
        print "Interpolando idw"
        interpolated_grid = alg.simple_idw(muestras,grid)
        #interpolated_grid = interpolated_grid.reshape(cols, rows)
        grid.z = interpolated_grid
        #~ self.__persist_grid__(grid, detalles);
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

    def method_voronoi (self, cols=300, rows=300) :
        print "construyendo la grilla"
        #~ print data
        muestras = Grid();
        muestras.parse(self.data);
        grid = muestras.extend(cols, rows);
        #genera los n puntos
        alg = Interpotalion()
        # Calculate IDW
        print "Interpolando voronoi"
        interpolated_grid = alg.voronoi(muestras, grid)
        grid.z = interpolated_grid
        #~ print grid
        print "done."
        return grid;

    def method_evolutive (self, cols=300, rows=300):
        print "obteniendo los datos climaticos"
        clima = TuTiempo("Asuncion")
        periodo = clima.get_periodo()
        #~ print data
        evol = Simulador(periodo=periodo, poblacion=self.data)
        print "iniciando simulación"
        evol.start()
        muestras_evol = evol.to_grid();
        print "generando los puntos a interpolar"
        grid = muestras_evol.extend(cols, rows);
        alg = Interpotalion()
        # Calculate IDW
        print "Interpolando idw"
        interpolated_grid = alg.simple_idw(muestras_evol,grid)
        #interpolated_grid = interpolated_grid.reshape(cols, rows)
        grid.z = interpolated_grid
        return grid

    def plot(self, grid, cols=300, rows=300):
        #djet = cmap_discretize(cm.jet, 1)
        bounds = grid.get_bounds()
        #~ points = grid
        points = self.muestras;
        #~ plt.figure()
        #~ plt.imshow(grid, extent=(x.min(), x.max(), y.max(), y.min()), cmap=djet)
        print grid.z
        z =  grid.z.reshape((cols, rows))
        print z[0][4]
        #~ print np.flipud(z)
        #~ print bounds.x_min, bounds.x_max, bounds.y_max, bounds.y_min
        #~ z =  grid.z;
        plt.imshow(z, extent=(bounds.x_min, bounds.x_max, bounds.y_max, bounds.y_min))
        #~ plt.imshow(z)
        plt.hold(True)
        plt.scatter(points.x,points.y,c=points.z)
        plt.colorbar()
        plt.title('IDW')
        #~ plt.show()

    def to_file (self, grid, cols=300, rows=300,suffix ="") :
        fo = open("/home/mbaez/Aplicaciones/geoserver2.3/data/coverages/arc_sample/test_"+suffix+".asc", "wb")
        fo.write( grid.to_raster(cols, rows));
        fo.close();

if __name__ == "__main__":
    gis = GisController();
    col= row = 300
    print "starting..."
    #~ resp = gis.method_voronoi(col,row);
    #~ resp = gis.method_idw(col,row)
    resp = gis.method_evolutive(col,row)
    print "parsing"
    #~ print resp
    #~ gis.plot(resp, col,row)
    gis.to_file(resp,col,row, "evol")
    print "end.."
