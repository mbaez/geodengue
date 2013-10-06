#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""

Content : Clase encargada de recibir strings de eventos y almacenarlos
en un archivo de salida en formato csv

"""

import os
import sys
import time
from datatype import *

class EventLogger( ):

    def __init__( self, log_name ):
        self.indice = 1
        self.log_file_name = log_name + str(int(time.time()))
        self.path = 'log/'

    def save_event( self, event ) :
        """

        Metodo para almacenar un string en formato csv que representa
        un evento en un archivo

        """
        target = open (self.path + self.log_file_name + '.log', 'a')
        target.write(str(self.indice) + ',')
        target.write(event)
        target.write('\n')
        target.close()

        self.indice += 1

    def to_csv( self, args ) :
        """

        La definicion de columnas dentro del archivo csv es :

        id_mosquito int
        dia int
        hora int
        temperatura int
        sexo string
        expectativa_de_vida float
        tiempo_de_vida float
        tiempo_madurez float
        madurez float
        tipo_zona string
        esta_muerto boolean
        ultima_oviposicion int
        ultimo_alimento int
        distancia_recorrida int
        cantidad_oviposicion int
        cantidad_alimentacion int
        is_inseminada boolean
        se_alimenta boolean
        se_reproduce boolean
        pone_huevos boolean
        cantidad_huevos int
        estado string
        posicion_x float
        posicion_y float


        """

        data_individuo = args['individuo']
        data_hora = args['hora']
        data_dia = args['dia']
        data_temperatura = args['temperatura']
        data_pone_huevos = args['pone_huevos']
        data_cantidad_huevos = args['cantidad_huevos']
        data_temperatura = args['temperatura']

        if data_individuo.estado == Estado.ADULTO :
            data_ultima_oviposicion = data_individuo.ultima_oviposicion
            data_ultimo_alimento = data_individuo.ultimo_alimento
            data_distancia_recorrida = data_individuo.distancia_recorrida
            data_cantidad_oviposicion = data_individuo.cantidad_oviposicion
            data_cantidad_alimentacion = data_individuo.cantidad_alimentacion
            data_is_inseminada = data_individuo.is_inseminada
            data_se_alimenta = data_individuo.se_alimenta
            data_se_reproduce = data_individuo._se_reproduce
        else :
            data_ultima_oviposicion = -1
            data_ultimo_alimento = -1
            data_distancia_recorrida = -1
            data_cantidad_oviposicion = -1
            data_cantidad_alimentacion = -1
            data_is_inseminada = False
            data_se_alimenta = False
            data_se_reproduce = False

        event = str(data_individuo.id_mosquito) + ',' + \
                str(data_hora) + ',' + \
                str(data_dia) + ',' + \
                str(data_temperatura) + ',' + \
                str(data_individuo.sexo) + ',' + \
                str(data_individuo.expectativa_vida) + ',' + \
                str(data_individuo.tiempo_vida) + ',' + \
                str(data_individuo.tiempo_madurez) + ',' + \
                str(data_individuo.madurez) + ',' + \
                str(data_individuo.rank_zona()) + ',' + \
                str(data_individuo.esta_muerto()) + ',' + \
                str(data_ultima_oviposicion) + ',' + \
                str(data_ultimo_alimento) + ',' + \
                str(data_distancia_recorrida) + ',' + \
                str(data_cantidad_oviposicion) + ',' + \
                str(data_cantidad_alimentacion) + ',' + \
                str(data_is_inseminada) + ',' + \
                str(data_se_alimenta) + ',' + \
                str(data_se_reproduce) + ',' + \
                str(data_pone_huevos) + ',' + \
                str(data_cantidad_huevos) + ',' + \
                str(data_individuo.estado) + ',' + \
                str(data_individuo.posicion.x) + ',' + \
                str(data_individuo.posicion.y)

        self.save_event( event )



