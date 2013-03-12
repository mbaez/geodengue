#se importan los libs correspondientes
import matplotlib.pyplot as plt
import csv
#Se impotan los modulos.
from base_model import *
from interpolation import *

def main():
    n = 100
    nx, ny = 50, 50
    #x, y, z = map(np.random.random, [n, n, n])
    x, y, z = import_csv('data/larvitrampas.csv')
    muestras = Grid(x, y, z);
    #genera los n puntos
    grid = muestras.gen_grid(nx, ny);
    alg = Idw()
    # Calculate IDW
    #interpolated_grid = alg.simple_idw(muestras.x,muestras.y,muestras.z,grid.x, grid.y)
    interpolated_grid = alg.scipy_idw(muestras.x,muestras.y,muestras.z,grid.x, grid.y)
    #interpolated_grid = alg.linear_rbf(muestras.x,muestras.y,muestras.z,grid.x, grid.y)
    interpolated_grid = interpolated_grid.reshape((ny, nx))

    plot(muestras.x,muestras.y,muestras.z,interpolated_grid)
    plt.title('IDW')
    plt.show()

def import_csv (filename):
    import csv
    import numpy as np
    x,y,z =[],[],[];
    with open(filename, 'rb') as f:
        mycsv = csv.reader(f,delimiter=',')
        for row in mycsv:
            z.append(float(row[1]))
            x.append(float(row[2]))
            y.append(float(row[3]))

    return np.array(x, dtype=np.float),\
            np.array(y,dtype=np.float),\
            np.array(z,dtype=np.float)

def plot(x,y,z,grid):
    plt.figure()
    plt.imshow(grid, extent=(x.min(), x.max(), y.max(), y.min()))
    plt.hold(True)
    plt.scatter(x,y,c=z)
    plt.colorbar()


if __name__ == '__main__':
    main()
