#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Este módulo contiene la definición del AeAegypti

@autors Maximiliano Báez, Roberto Bañuelos
@contact mxbg.py@gmail.com, robertobanuelos@gmail.com
"""

from random import randint
from datatype import *

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

    def __init__(self, **kargs) :
        """
        Inicializa la clase setenado la espectativa de vida y la edad a
        cero.

        @param kargs: Parametros de inicialización de la clase

        @keyword [sexo]: El enum que identifica el sexo del AeAegypti
        @keyword [estado]: El enum que identifica el estado del AeAegypti
        @keyword [x]: la coordenada x
        @keyword [y]: La coordenada y
        @keyword [posicion]: El punto que determina la ubiación del AeAegypti
        """
        self._sexo = kargs.get('sexo', None)
        self._estado = kargs.get('estado', None)
        if kargs.has_key('posicion') :
            self._posicion = kargs.get('posicion', None)
        else :
            self._posicion = Point(kargs)
        self._edad = 0;
        self._madurez = 0;
        self._espectativa_vida = 100;
        self.delta_vuelo = 0;

    def se_reproduce (self, hora) :
        """
        @type hora : Hora
        @param hora: el objeto que contiene los datos climatologicos para
            una hora.
        """
        return False;

    def __str__(self):
        """
        Metodo que se encarga de traducir la clase a un string
        """
        return str(self.estado) + "(" + str(self.sexo) + ")" + \
            "vida=" + str(self.espectativa_vida) + \
            " edad=" + str(self.edad) + "  madurez=" + str(self.madurez)
