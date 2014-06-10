#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Este módulo contiene la definición de datos utilizados en el simulador.

@autors Maximiliano Báez, Roberto Bañuelos
@contact mxbg.py@gmail.com, robertobanuelos@gmail.com
"""
from datatype import *
from db_manager import *

DAO = PuntosControlModel()


class RankingTable:

    """
    Se encarga de guardar en memoria  el valor de todas las zonas que ya
    fueron rankeadas en algún momento para evitar calculos incecesarios.
    """
    @property
    def memory(self):
        """Tabla en memoria"""
        return self.__memory

    @memory.setter
    def memory(self, value):
        self.__memory = value

    def __init__(self):
        self.__memory = {}

    def get_tipo_zona(self, pts):
        """
        60 < Pts  Optima
        60 > Pts  Buena
        30 > Pts  Normal
        20 > Pts  Mala
        8 > Pts   Pésima
        "OPTIMA", "BUENA", "NORMAL", "MALA", "PESIMA"]
        """
        if pts < 11:
            return Zonas.PESIMA

        elif pts >= 11 and pts < 23:
            return Zonas.MALA

        elif pts >= 23 and pts < 41:
            return Zonas.NORMAL

        elif pts >= 41 and pts < 67:
            return Zonas.BUENA

        elif pts >= 67:
            return Zonas.OPTIMA

    def gen_key(self, punto, distancia):
        """
        Genera una clave única para el punto y la distancia.
        """
        return str(punto.x) + "-" + str(punto.y) + "-" + str(distancia)

    def raking_zona(self, point, distancia):
        """
        Este método se encarga de analizar los puntos criticos y dar un
        puntaje a la zona. Una zona se califica teniendo en cuenta :

        * La cantidad de puntos criticos que existen en la zona.
        * El riesgo de los puntos criticos.
        """
        rank_value = 0.0
        dist_value = 0.0
        #~ Se obtienen todos los puntos de riesgo que se encuentran en la zona
        #~ para analizar si el mosquito debe volar en busca de mejores
        #~ condiciones
        zona_muestras = DAO.get_within(point, distancia)
        if len(zona_muestras) == 0:
            return 0

        sum_wi = 0
        _sum = 0
        p = 1.7
        #~ se evaluan los puntos de riesgo
        for i in range(len(zona_muestras)):
            dx = point.distance_to(zona_muestras[i])
            if dx > 0:
                sum_wi += 1 / (dx ** p)

        for i in range(len(zona_muestras)):
            dx = point.distance_to(zona_muestras[i])
            if dx > 0:
                wi = 1 / (dx ** p)
                ui = zona_muestras[i]['cantidad']
                rank_value += (wi * ui) / sum_wi
                _sum += ui

        # print str(_sum / len(zona_muestras)) + " \t " + str(rank_value)
        #~ se calcula el promedio de riesgo
        rank_value = rank_value / len(zona_muestras)

        return rank_value

    def lagrange_i(self, bs, i):
        X = [0, 10.0, 23.0, 67.0, 100.0]
        l_i = 1.0
        for j in range(0, len(X)):
            if j != i:
                l_i *= (bs - X[j]) / (X[i] - X[j])
        return l_i

    def get_bs_ij(self, cantidad):
        Y = [15.0, 15.0, 25.0, 50.0, 50.0]
        if cantidad >= 100:
            return 50

        p_x = 0
        for i in range(0, len(Y)):
            p_x += self.lagrange_i(cantidad, i) * Y[i]
        return p_x

    def get_ranking(self, punto, distancia):
        """
        Se ecarga de verificar si la zona ya fue rankeada, de ser así
        se retorna el valor de la tabla de zonas rankeadas. Si no fue
        rankeada se rankea la zona y se guarda en la tabla de ranking.
        """
        key = self.gen_key(punto, distancia)
        if not self.memory.has_key(key):
            rank_value = self.raking_zona(punto, distancia)
            self.memory[key] = self.get_bs_ij(rank_value)

        return self.memory[key]
