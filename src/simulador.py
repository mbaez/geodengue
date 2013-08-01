#! /usr/bin/env python
# -*- coding: utf-8 -*-


__author__ = "Maximiliano Báez"
__mail__ = "mxbg.py@gmail.com"

#Se impotan los modulos.

from db_manager import *
from models import *
from tutiempo import *

"""
Enum que representa los estados por lo cuales atravieza el individuo.
"""
Estado = Enum(["HUEVO", "LARVA","PUPA","ADULTO"])

"""
Sexo válidos del individuo
"""
Sexo = Enum(["MACHO", "HEMBRA"])

"""
Representación de un individuo de la población.
"""
class Individuo :
    """
    Esta clase contiene la representación de un individuo de la población.
    Un mosquito de la población tiene los siguientes atributos :
    * Sexo : Macho o hembra
    * Edad : cantidad de días que lleva vivo el mosquito.
    * Estado : Huevo, Larva, Pupa, Adulto..
    * Ubicación : coordenadas longitud y latitud
    * Dispositivo de origen : el código del dispositivo de ovipostura de origen.
    * Expectativa de vida : es un valor numérico que varía de acuerdo a las
        condiciones climáticas a las que es sometido el mosquito.
    * Periodo es el intervalo de tiempo al que será sometido la población inicial a evolución.
    """
    def __init__ (self) :
        self.sexo = Sexo.HEMBRA
        self.edad = 0
        self.estado = Estado.HUEVO
        self.espectativa_vida = 100
        self.coordenadas = None
        self.dispositivo_origen = None

    def esta_muerto (self):
        """
        esta_muerto : si espectativa de vida <= 0, si edad >= 30 dias.
        """
        return self.espectativa_vida <= 0 or self.edad >= 30

    def se_reproduce (self, dia):
        """
        El mosquito se reproduce si :
        * No está muerto = no
        * Sexo = hembra, temperatura > 18 C
        """
        return self.esta_muerto() == False \
            and self.sexo == Sexo.HEMBRA \
            and self.estado == Estado.ADULTO

    def buscar_alimento(self):
        """
        Se tiene en cuenta la ubicacion del mosquito adulto y la densidad
        poblacional en dicha ubicación.
        """
        pass

    def desarrollar(self, dia) :
        """
        """
        self.espectativa_vida -= 10;
        self.edad += 1;


    def poner_huevos(self, dia) :
        """
        """
        return []

    def __str__(self):
        return str(self.espectativa_vida) + " - " + str(self.edad )


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
            self.poblacion = kargs["poblacion"]
        #~ se inicializa el atributo periodo
        self.historial_clima =[]
        #~ se inicializa el atributo periodo
        self.periodo = []
        if kargs.has_key("periodo") == True:
            self.periodo = kargs["periodo"]


    def start(self):
        """
        Se encarga de iniciar el simulador.
        """
        i=0
        for dia in self.periodo.horas :
            #~ se procesa cada individuo de la población
            j=0
            for individuo in self.poblacion :
                #~ Se desarrolla el inidividuo
                individuo.desarrollar(dia)

                #~ Se verifica el estado del individuo
                if(individuo.esta_muerto() == True):
                    print "Esta muerto.. Individiuos restantes :" +\
                        str(len(self.poblacion))
                    self.poblacion.remove(individuo)

                elif(individuo.se_reproduce(dia) == True) :
                    huevos = individuo.poner_huevos(dia)
                    self.poblacion.append(huevos)
                #~ fin del preiodo
                j += 1
            #~ fin del preiodo
            i += 1
            print "dia " + str(i)


if __name__ == "__main__" :
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
    muestras = Grid();
    muestras.parse(data);

    evol = Simulador(periodo=periodo)
    for i in range(len(muestras)):
        evol.poblacion.append(Individuo())
    print "iniciando simulación"
    evol.start()
    for ind in evol.poblacion :
        print str(ind)

