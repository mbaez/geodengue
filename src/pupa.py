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

    @deprecated
    def madurar (self, hora) :
        #~  se inicializa la varible
        delta_madurez = 0.0
        if hora.temperatura >= 27  and hora.temperatura <= 32:
            """
            Entre los 27-32oC la pupa se transforma a un adulto, escenario
            ideal :

            Macho 1.9 días : delta_madurez = 100 /(1.9 * 24)
            Hembra 2.5 días: delta_madurez = 100 /(2.5 * 24)

            TODO : ¿Que pasa cuando la temperatura supera los 32 C ?
            """
            #~ Si es hembra el proceso de madurez tarda más
            if self.sexo == Sexo.HEMBRA :
                delta_madurez = 100/(2.5 * 24.0)
            else :
                delta_madurez = 100/(1.9 * 24)

        elif hora.temperatura > 20  and hora.temperatura <= 25:
            """
            [17,59 (9-29)] * 0.206 días a 25oC
            Para determinar  la cantidad de días que toma a un macho y
            una hembra se partio del punto que para el desarrollo, en
            condiciones optimas se dearrolla un
            Macho 1.9 días
            Hembra 2.5 días

            Suponiendo que el estado por defecto es la hembra se calcula
            la relación:

            Macho = 2.5 / 1.9 Hembras = 1,315789474 Hembras

            """
            delta_madurez = 100.0 / (randint(9, 29) * 0.206 * 24.0)
            #~  si es macho madura más rápido
            if Sexo.MACHO == self.sexo :
                delta_madurez =  delta_madurez / 1.315789474

        elif hora.temperatura <= 20:
            """
            [26,83 (10-47)] * 0.206 días a 20oC

            Para determinar  la cantidad de días que toma a un macho y
            una hembra se partio del punto que para el desarrollo, en
            condiciones optimas se dearrolla un
            Macho 1.9 días
            Hembra 2.5 días

            Suponiendo que el estado por defecto es la hembra se calcula
            la relación:

            Macho = 2.5 / 1.9 Hembras = 1,315789474 Hembras

            """
            delta_madurez =100.0 / (randint(10,47) * 0.206 * 24.0)
            #~  si es macho madura más rápido
            if Sexo.MACHO == self.sexo :
                delta_madurez =  delta_madurez / 1.315789474


        """
        TODO Como afecta las condiciones climáticas al desarrollo de la
        pupa ?
        """
        self._expectativa_vida -= 0.1389
        self._madurez += delta_madurez

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
        cantidad_dias = self.get_expectativa_zona(hora)
        if (cantidad_dias > 0 ) :
            #~ se calcula el promedio de días que puede vivir la pupa
            if self.tiempo_vida > 0 :
                self._tiempo_vida = (self.tiempo_vida + cantidad_dias)/2
            else :
                self._tiempo_vida = cantidad_dias
            #~ se hace madurar a pa pupa
            self._madurez += 100/(cantidad_dias * 24.0)
        if self.tiempo_vida > 0 :
            #~ se disminuye la expectativa de vida de la pupa
            self._expectativa_vida -= 100/(self.tiempo_vida * 24.0)
        #~ se envejece la pupa
        self._edad +=1

        return self
