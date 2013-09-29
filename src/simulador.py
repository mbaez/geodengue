#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Este módulo contiene la definición del proceso evolutivo de los puntos
de control.

@autors Maximiliano Báez, Roberto Bañuelos
@contact mxbg.py@gmail.com, robertobanuelos@gmail.com
"""

#Se impotan los modulos.

from huevo import *
from larva import *
from pupa import *
from adulto import *

class Simulador :
    """
    El proceso de evolución de las muestras consiste en un proceso, en el
    cual las muestras obtenidas mediante los dispositivos de ovipostura son
    expuestas a un conjunto de variaciones en un periodo de tiempo. Las
    variaciones que, principalmente, afectan a las muestras son :

    * Las variaciones del clima en dicho periodo : Se someten las muestras
        obtenidas a las distintas variaciones climáticas ocurridas en el
        periodo de tiempo seleccionado para el estudio.

    * La naturaleza del mosquito : Cada elemento de la muestra, es sometido
        a cambios considerando la naturaleza del mosquito. Los aspectos que
        se tienen en cuenta son su ciclo de vida del mosquito, ciclo
        reproductivo y el desplazamiento.

    """

    def __init__ (self, **kargs) :
        """
        Constructor de la clase
        @param kargs: Parametros de inicialización de la clase

        @keyword poblacion: La población inicial.
        @keyword periodo: El periodo de simulación.
        """
        #~ se inicializa el atributo periodo
        self.poblacion =  [];
        if kargs.has_key("poblacion") == True:
            self.generar_poblacion(kargs["poblacion"])
        #~ se inicializa el atributo periodo
        self.historial_clima =[]
        #~ se inicializa el atributo periodo
        self.periodo = kargs.get('periodo',[])

    def generar_poblacion (self, data ):
        """
        Este método se encarga de procesar los datos de las muestras y
        generar los inidividuos para inicializar la población.

        """
        grid = Grid();
        grid.parse(data);
        for i in range(len(grid)):
            # se obtine la cantidad de individuos
            cantidad_larvas = int(grid.z[i]);
            for cantidad in range(cantidad_larvas) :
                #se inicializa los inidviduos

                indv = Larva(x=grid.x[i], y=grid.y[i], \
                    id=grid.ids[i], estado=Estado.LARVA, index=i)

                self.poblacion.append(indv)

        self.__grid = grid

    def cambiar_estado (self, individuo) :
        """
        """
        if individuo.estado == Estado.HUEVO :
            return Larva(sexo=individuo.sexo, posicion=individuo.posicion)

        elif individuo.estado == Estado.LARVA :
            return Pupa(sexo=individuo.sexo, posicion=individuo.posicion)

        elif individuo.estado == Estado.PUPA :
            return Adulto(sexo=individuo.sexo, posicion=individuo.posicion)
        else :
            return individuo

    def start(self):
        """
        Se encarga de iniciar el simulador.
        """

        init_dic = self.stats()
        i=0
        for hora in self.periodo.horas :
            #~ se procesa cada individuo de la población
            j=0
            nueva_poblacion = []
            time = 0
            for individuo in self.poblacion :
                #~ Se desarrolla el inidividuo
                individuo.desarrollar(hora)
                #~ Se verifica el estado del individuo
                if(individuo.esta_muerto() == True) :
                    """
                    si el individuo esta muerto se lo remueve de la poblacion
                    """
                    self.poblacion.remove(individuo)

                elif individuo.esta_maduro() :
                    """
                    si el individuo esta maduro, se realiza el cambio de
                    estado.
                    """
                    individuo = self.cambiar_estado(individuo);

                elif individuo.estado == Estado.ADULTO :
                    if(individuo.se_reproduce(hora) == True) :
                        huevos = individuo.poner_huevos(hora)
                        if not huevos == None :
                            nueva_poblacion.extend(huevos)
                #~ fin del preiodo
                j += 1
            #~ fin del preriodo
            self.poblacion.extend(nueva_poblacion)
            i+= 1


        print 'Poblacion inicial'
        for k in init_dic.keys() :
            print( 'nro de ' + str(k) + ' = ' + str(init_dic[k]))

        print 'Poblacion final'
        out_dic = self.stats()
        for k in out_dic.keys() :
            print( 'nro de ' + str(k) + ' = ' + str(out_dic[k]))

    def to_grid (self):
        """
        Este método se encarga de traducir la población de inidviduos
        a un grid interpolable.

        Los adultos no son incluidos en el conteo de individuos.
        """
        key_map = {}
        data_array = []
        max_cantidad = 0
        for individuo in self.poblacion :
            point = individuo.posicion
            key = str(point.x) + "-" + str(point.y)
            if not key_map.has_key(key) \
                and not individuo.estado == Estado.HUEVO :
                # se obtiene los datos
                data = {}
                data['x'] = point.x
                data['y'] = point.y
                data['id'] = 0
                #~ data['index'] = individuo.index
                data['cantidad'] = 1
                #se añade el elemento al array
                data_array.append(data)
                # se añade el indice al array
                key_map[key] = len(data_array) -1
            elif not individuo.estado == Estado.HUEVO :
                index = key_map[key]
                # se incrementa la cantidad de larvas
                data_array[index]['cantidad'] += 1
                if data_array[index]['cantidad'] >  max_cantidad :
                    max_cantidad = data_array[index]['cantidad']

        #ajustar las escala de valores para tener cantidades en el rango
        #de 0 a 80
        for data in data_array :
            data['cantidad'] = \
                float(data['cantidad'])*float(80.0/max_cantidad)

        print 'cantidad de puntos a interpolar: ' + str(len(data_array))

        #orden por coordenada
        print "sort por coordenada..."
        swapped = True
        while swapped :
            swapped = False
            for i in range(1, len(data_array)) :
                comp1 = (data_array[i-1]['x'], data_array[i-1]['y'])
                comp2 = (data_array[i]['x'], data_array[i]['y'])
                if self.compare_coordinates(comp1, comp2) > 0 :
                    aux = data_array[i-1]
                    data_array[i-1] = data_array[i]
                    data_array[i] = aux
                    swapped = True

        # se realiza el parse a grid
        grid = Grid();
        grid.parse(data_array)

        # se retorna la referencia al grid
        return grid;

    """
    Metodo para comparar 2 puntos
    @param p1, p2
    array puntos
        ej> p1 = (x1, y1)
    """
    def compare_coordinates( self, p1, p2 ) :
        if float(p1[0]) == float(p2[0]) :
            return float(p1[1]) - float(p2[1])
        else :
            return float(p1[0]) - float(p2[0])

    def stats( self ) :
        """
        Metodo para analizar el comportamiento global de la pobacion
        Tomando en cuenta la poblacion inicial se analiza durante un periodo
        de tiempo
            cantidad de hembras y machos
            cantidad de individuos en el estado huevo
            cantidad de individuos en el estado larva
            cantidad de individuos en el estado pupa
            cantidad de individuos en el estado adulto
        """
        #~ inicializamos el diccionario con los valores que contabilizaremos
        stats_dic = {}
        stats_dic['macho'] = 0
        stats_dic['hembra'] = 0
        stats_dic['huevo'] = 0
        stats_dic['larva'] = 0
        stats_dic['pupa'] = 0
        stats_dic['adulto'] = 0

        for individuo in self.poblacion :
            if individuo.sexo == Sexo.MACHO :
                stats_dic['macho'] += 1
            else :
                stats_dic['hembra'] += 1

            if individuo.estado == Estado.HUEVO :
                stats_dic['huevo'] += 1
            elif individuo.estado == Estado.LARVA :
                stats_dic['larva'] += 1
            elif individuo.estado == Estado.PUPA :
                stats_dic['pupa'] += 1
            else :
                stats_dic['adulto'] += 1

        return stats_dic

if __name__ == "__main__" :
    from db_manager import *
    from models import *
    from tutiempo import *

    id_muestras = 1;
    #se obtiene el historial climatico
    print "obteniendo los datos climaticos"
    clima = TuTiempo("Asuncion")
    periodo = clima.get_periodo()

    print "obteniendo los datos de la bd"
    dao = PuntosControlModel()
    data = dao.get_by(id_muestras);
    print "construyendo la grilla"
    #~ print data

    evol = Simulador(periodo=periodo, poblacion=data)

    print "iniciando simulación"
    evol.start()
    """
    for ind in evol.poblacion :
        print str(ind)
    """
    evol.to_grid()
