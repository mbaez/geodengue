#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Este módulo contiene la definición del estado Huevo del Aedes Aegypty

@autors Maximiliano Báez
@contact mxbg.py@gmail.com
"""

from aaegypti import *


class Huevo(AeAegypti):

    """
    Esta clase contiene la representación del AeAegypti en su etapa de
    huevo.
    """

    def __init__(self, **kargs):
        """
        @param kargs: Parametros de inicialización de la clase

        @keyword [sexo]: El enum que identifica el sexo del Huevo
        @keyword [position]: El punto que determina la ubiación del huevo
        """
        # Se genera de forma aleatoria el sexo del huevo
        sexo = randint(0, 1)
        if sexo == 0:
            sexo = Sexo.MACHO
        else:
            sexo = Sexo.HEMBRA
        kargs['sexo'] = sexo
        kargs['estado'] = Estado.HUEVO
        # se invoca al constructor de la clase padre.
        AeAegypti.__init__(self, **kargs)

    def esta_muerto(self):
        """
        La supervivencia de los mosquitos depende de la capacidad para alimentarse,
        reproducirse, protegerse y dispersarse.
            Estado  Tiempo promedio
            huevo   2 a 5 dias
        """
        return self.expectativa_vida <= 0

    def desarrollar(self, hora):
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
        cantidad_dias = self.get_madurez_zona(hora)

        self._tiempo_madurez = cantidad_dias

        if cantidad_dias > 0:
            #~ se hace madurar a pupa
            delta_madurez = 100 / (cantidad_dias)

        #~ se envejece la pupa
        self._edad += 1
        #~ se incrementa la madurez del mosquito en un delta
        self._madurez += delta_madurez
        return self

    def inhibicion_eclosion(self, temperatura, colonia):
        """
        [otero2006]La posibilidad de un proceso de regulación compleja, en la
        que la alta densidad de larvas inhibe eclosión de los huevos, la
        inducción de los huevos para entrar en diapausa, fue desenterrado por
        Livdah. Hemos introducido este efecto a través de un factor de
        reducción de la tasa de eclosión cuando las larvas supera una densidad
        predeterminada.
        """
        H = colonia[Estado.HUEVO]["cantidad"]
        L = colonia[Estado.LARVA]["cantidad"]
        a_0 = 0.5
        bs_ij = self.get_bs_ij()
        omega = L / bs_ij
        if omega < a_0:
            omega = 0
        else:
            omega = 0.63

        coef = COEF_SH_DE.get_by(Estado.HUEVO)
        elr = self.sharpe_demichele(temperatura, coef[0])
        hi = H * elr * omega
        return hi

    def mortalidad(self, temperatura, colonia):
        """
        Para la etapa huevo, [otero2006] la define como una constante
        independiente de la temperatura.
        """

        return colonia[self.estado]["cantidad"] / 100.0
