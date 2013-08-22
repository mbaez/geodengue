#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Este módulo contiene la definición del proceso evolutivo de los puntos
de control.

@autors Maximiliano Báez, Roberto Bañuelos
@contact mxbg.py@gmail.com, robertobanuelos@gmail.com
"""

#Se impotan los modulos.

from individuo import *

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
            self.__init_poblacion__(kargs["poblacion"])
        #~ se inicializa el atributo periodo
        self.historial_clima =[]
        #~ se inicializa el atributo periodo
        self.periodo = kargs.get('periodo',[])

    def __init_poblacion__ (self, data ):
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

                indv = Individuo(x=grid.x[i], y=grid.y[i], \
                    id=grid.ids[i], estado=Estado.LARVA, index=i)

                self.poblacion.append(indv)

        self.__grid = grid


    def start(self):
        """
        Se encarga de iniciar el simulador.
        """
        i=0
        for hora in self.periodo.horas :
            #~ se procesa cada individuo de la población
            j=0
            nueva_poblacion = []
            for individuo in self.poblacion :
                #~ Se desarrolla el inidividuo
                individuo.desarrollar(hora)

                #~ Se verifica el estado del individuo
                if(individuo.esta_muerto() == True):
                    print "Esta muerto.. : " + str(hora.temperatura)
                    self.poblacion.remove(individuo)
                    pass

                elif(individuo.se_reproduce(hora) == True) :
                    print "se reproduce :" + str(hora.temperatura)
                    huevos = individuo.poner_huevos(hora)
                    if not huevos == None :
                        print "puso huevos :" + str(hora.temperatura)
                        nueva_poblacion.extend(huevos)
                #~ fin del preiodo
                j += 1
            #~ fin del preriodo
            self.poblacion.extend(nueva_poblacion)
            i+= 1
            print "New perido " + str(i) + "\n"

        self.stats()


    def to_grid (self):
        """
        Este método se encarga de traducir la población de inidviduos
        a un grid interpolable.

        Los adultos no son incluidos en el conteo de individuos.
        """
        key_map = {}
        data_array = []
        for individuo in self.poblacion :
            if not key_map.has_key(individuo.id_dispositivo) \
                and not individuo.mosquito.estado == Estado.ADULTO:
                # se obtiene los datos
                data = {}
                data['x'] = individuo.coordenada_x
                data['y'] = individuo.coordenada_y
                data['id'] = individuo.id_dispositivo
                data['index'] = individuo.index
                data['cantidad'] = 1
                #se añade el elemento al array
                data_array.append(data)
                # se añade el indice al array
                key_map[individuo.id_dispositivo] = len(data_array) -1
            elif not individuo.mosquito.estado == Estado.ADULTO:
                index = key_map[individuo.id_dispositivo]
                # se incrementa la cantidad de larvas
                data_array[index]['cantidad'] += 1
        #se ordenan los datos
        new_list = sorted(data_array, key=lambda k: k['index'])
        # se realiza el parse a grid
        grid = Grid();
        grid.parse(new_list)
        # se retorna la referencia al grid
        return grid;

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
            if individuo.mosquito.sexo == Sexo.MACHO :
                stats_dic['macho'] += 1
            else :
                stats_dic['hembra'] += 1

            if individuo.mosquito.estado == Estado.HUEVO :
                stats_dic['huevo'] += 1
            elif individuo.mosquito.estado == Estado.LARVA :
                stats_dic['larva'] += 1
            elif individuo.mosquito.estado == Estado.PUPA :
                stats_dic['pupa'] += 1
            else :
                stats_dic['adulto'] += 1

        for k in stats_dic.keys() :
            print( 'nro de ' + str(k) + ' = ' + str(stats_dic[k]))

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
