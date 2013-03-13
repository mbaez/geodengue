# -*- coding: utf-8 -*-
#se importan los libs correspondientes
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import csv

#Se impotan los modulos.
from base_model import *
from interpolation import *
from idw_test import Invdisttree

def main():
    n = 100
    nx, ny = 50, 50
    #x, y, z = map(np.random.random, [n, n, n])
    x, y, z, c = import_csv('data/larvitrampas.csv')
    muestras = Grid(x, y, z);
    #genera los n puntos
    grid = muestras.gen_grid(nx, ny);
    alg = Idw()
    # Calculate IDW
    interpolated_grid = alg.simple_idw(muestras,grid)
    interpolated_grid = interpolated_grid.reshape((ny, nx))

    plot(muestras.x,muestras.y,muestras.z,interpolated_grid)
    plt.title('IDW')
    plt.show()

def main2 () :
    N = 50
    Ndim = 2
    Nask = N  # N Nask 1e5: 24 sec 2d, 27 sec 3d on mac g4 ppc
    Nnear = 8  # 8 2d, 11 3d => 5 % chance one-sided -- Wendel, mathoverflow.com
    leafsize = 10
    eps = .1  # approximate nearest, dist <= (1 + eps) * true nearest
    p = 1  # weights ~ 1 / distance**p
    cycle = .25
    seed = 1
    print "inicializando.."
    x, y, z, known = import_csv('data/larvitrampas.csv')
    invdisttree = Invdisttree( known, z, leafsize=leafsize, stat=1 )
    xi = numpy.linspace(x.min(), x.max(), N);
    yi = numpy.linspace(y.min(), y.max(), N);
    xi, yi = numpy.meshgrid(xi, yi)
    #Copia los subarrays en un un array de una dimensión
    xi, yi = xi.flatten(), yi.flatten();
    ask = [];
    for i in range(len(xi)) :
        ask.append([xi[i], yi[i]]);
    ask = np.array(ask,dtype=np.int)
    print "starting.."
    interpol = invdisttree( ask, nnear=Nnear, eps=eps, p=p )


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

def plot(x,y,z,grid):
    #djet = cmap_discretize(cm.jet, 1)
    plt.figure()
    #plt.imshow(grid, extent=(x.min(), x.max(), y.max(), y.min()), cmap=djet)
    plt.imshow(grid, extent=(x.min(), x.max(), y.max(), y.min()))
    plt.hold(True)
    plt.scatter(x,y,c=z)
    plt.colorbar()



if __name__ == '__main__':
    main2()
    main()
