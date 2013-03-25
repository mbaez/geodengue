#! /usr/bin/env python
# -*- coding: utf-8 -*-
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cm
#Se impotan los modulos.
from base_model import *
from db_manager import *
from interpolation import *
__author__ = "Maximiliano Báez"
__mail__ = "mxbg.py@gmail.com"

class GisController :

    def __init__(self, id_muestras=1):
                #~ print "obteniendo los datos"
        #x, y, z, c = import_csv('data/larvitrampas.csv')
        dao = PuntosControlModel()
        data = dao.get_by(id_muestras);
        #~ print "construyendo la grilla"
        #~ print data
        self.id_muestras = id_muestras;
        self.muestras = Grid();
        self.muestras.parse(data);

    def method_idw (self, cols=300, rows=300) :
        #genera los n puntos
        #~ print "generando los puntos a interpolar"
        grid = self.muestras.extend(cols, rows);
        alg = Interpotalion()
        # Calculate IDW
        #~ print "Interpolando idw"
        interpolated_grid = alg.simple_idw(self.muestras,grid)
        #interpolated_grid = interpolated_grid.reshape(cols, rows)
        grid.z = interpolated_grid
        detalles = {
            'id_muestra' : self.id_muestras,
            'descripcion': 'Método utilizado SIMPLE IDW'
        }
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
        grid = self.muestras.extend(cols, rows);
        #genera los n puntos
        alg = Interpotalion()
        # Calculate IDW
        print "Interpolando voronoi"
        interpolated_grid = alg.voronoi(self.muestras, grid)
        grid.z = interpolated_grid
        #~ print grid
        print "done."
        return grid;

    def plot(self, grid, cols=300, rows=300):
        #djet = cmap_discretize(cm.jet, 1)
        bounds = grid.get_bounds()
        points = grid
        #~ points = self.muestras;
        plt.figure()
        #~ plt.imshow(grid, extent=(x.min(), x.max(), y.max(), y.min()), cmap=djet)
        z =  grid.z.reshape(cols, rows)
        #~ print len(grid.z)
        #~ print grid.z.tolist()
        z =  grid.z;
        print len(z)
        #~ plt.imshow(z, extent=(bounds.x_min, bounds.x_max, bounds.y_max, bounds.y_min))
        #~ plt.imshow(z)
        plt.hold(True)
        plt.scatter(points.x,points.y,c=points.z)
        plt.colorbar()
        plt.title('IDW')
        plt.show()


if __name__ == "__main__":
    gis = GisController();
    #~ resp = gis.method_voronoi(100,100);
    resp = gis.method_idw(100,100)
    print "parsing"
    #~ print resp
    gis.plot(resp, 100,100)
    print "end.."
