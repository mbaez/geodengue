#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Este módulo contiene la definición del estado Huevo del Aedes Aegypty

@autors Maximiliano Báez, Roberto Bañuelos
@contact mxbg.py@gmail.com, robertobanuelos@gmail.com
"""

from aaegypti import *

class Huevo(AeAegypti) :
    """
    Esta clase contiene la representación del AeAegypti en su etapa de
    huevo.
    """
    def __init__(self, **kargs) :
        """
        @param kargs: Parametros de inicialización de la clase

        @keyword [sexo]: El enum que identifica el sexo del Huevo
        @keyword [position]: El punto que determina la ubiación del huevo
        """
        # Se genera de forma aleatoria el sexo del huevo
        sexo = randint(0, 1)
        if sexo == 0 :
            sexo = Sexo.MACHO
        else :
            sexo = Sexo.HEMBRA
        kargs['sexo'] = sexo
        kargs['estado'] = Estado.HUEVO
        # se invoca al constructor de la clase padre.
        AeAegypti.__init__(self, **kargs);

    def esta_muerto (self):
        """
        La supervivencia de los mosquitos depende de la capacidad para alimentarse,
        reproducirse, protegerse y dispersarse.
            Estado  Tiempo promedio
            huevo   2 a 5 dias
        """
        return self.espectativa_vida <= 0 or self.edad > 5*24

    def desarrollar(self, hora) :
        """
        Para el estudío se supone que los criaderos disponibles estan
        delimitados por los puntos de control(dispositivos de ovipostura)
        fijados. Para el caso de los huevos, estos son depositados
        individualmente en las paredes de los recipientes(dispositivo de
        ovipostura) por encima del nivel del agua.

        Para el desarrollo del huevo se supone que una vez que culmine el
        desarrollo embriológico los huevos eclosionarán.

        La lógica de que los huevos deben mojarse para eclosionar no está
        implementada, así como que los huevos desarrollados pueden
        sobrevivir por periodos largos para posteriormente eclosionar.

        @type hora : Hora
        @param hora: el objeto que contiene los datos climatologicos para
            una hora.
        """
        #~ Se inicializan las variables
        delta_vida = 0
        delta_madurez = 0
        #~ Se realizan los controles para aumentar y/o disminuir la
        #~ espectativa de vida y la madurez de la larva de acuerdo con
        #~ la temperatura del medio.
        if hora.temperatura >= 27 :
            """
            Se considera un clima cálido cuando la temperatura es superior
            de los 27 C.

            El desarrollo embriológico generalmente se completa en 48 horas
            si el ambiente es húmedo y cálido.
            """
            delta_madurez = 100/48.0
        elif hora.temperatura <= 15 :
            """
            El desarrollo embriológico puede prolongarse hasta 5 días a
            temperaturas bajas.
            """
            delta_madurez = 100/120.0
            #~ Arbitrariamente se disminuye la espectativa de vida del huevo
            delta_vida = 100/ 140.0
        else :
            """
            En temperaturas no optimas se calcula con regla de 3 el delta
            de maduración del huevo.
            """
            temp_med = randint(27,40)
            delta_madurez = (hora.temperatura * 48.0 )/(temp_med * 1.0)

        #~ Se disminuye la espectativa de vida en un delta
        self._espectativa_vida -= delta_vida
        #~ se incrementa la madurez del mosquito en un delta
        self._madurez += delta_madurez
        self._edad +=1
        return self;
