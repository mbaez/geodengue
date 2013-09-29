#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Este módulo contiene la definición del AeAegypti

@autors Maximiliano Báez, Roberto Bañuelos
@contact mxbg.py@gmail.com, robertobanuelos@gmail.com
"""

from random import randint
from datatype import *
from models import *
from config import *

class AeAegypti :
    """
    Clase base, contiene la definición los atributos básicos.
    """
    @property
    def espectativa_vida(self):
        """
        La expectativa de vida es un valor numérico(entre 0 y 100) que
        varía de acuerdo a las condiciones climáticas a las que es
        sometido el mosquito. Cuando la espectativa de vida es creo el
        mosquito muere.
        """
        return self._espectativa_vida

    @property
    def edad(self):
        """
        La edad es la cantidad de horas que lleva el individuo lleva vivo.
        """
        return self._edad

    @property
    def tiempo_vida(self):
        """
        La cantidad de dias que puede vivir el individuo
        """
        return self._tiempo_vida

    @property
    def sexo(self):
        """
        El sexo puede ser Macho o hembra, valor generado aleatoriamente.
        """
        return self._sexo

    @property
    def estado(self):
        """
        Indica el estado actual de la clase.
        """
        return self._estado

    @property
    def madurez (self):
        """
        La madurez es un valor numérico(entre 0 y 100) que varía de acuerdo
        a las condiciones climáticas a las que es sometido el mosquito.
        Cuando la madurez es igual a 100 el mosquito ya se encuentra
        listo para un cambio de estado.
        """
        return self._madurez

    @property
    def posicion (self):
        """
        La posición esta definida por las coordenadas x e y, se encuentra
        representada por un punto.

        @see Point
        """
        return self._posicion

    @property
    def zonas (self):
        """
        Amacena la referencia a la tabla que almacena todas las zonas que
        ya fueron procesadas y rankeadas.

        @see RankingTable
        """
        return self._zonas

    def __init__(self, **kargs) :
        """
        Inicializa la clase setenado la espectativa de vida y la edad a
        cero.

        @param kargs: Parametros de inicialización de la clase

        @keyword [sexo]: El enum que identifica el sexo del AeAegypti
        @keyword [estado]: El enum que identifica el estado del AeAegypti
        @keyword [zonas]: La referencia al ranking table de las zonas
        @keyword [x]: la coordenada x
        @keyword [y]: La coordenada y
        @keyword [posicion]: El punto que determina la ubiación del AeAegypti
        """
        self._sexo = kargs.get('sexo', None)
        self._estado = kargs.get('estado', None)
        self._zonas = kargs.get('zonas', None)
        if kargs.has_key('posicion') :
            self._posicion = kargs.get('posicion', None)
        else :
            self._posicion = Point(kargs)
        self._edad = 0;
        self._madurez = 0;
        self._espectativa_vida = 100;
        self.delta_vuelo = 0;
        self._tiempo_vida = 0

    def se_reproduce (self, hora) :
        """
        @type hora : Hora
        @param hora: el objeto que contiene los datos climatologicos para
            una hora.
        """
        return False;

    def esta_maduro (self) :
        """
        @rtype Boolean
        @return True si la madurez es >= 100 False en caso contraio
        """
        return self.madurez >= 100

    def rank_zona (self) :
        """
        Calcula el tipo de zona en la que se encuentra el mosquito
        """
        #~ se calcula el puntaje de la zona
        pts = self.zonas.get_ranking(self.posicion, TAMANHO_ZONA)
        #~ se retorna el tipo de zona
        return self.zonas.get_tipo_zona(pts);


    def get_espectativa_zona (self, hora) :
        """
        Se encarga de mapear el puntaje asignado a la zona del mosquito
        a la cantidad de días estimado de vida.

        Para LARVAS (P=0.8) Y PUPAS(P=0.2)

        60 < Pts  Optima  0   [10, 17.4] * P    [9, 13]* P    [5, 7.2] * P  0
        60 > Pts  Buena   0   [17.4, 24.8] * P  [13, 17]* P   [7.2, 9.4] * P    0
        30 > Pts  Normal  0   [24.8, 32.2] * P  [17, 21]* P   [9.4, 11.6] * P   0
        20 > Pts  Mala    0   [32.2, 39.6] * P  [21, 25]* P   [11.6, 13.8] * P  0
        8 > Pts   Pésima  0   [39.6, 47] * P    [25, 29]* P   [13.8, 16] * P    0
        """
        tipo_zona = str(self.rank_zona())
        tipo_clima = str(hora.get_tipo_clima())

        if(self.estado == Estado.HUEVO) :
            return

        elif(self.estado == Estado.LARVA) :
            return self.__get_dias__(LARVA_PUPA_ZONE, tipo_zona, tipo_clima, 0.8)

        elif(self.estado == Estado.PUPA) :
            return self.__get_dias__(LARVA_PUPA_ZONE ,tipo_zona, tipo_clima, 0.2)

        else :
            return


    def __get_dias__(self, table,tipo_zona, tipo_clima, p) :
        """
        Obtiene el valor que corersponde a la zona y el tipo de clima

        @type table : Diccionario
        @param table: La tabla que continene los datos

        @type tipo_zona : String
        @param tipo_zona: El string que caracteriza a la zona

        @type tipo_clima : String
        @param tipo_clima: El string que caracteriza al clima

        @type p : Float
        @param p: El porcentaje de duración del periodo
        """
        dias = table[tipo_zona][tipo_clima]
        if(len(dias) > 1) :
            #~ se obitnene los extremos, se multiplica por 100 para realizar
            #~ un ranint entre los extremos ya que no existe un 'randfloat'
            start = int(dias[0] * 100)
            end = int(dias[1] * 100)
            #~ se calcula un número aleatorio en entre los extremos
            cantidad_dias = randint(start, end)
            #~ print "cantidad dias " +str(cantidad_dias)
            return  (cantidad_dias * p) /100.0
        #~ si tiene un solo elemento se retorna el elemento multiplicado
        #~  por el porcentaje
        return dias[0] * p;

    def __str__(self):
        """
        Metodo que se encarga de traducir la clase a un string
        """
        return str(self.estado) + "(" + str(self.sexo) + ")" + \
            " vida=" + str(self.espectativa_vida) + \
            " edad=" + str(self.edad / 24) + \
            " tiempo_vida=" + str(self.tiempo_vida)+ \
            " madurez=" + str(self.madurez)
