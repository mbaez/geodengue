#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Este módulo contiene la definición del estados Larva

@autors Maximiliano Báez, Roberto Bañuelos
@contact mxbg.py@gmail.com, robertobanuelos@gmail.com
"""
from aaegypti import *


class Larva(AeAegypti):

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

    def __init__(self, **kargs):
        """
        @param kargs: Parametros de inicialización de la clase

        @keyword [sexo]: El el sexo del huevo a partir del cual eclosionó la larva.
        @keyword [position]: El punto que determina la ubiación de la larva
        """

        if not kargs.has_key('sexo'):
            # Se genera de forma aleatoria el sexo del mosquito
            sexo = randint(0, 1)
            if sexo == 0:
                kargs['sexo'] = Sexo.MACHO
            else:
                kargs['sexo'] = Sexo.HEMBRA
        kargs['estado'] = Estado.LARVA

        # se invoca al constructor de la clase padre.
        AeAegypti.__init__(self, **kargs)

    def esta_muerto(self):
        """
        La supervivencia de los mosquitos depende de la capacidad para alimentarse,
        reproducirse, protegerse y dispersarse.
            Estado  Tiempo promedio
            larva   4 a 14 dias
        """
        return self.expectativa_vida <= 0

    def desarrollar(self, hora):
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
        self._tiempo_madurez = cantidad_dias
        if cantidad_dias > 0:
            #~ se hace madurar a pupa
            self._madurez += 100 / (cantidad_dias)

        #~ se envejece la larva
        self._edad += 1

        return self

    def mortalidad(self, temperatura, colonia):
        """
        En el caso de las larvas otero2006 define que se
        encuentra influenciada dos métodos. La primera define como una
        ecuación dependiente de temperatura. La segunda depende de la
        densidad poblacional del habitad de la larva.
        pag 1964

        """
        k = temperatura + 273.15
        ml = 0.01 + 0.9725 * math.exp(-(k - 278) / 2.7035)

        L = colonia[self.estado]["cantidad"]
        """
        Marcelo Otero:
        El termino L-1 corresponde a la competencia intraespecífica en el
        estadío larval. Si tengo L larvas, entonces una larva cualquiera
        interactua no con las L larvas sino con L-1 larvas ya que no
        interactua consigo misma. Por eso el término de interacción no lineal
        es L*(L-1). Esto se debe también debido a que las poblaciones son
        discretas, es decir la población de larvas solo puede tomar valores en
        los naturales incluyendo el 0. Entonces si la población de larvas es
        una sola larva, el término no lineal es L*(L-1) = 1*(1-1) = 0.
        Conclusión, si hay una sola larva, no hay competencia intraespecífica.
        """
        bs_ij = self.get_bs_ij()
        m = ml * L + (ALPHA / bs_ij) * L * (L - 1)

        colonia[self.estado]["cantidad_ant"] = m
        # innivición de eclosión de huevos
        return m
