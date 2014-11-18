#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Clase encargada de recibir strings de eventos y almacenarlos
en un archivo de salida en un tabla de eventos.

@autors Maximiliano Báez
@contact mxbg.py@gmail.com
"""
import threading
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

    def __init__(self, id_muestra, codigo=''):
        self.db = DBManager()
        self.__id_muestra = id_muestra
        self.__codigo = codigo
        self.query = ""

    def add(self, kargs):
        aedes = kargs['aedes']
        dia = kargs['dia']
        periodo = kargs['periodo']
        args = {}
        args['codigo'] = self.__codigo
        args['id_muestra'] = self.id_muestra
        args['id_mosquito'] = aedes.id_mosquito
        args['id_colonia'] = aedes.id_colonia
        args['id_mosquito_padre'] = aedes.id_padre
        args['sexo'] = aedes.sexo
        args['expectativa_de_vida'] = aedes.expectativa_vida
        args['tiempo_madurez'] = aedes.tiempo_madurez
        args['tiempo_de_vida'] = aedes.tiempo_vida
        args['madurez'] = aedes.madurez
        args['tipo_zona'] = aedes.get_tipo_zona()
        args['bs'] = aedes.get_bs_ij()
        args['temperatura'] = dia.temperatura
        args['estado'] = aedes.estado
        args['edad'] = aedes.edad
        args['generacion'] = aedes.generacion
        args['x'] = aedes.posicion.x
        args['y'] = aedes.posicion.y
        # args['fecha'] =
        args['dia'] = periodo
        target_method = None
        if aedes.estado == Estado.ADULTO:
            args['tipo_zona'] = aedes.tipo_zona
            args['ultima_oviposicion'] = aedes.ultima_oviposicion
            args['ultimo_alimento'] = aedes.ultimo_alimento
            args['distancia_recorrida'] = aedes.distancia_recorrida
            args['desplazamiento_diario'] = aedes.desplazamiento_diario
            args['cantidad_oviposicion'] = aedes.cantidad_oviposicion
            args['cantidad_alimentacion'] = aedes.cantidad_alimentacion
            args['is_inseminada'] = aedes.is_inseminada
            args['se_alimenta'] = aedes.se_alimenta
            args['se_reproduce'] = aedes.se_reproduce(dia)
            args['ciclo_gonotrofico'] = aedes.ciclo_gonotrofico
            args['cantidad_huevos'] = kargs.get('huevos', 0)
            target_method = self.persist_adulto
        else:
            target_method = self.persist
        # se lanza un thread
        self.query += target_method(args)

    def persist_adulto(self, args):
        """
        """
        # se definie el query de la consulta.
        sql_string = """
        INSERT INTO public.evolucion_log(
            id_mosquito,
            id_colonia,
            id_mosquito_padre,
            id_muestra,
            codigo,
            temperatura,
            sexo,
            expectativa_de_vida,
            tiempo_de_vida,
            tiempo_madurez,
            madurez,
            tipo_zona,
            bs,
            ultima_oviposicion,
            ultimo_alimento,
            distancia_recorrida,
            cantidad_oviposicion,
            cantidad_alimentacion,
            is_inseminada,
            se_alimenta,
            se_reproduce,
            ciclo_gonotrofico,
            cantidad_huevos,
            estado,
            the_geom,
            fecha,
            dia,
            generacion,
            edad
            ) VALUES (
                {id_mosquito},
                '{id_colonia}',
                {id_mosquito_padre},
                {id_muestra},
                '{codigo}',
                {temperatura},
                '{sexo}',
                {expectativa_de_vida},
                {tiempo_de_vida},
                {tiempo_madurez},
                {madurez},
                '{tipo_zona}',
                {bs},
                {ultima_oviposicion},
                {ultimo_alimento},
                {distancia_recorrida},
                {cantidad_oviposicion},
                {cantidad_alimentacion},
                {is_inseminada},
                {se_alimenta},
                {se_reproduce},
                {ciclo_gonotrofico},
                {cantidad_huevos},
                '{estado}',
                ST_GeomFromText('POINT({x} {y})', 4326),
                now(),
                {dia},
                {generacion},
                {edad}
            );
        """
        # se construye el diccionario que contiene los parametros del query.
        return sql_string.format(**args)

    def persist(self, args):
        """
        """
        # se definie el query de la consulta.
        sql_string = """
        INSERT INTO public.evolucion_log(
            id_mosquito,
            id_colonia,
            id_mosquito_padre,
            id_muestra,
            codigo,
            temperatura,
            sexo,
            expectativa_de_vida,
            tiempo_de_vida,
            tiempo_madurez,
            madurez,
            tipo_zona,
            bs,
            estado,
            the_geom,
            fecha,
            dia,
            edad,
            generacion
        ) VALUES (
            {id_mosquito},
            '{id_colonia}',
            {id_mosquito_padre},
            {id_muestra},
            '{codigo}',
            {temperatura},
            '{sexo}',
            {expectativa_de_vida},
            {tiempo_de_vida},
            {tiempo_madurez},
            {madurez},
            '{tipo_zona}',
            {bs},
            '{estado}',
            ST_GeomFromText('POINT({x} {y})', 4326),
            now(),
            {dia},
            {edad},
            {generacion}
            );
        """
        # se construye el diccionario que contiene los parametros del query.
        return sql_string.format(**args)

    def save(self):
        sql_string = str(self.query)
        self.query = ""
        if len(sql_string) == 0:
            return

        t = threading.Thread(target=self.db.query, args=(sql_string,))
        t.start()
