#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Este módulo contiene la definición del estados Larva

@autors Maximiliano Báez, Roberto Bañuelos
@contact mxbg.py@gmail.com, robertobanuelos@gmail.com
"""
from aaegypti import *

class Larva(AeAegypti) :
    """
    Esta clase contiene la representación del AeAegypti en su etapa de
    larva.

    Los porcentajes (y rango) del tiempo total de desarrollo, en todo el
    rango de temperaturas, que pasó en cada etapa inmadura son :
    1er estadio : 19% (13,9 a 23,1)
    2do estadio : 14% (11,3 a 21,3)
    3er estadio : 17% (13,0 a 27,0)
    4to estadio : 27% (24,2 a 28,5)
    Fuente : Temperature-Dependent Development and Survival Rates of
    Culex quinquefasciatus tus and Aedes aegypti (Diptera: Culicidae
    """

    def __init__(self, **kargs) :
        """
        @param kargs: Parametros de inicialización de la clase

        @keyword [sexo]: El el sexo del huevo a partir del cual eclosionó la larva.
        @keyword [position]: El punto que determina la ubiación de la larva
        """

        if not kargs.has_key('sexo') :
            # Se genera de forma aleatoria el sexo del mosquito
            sexo = randint(0, 1)
            if sexo == 0 :
                kargs['sexo'] = Sexo.MACHO
            else :
                kargs['sexo'] = Sexo.HEMBRA
        kargs['estado'] = Estado.LARVA

        # se invoca al constructor de la clase padre.
        AeAegypti.__init__(self, **kargs);



    def esta_muerto (self):
        """
        La supervivencia de los mosquitos depende de la capacidad para alimentarse,
        reproducirse, protegerse y dispersarse.
            Estado  Tiempo promedio
            larva   4 a 14 dias
        """
        return self.expectativa_vida <= 0

    @deprecated
    def madurar (self, hora) :
        #~ Se inicializan las variables
        delta_vida = 0
        delta_madurez = 0
        #~ Se realizan los controles para aumentar y/o disminuir la
        #~ expectativa de vida y la madurez de la larva de acuerdo con
        #~ la temperatura del medio.
        if hora.temperatura >= 34 :
            """
            La temperatura más alta que permite el desarrollo es 36oC,
            con una menor duración del estado larval.

            En condiciones óptimas el período larval puede durar 5 días,
            Lo que significa que maduraría en razon a
            delta_madurez = 100/(5*24)
            """
            delta_madurez = 100.0/(5.0*24.0)

        elif hora.temperatura >= 20 and hora.temperatura <= 34 :
            """
            Las temperaturas más cálidas ayudan a la rápida maduración
            de las larvas.

            En condiciones calidas el período larvar pude durar 5 y 8 días,
            de forma aleatoria se calcula la duración del periodo larvario
            para calcular el delta de la maduración
            """
            duracion_periodo = randint(5, 8) * 24.0
            delta_madurez = 100.0/ duracion_periodo

        elif hora.temperatura <= 11 :
            """
            El desarrollo cero se sitúa en 13,3oC, con un umbral inferior
            de desarrollo ubicado entre 9 y 10oC

            Christophers (1960) señala que la actividad del insecto disminuye
            abruptamente por debajo de 15oC hasta inhibición bajo medias
            diarias de 12oC.

            Para evitar su desarrollo se disminuye la expectativa de vida
            del individuo considerablemente como para que muera en un
            lapso de 72 hs(Arbitrariamente).
            delta = 100/72
            """
            delta_vida = 100.0/72.0
            #~ delta_madurez = 100/(14*24)
            delta_madurez = 100.0/(14.0*24.0)

        elif hora.temperatura <= 15 :
            """
            El desarrollo larval a 14 C es irregular y la mortalidad
            relativamente alta. Por debajo de esa temperatura, las larvas
            eclosionadas no alcanzan el estado adulto.

            Para evitar su desarrollo se disminuye la expectativa de vida
            del individuo considerablemente como para que muera en un
            lapso de 96 hs(Arbitrariamente).
            delta = 100/96
            """
            delta_vida = 100.0/92.0
            #~ se aumenta la madurez del individuo.
            delta_madurez = 100.0/(14.0*24.0)

        else :
            """
            De forma aleatoria se calcula la duración del periodo larvario
            para calcular el delta de la maduración
            """
            duracion_periodo = randint(5, 14) * 24.0
            delta_madurez = 100.0/ duracion_periodo
            delta_vida = 0.1389

        #~ Se disminuye la expectativa de vida en un delta
        self._expectativa_vida -= delta_vida
        #~ se incrementa la madurez del mosquito en un delta
        self._madurez += delta_madurez

    def desarrollar(self, hora) :
        """
        Este método se encarga de desarrollar el individuo que se encuentra
        en el estado de larva

        En condiciones óptimas el período larval puede durar 5 días pero
        comúnmente se extiende de 7 a 14 días.

        @type hora : Hora
        @param hora: el objeto que contiene los datos climatologicos para
            una hora.
        """
        cantidad_dias = self.get_madurez_zona(hora)
        tiempo_vida = self.get_expectativa_zona(hora)
        self._tiempo_vida = tiempo_vida
        self._tiempo_madurez = cantidad_dias
        if cantidad_dias > 0  :
            #~ se hace madurar a pupa
            self._madurez += 100/(cantidad_dias * 24.0)

        if tiempo_vida > 0 :
            #~ se disminuye la expectativa de vida de la pupa
            self._expectativa_vida -= 100/(tiempo_vida * 24.0)

        #~ se envejece la pupa
        self._edad += 1

        return self
