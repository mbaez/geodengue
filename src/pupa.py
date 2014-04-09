#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Este módulo contiene la definición del estado Pupa del Aedes Aegypti

@autors Maximiliano Báez, Roberto Bañuelos
@contact mxbg.py@gmail.com, robertobanuelos@gmail.com
"""

from aaegypti import *

class Pupa(AeAegypti) :
    """
    Esta clase contiene la representación del AeAegypti en su etapa de
    pupa. La etapa de pupa es una etapa de no alimentación, se mueven,
    respondiendo a cambios en la luz y al movimiento. Durante esta etapa,
    el mosquito se transforma en adulto. En mosquitos Culex esto toma 2
    días en el verano. Las pupas de mosquito viven en el agua de 1 a 4
    días, según la especie y la temperatura.

    La metamorfosis del mosquito en adulto se completa dentro de la cavidad
    de la pupa. Cuando el desarrollo está terminado, la piel de la pupa se
    rompe y el mosquito adulto emerge

    @see http://medicina.tij.uabc.mx/von/ciclo.html
    @see http://www.todosobremosquitos.com.ar/index.php?id=48&titulo=pupas-de-mosquitos
    """
    def __init__(self, **kargs) :
        """
        @param kargs: Parametros de inicialización de la clase

        @keyword [sexo]: El sexo de la larva a partir del cual evoluciono a pupa.
        @keyword [position]: El punto que determina la ubiación de la pupa
        """
        # se invoca al constructor de la clase padre.
        kargs['estado'] = Estado.PUPA
        AeAegypti.__init__(self, **kargs);


    def esta_muerto (self):
        """
        El estadio de pupa dura aproximadamente dos o tres días, emergiendo
        alrededor del 88% de los adultos en cuestión de 48 horas (Méndez et al., 1996)
        @see Dengeue en Mexico
        """
        return self.expectativa_vida <= 0

    def desarrollar(self, hora) :
        """
        El estadio de pupa dura aproximadamente dos o tres días, emergiendo
        alrededor del 88% de los adultos en cuestión de 48 horas (Méndez et al., 1996)

        Entre los 27-32oC la pupa que da lugar al Adulto macho emerge en
        1,9 días y la pupa que originará una hembra muda en 2,5 días.

        La duración promedio de la pupa, expresada como porcentaje del
        tiempo ocupado por la larva hasta que llega a adulto es de 20,6
        (Baz-Zeed, 1958)

        [26,83 (10-47)] * 0.206 días a 20oC
        [17,59 (9-29)]  * 0.206 días a 25oC
        [9,75 (5-16) ] * 0.206  días a 30oC

        @see Dengeue en Mexico
        @see El Aedes aegypti y la transmision del dengue
        @see The effect of temperature on the growth rate and survival
             of the immature stages of Aedes aegypti
        """
        cantidad_dias = self.get_madurez_zona(hora)
        self._tiempo_madurez = cantidad_dias

        if cantidad_dias > 0  :
            #~ se hace madurar a pupa
            self._madurez += 100/(cantidad_dias)

        #~ se envejece la pupa
        self._edad += 1

        return self

    def mortalidad (self, temperatura) :
        """
        En el caso de la pupa otero2006, la mortalidad intrínseca de una
        pupa se ha considerado como una ecuación dependiente de temperatura.
        Además de la mortalidad diaria en la fase de pupa, existe una importante
        mortalidad adicional, solo el 83% otero2006 de las pupas alcanzan
        la maduración y emergerán como mosquitos adultos, por lo tanto,
        el factor de supervivencia es de 0.83.
        """
        k = temperatura + 273.15
        return (0.01 + 0.9725 * math.exp( -(k - 278)/2.7035)) * 0.83
