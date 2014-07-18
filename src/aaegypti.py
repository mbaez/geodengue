#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Este módulo contiene la definición del AeAegypti

@autors Maximiliano Báez, Roberto Bañuelos
@contact mxbg.py@gmail.com, robertobanuelos@gmail.com
"""
from random import randint, uniform
from datatype import *
from models import *
from config import *

from db_manager import *

COEF_SH_DE = CoefSarpeDemicheleModel()


class AeAegypti:

    """
    Clase base, contiene la definición los atributos básicos.
    """
    @property
    def expectativa_vida(self):
        """
        La expectativa de vida es un valor numérico(entre 0 y 100) que
        varía de acuerdo a las condiciones climáticas a las que es
        sometido el mosquito. Cuando la expectativa de vida es creo el
        mosquito muere.
        """
        return self._expectativa_vida

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
    def tiempo_madurez(self):
        """
        La cantidad de dias que puede vivir el individuo
        """
        return self._tiempo_madurez

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
    def madurez(self):
        """
        La madurez es un valor numérico(entre 0 y 100) que varía de acuerdo
        a las condiciones climáticas a las que es sometido el mosquito.
        Cuando la madurez es igual a 100 el mosquito ya se encuentra
        listo para un cambio de estado.
        """
        return self._madurez

    @property
    def posicion(self):
        """
        La posición esta definida por las coordenadas x e y, se encuentra
        representada por un punto.

        @see Point
        """
        return self._posicion

    @property
    def zonas(self):
        """
        Amacena la referencia a la tabla que almacena todas las zonas que
        ya fueron procesadas y rankeadas.

        @see RankingTable
        """
        return self._zonas

    @property
    def colonia(self):
        """
        Amacena la referencia a la colonia de la que proviene el individuo
        """
        return self._colonia

    @property
    def id_colonia(self):
        """
        Amacena la referencia a la colonia de la que proviene el individuo
        """
        return self._id_colonia

    @property
    def id_mosquito(self):
        """
        Campo para validar individualmente el proceso evolutivo de un
        mosquito
        """
        return self._id_mosquito

    @property
    def id_padre(self):
        """
        Campo para validar individualmente el proceso evolutivo de un
        mosquito
        """
        return self._id_padre

    def __init__(self, **kargs):
        """
        Inicializa la clase setenado la expectativa de vida y la edad a
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
        self._colonia = kargs.get('colonia', None)
        self._id_colonia = kargs.get('id_colonia', None)
        if kargs.has_key('posicion'):
            self._posicion = kargs.get('posicion', None)
        else:
            self._posicion = Point(kargs)
        self._posicion = self.posicion.clone()
        self._edad = 0
        self._madurez = kargs.get('madurez', 0)
        self._expectativa_vida = kargs.get('expectativa_vida', 100)
        self.delta_vuelo = 0
        self._tiempo_vida = 0
        self._tiempo_madurez = 0
        self._id_mosquito = kargs.get('id', 0)
        self._id_padre = kargs.get('id_padre', 0)

    def se_reproduce(self, hora):
        """
        @type hora : Hora
        @param hora: el objeto que contiene los datos climatologicos para
            una hora.
        """
        return False

    def esta_maduro(self):
        """
        @rtype Boolean
        @return True si la madurez es >= 100 False en caso contraio
        """
        return self.madurez >= 100

    def get_bs_ij(self):
        """
        Calcula el valor de bs teniendo en cuenta la densidad larvaria de la
        zona.
        """
        #~ se retorna el tipo de zona
        return self.zonas.get_ranking(self.posicion, TAMANHO_ZONA)

    def get_tipo_zona(self):
        pts = self.get_bs_ij()
        return self.zonas.get_tipo_zona(pts)

    def get_madurez_zona(self, hora):
        """
        Se encarga de mapear el puntaje asignado a la zona del mosquito
        a la cantidad de días estimado de vida. para ello se utiliza
        el modelo de sharpe&demichele.

        """
        coef = COEF_SH_DE.get_by(self.estado)
        cantidad_dias = 1 / self.sharpe_demichele(hora.temperatura, coef[0])
        return cantidad_dias

    def sharpe_demichele(self, temperatura, coef):
        """
        @type  temperatura: Integer
        @param temperatura: La temperatura en grados centigrados.

        @type  coef: Dicionario
        @param coef: Coeficientes para el modelo enzimatico
        """
        k = temperatura + 273.15
        return coef["rh025"] * ((k / 298.15) * math.exp(
            (coef["ha"] / 1.987) * (1 / 298.15 - 1 / k))
        )\
            / (1 + math.exp((coef["hh"] / 1.987) * (1 / coef["th"] - 1 / k)))

    def __str__(self):
        """
        Metodo que se encarga de traducir la clase a un string
        """
        return str(self.estado) + "(" + str(self.sexo) + ")" + \
            " \nid=" + str(self.id_mosquito) + \
            " \nexp_vida=" + str(self.expectativa_vida ) + \
            " \nedad=" + str(self.edad / 24.0) + \
            " \nubicacion=" + str(self.posicion) + \
            " \ntiempo_madurez=" + str(self.tiempo_madurez) + \
            " \nmadurez=" + str(self.madurez)
