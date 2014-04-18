#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""

Content : Clase encargada de recibir strings de eventos y almacenarlos
en un archivo de salida en formato csv

"""
# import threading
import os
import sys
import time
from datatype import *
from db_manager import DBManager


class EventLogger():

    """
    """
    @property
    def id_muestra(self):
        """
        """
        return self.__id_muestra

    def __init__(self, id_muestra):
        self.db = DBManager()
        self.__id_muestra = id_muestra

    def save(self, kargs):
        aedes = kargs['aedes']
        dia = kargs['dia']
        periodo = kargs['periodo']
        args = {}
        args['id_mosquito'] = aedes.id_mosquito
        args['id_mosquito_padre'] = aedes.id_padre
        args['id_muestra'] = self.id_muestra
        args['sexo'] = aedes.sexo
        args['expectativa_de_vida'] = aedes.expectativa_vida
        args['tiempo_madurez'] = aedes.tiempo_madurez
        args['tiempo_de_vida'] = aedes.tiempo_vida
        args['madurez'] = aedes.madurez
        args['tipo_zona'] = dia.get_tipo_clima()
        args['temperatura'] = dia.temperatura
        args['estado'] = aedes.estado
        args['edad'] = aedes.edad
        args['x'] = aedes.posicion.x
        args['y'] = aedes.posicion.y
        # args['fecha'] =
        args['dia'] = periodo
        target_method = None
        if aedes.estado == Estado.ADULTO:
            args['ultima_oviposicion'] = aedes.ultima_oviposicion
            args['ultimo_alimento'] = aedes.ultimo_alimento
            args['distancia_recorrida'] = aedes.distancia_recorrida
            args['cantidad_oviposicion'] = aedes.cantidad_oviposicion
            args['cantidad_alimentacion'] = aedes.cantidad_alimentacion
            args['is_inseminada'] = aedes.is_inseminada
            args['se_alimenta'] = aedes.se_alimenta
            args['se_reproduce'] = aedes.se_reproduce(dia)
            args['cantidad_huevos'] = kargs.get('huevos', 0)
            target_method = self.persist_adulto
        else:
            target_method = self.persist
        # se lanza un thread
        #t = threading.Thread(target=target_method, args=(args,))
        # t.start()
        target_method(args)

    def persist_adulto(self, args):
        """
        """
        # se definie el query de la consulta.
        sql_string = """
        INSERT INTO public.evolucion_log(
            id_mosquito,
            id_mosquito_padre,
            id_muestra,
            temperatura,
            sexo,
            expectativa_de_vida,
            tiempo_de_vida,
            tiempo_madurez,
            madurez,
            tipo_zona,
            ultima_oviposicion,
            ultimo_alimento,
            distancia_recorrida,
            cantidad_oviposicion,
            cantidad_alimentacion,
            is_inseminada,
            se_alimenta,
            se_reproduce,
            cantidad_huevos,
            estado,
            the_geom,
            fecha,
            dia,
            edad)
            VALUES (
                %(id_mosquito)s,
                %(id_mosquito_padre)s,
                %(id_muestra)s,
                %(temperatura)s,
                %(sexo)s,
                %(expectativa_de_vida)s,
                %(tiempo_de_vida)s,
                %(tiempo_madurez)s,
                %(madurez)s,
                %(tipo_zona)s,
                %(ultima_oviposicion)s,
                %(ultimo_alimento)s,
                %(distancia_recorrida)s,
                %(cantidad_oviposicion)s,
                %(cantidad_alimentacion)s,
                %(is_inseminada)s,
                %(se_alimenta)s,
                %(se_reproduce)s,
                %(cantidad_huevos)s,
                %(estado)s,
                ST_GeomFromText('POINT(%(x)s %(y)s)', 4326),
                now(),
                %(dia)s,
                %(edad)s
            );
        """
        # se construye el diccionario que contiene los parametros del query.
        cursor = self.db.query(sql_string, args)
        return cursor

    def persist(self, args):
        """
        """
        # se definie el query de la consulta.
        sql_string = """
        INSERT INTO public.evolucion_log(
            id_mosquito,
            id_mosquito_padre,
            id_muestra,
            temperatura,
            sexo,
            expectativa_de_vida,
            tiempo_de_vida,
            tiempo_madurez,
            madurez,
            tipo_zona,
            estado,
            the_geom,
            fecha,
            dia,
            edad
        ) VALUES (
            %(id_mosquito)s,
            %(id_mosquito_padre)s,
            %(id_muestra)s,
            %(temperatura)s,
            %(sexo)s,
            %(expectativa_de_vida)s,
            %(tiempo_de_vida)s,
            %(tiempo_madurez)s,
            %(madurez)s,
            %(tipo_zona)s,
            %(estado)s,
            ST_GeomFromText('POINT(%(x)s %(y)s)', 4326),
            now(),
            %(dia)s,
            %(edad)s
            );
        """
        # se construye el diccionario que contiene los parametros del query.
        cursor = self.db.query(sql_string, args)
        return cursor
