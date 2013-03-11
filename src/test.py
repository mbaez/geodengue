#se importan los libs correspondientes
import matplotlib.pyplot as plt
#Se impotan los modulos.
from base_model import *
from interpolation import *

def main():
    n = 100
    nx, ny = 500, 500
    x, y, z = map(np.random.random, [n, n, n])
    muestras = Grid(x, y, z);
    #genera los n puntos
    grid = muestras.gen_grid(nx, ny);
    alg = Idw()
    # Calculate IDW
    interpolated_grid = alg.linear_rbf(muestras.x,muestras.y,muestras.z,grid.x, grid.y)
    interpolated_grid = interpolated_grid.reshape((ny, nx))

    plot(muestras.x,muestras.y,muestras.z,interpolated_grid)
    plt.title('IDW')
    plt.show()


def plot(x,y,z,grid):
    plt.figure()
    plt.imshow(grid, extent=(x.min(), x.max(), y.max(), y.min()))
    plt.hold(True)
    plt.scatter(x,y,c=z)
    plt.colorbar()


if __name__ == '__main__':
    main()
