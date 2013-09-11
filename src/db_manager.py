#! /usr/bin/env python
# -*- coding: utf-8 -*-

import psycopg2
from psycopg2 import connect
import psycopg2.extras
"""
@autors Maximiliano Báez, Roberto Bañuelos
@contact mxbg.py@gmail.com, robertobanuelos@gmail.com
"""


class DBManager :
    def __init__(self):
        self.connection = connect(
        """ dbname=geodenguedb
            host=localhost
            user=postgres
            password=postgres
        """)
        self.connection.autocommit = True;

    def close (self) :
        """
        Este método se encarga de cerrar la conexión
        """
        self.connection.close();

    def query (self, query_string, args={}, is_many=False):
        """
        Este método se encarga de construir la consulta sql definida en
        `query_string`, establce la conexión en la base de datos y
        ejecuta la consulta.

            SELECT * FROM tabla WHERE id = :id

        @type query_string : String
        @param query_string: La referencia al cursor de la consulta.

        @type args : Dictionaries
        @param args: Un diccionario con los parametros del query.

        @type insert_many : Boolean
        @param insert_many: True para activar el executemany.

        @rtype  Cursor
        @return La referencia al cursor de la consulta.
        """
        #~ for key in args.keys():
            #~ query_string = query_string.replace(':'+key, str(args[key]))

        cursor = self.connection.cursor()
        #~ print args
        if not is_many :
            cursor.execute(query_string,args)
        else :
            cursor.executemany(query_string,args)
        return cursor

    def to_dict(self, dbcursor):
        """
        Se encarga de procesar el cusor y generar un diccionario con los
        datos obtenidos del cursor. Las columnas de los campos del cursor
        son utilizadas como claves de diccionario.

        @type dbcursor : Cursor
        @param dbcursor : La referencia al cursor de la consulta.

        @rtype  Dictionaries
        @return Un diccionario con los datos del cursor.
        """
        # se obtienen todos los datos
        results = dbcursor.fetchall()
        if results < 1:
            return results

        # se genera el array de resultados a partir de cursor
        rownum = 0
        for row in results:
            dictrow = {}
            dictnum = 0
            for col in dbcursor.description:
                dictrow[col[0]] = row[dictnum]
                dictnum += 1
            results[rownum] = dictrow
            rownum += 1

        #se retorna la lista de resultados
        return results


class PuntosControlModel :
    """
    Esta clase define la capa de acceso y comunicación para la tabla
    `puntos_control`.
    """
    def __init__(self):
        self.db = DBManager()

    def get_by(self, id_muestras):
        """
        Se encarga de obtener la lista de puntos de control que poseean
        el `id_muestras` definido.

            SELECT id,  id_muestras, codigo, descripcion,
                   cantidad, ST_X(the_geom), ST_Y(the_geom)
            FROM puntos_control
            WHERE id_muestras = :id_muestras

        @type id_muestras : Integer
        @param id_muestras: El id del grupo de muestras.

        @rtype  Dictionaries
        @return Un diccionario con el resultado de la consulta
        """
        # se definie el query de la consulta.
        sql_string = """
            SELECT id,  id_muestras, codigo, descripcion,
                cantidad, ST_X(the_geom) as x, ST_Y(the_geom) as y
            FROM puntos_control
            WHERE id_muestras = %(id_muestras)s
                AND fecha_recoleccion is not null
        """
        # se construye el diccionario que contiene los parametros del query.
        args = {'id_muestras' : id_muestras};
        cursor = self.db.query(sql_string, args)
        return self.db.to_dict(cursor)


class InterpolacionModel :
    """
    Esta clase define la capa de acceso y comunicación para la tabla
    `interpolacion`.
    """
    def __init__(self):
        self.db = DBManager()

    def persist(self,args={}):
        """
        Se encarga de persitir la cabecera en la tabla `interpolacion`.

            INSERT INTO interpolacion(id_muestra, descripcion)
                VALUES (%(id_muestra)s,%(descripcion)s)

        @type args : Dictionaries
        @param args: Un diccionario con los paramteros de la consulta.
        """
        # se definie el query de la consulta.
        sql_string = """
        INSERT INTO interpolacion(id_muestra, descripcion)
            VALUES (%(id_muestra)s,%(descripcion)s)
        RETURNING id
        """
        # se construye el diccionario que contiene los parametros del query.
        cursor = self.db.query(sql_string, args)
        return cursor


class PuntosRiesgoDao :
    """
    Esta clase define la capa de acceso y comunicación para la tabla
    `puntos_control`.
    """
    def __init__(self):
        self.db = DBManager()

    def get_all(self):
        """
        Se encarga de obtener la lista de todos los puntos de riesgo definidos

        @rtype  Dictionaries
        @return Un diccionario con el resultado de la consulta
        """
        # se definie el query de la consulta.
        sql_string = """
            SELECT id, codigo, id_tipo, descripcion,
            ST_X(the_geom) as x, ST_Y(the_geom) as y
            FROM puntos_riesgo
            WHERE fecha_fin is null
                OR (fecha_inicio >= now() AND fecha_fin <= now())
        """
        # se construye el diccionario que contiene los parametros del query.
        cursor = self.db.query(sql_string)
        return self.db.to_dict(cursor)

    def get_within(self, point, distance):
        """
        Se encarga de obtener la lista de todos los puntos que se encuentran
        a una determinada distancia del punto de origen.

        @rtype  Dictionaries
        @return Un diccionario con el resultado de la consulta
        """
        # se definie el query de la consulta.
        sql_string = """
            SELECT id, codigo, id_tipo, descripcion,
            ST_X(the_geom) as x, ST_Y(the_geom) as y
            FROM puntos_riesgo
            WHERE (fecha_fin is null
                    OR (fecha_inicio >= now() AND fecha_fin <= now())
                )
            AND ST_DWithin(
            Geography(the_geom),
            Geography(
                ST_GeomFromText('POINT(%(x)s  %(y)s)',
                4326)
            ), %(distance))
        """
        args = {"distance" : distance}
        args["x"] = point.x
        args["y"] = point.y
        # se construye el diccionario que contiene los parametros del query.
        cursor = self.db.query(sql_string, args)
        return self.db.to_dict(cursor)


if __name__ == "__main__" :
    #~ dic = da.get_by(1)
    a = PuntosRiesgoDao()
    dic = a.get_all();
    print dic;
    #~ cursor = a.persist({'id_muestra': 1, 'descripcion': 'test'})
    #~ print cursor.fetchone()[0]
