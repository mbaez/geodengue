#! /usr/bin/env python
# -*- coding: utf-8 -*-

import psycopg2
from psycopg2 import connect
import psycopg2.extras

__author__ = "Maximiliano Báez"
__mail__ = "mxbg.py@gmail.com"


class DBManager :
    """
    """
    def __init__(self):
        """
        """
        self.connection = connect(
        """ dbname=dengue
            host=localhost
            user=postgres
            password=postgres
        """)
        self.connection.autocommit = True;

    def query (self, query_string, args={}):
        """
        """
        for key in args.keys():
            query_string = query_string.replace(':'+key, str(args[key]))

        cursor = self.connection.cursor()
        cursor.execute(query_string)
        return cursor


    def to_dict(self, dbcursor):
        """
        """
        # test for and store results
        results = dbcursor.fetchall( )
        if results < 1:
            return results

        # replace results lists with dicts
        rownum = 0
        for row in results:
            dictrow = {}
            dictnum = 0
            for col in dbcursor.description:
                dictrow[col[0]] = row[dictnum]
                dictnum += 1
            results[rownum] = dictrow
            rownum += 1
        return results


class PuntosControlModel :

    def __init__(self):
        self.db = DBManager()

    def get_by(self, id_muestras):
        sql_string = """
            SELECT id,  id_muestras, codigo, descripcion,
                cantidad, X(the_geom), Y(the_geom)
            FROM puntos_control
            WHERE id_muestras = :id_muestras
        """
        args = {'id_muestras' : id_muestras};
        cursor = self.db.query(sql_string, args)
        return self.db.to_dict(cursor)


class InterpolacionModel :

    def __init__(self):
        self.db = DBManager()

    def persist(self,args={}):
        sql_string = """
        INSERT INTO interpolacion(
            id_muestra, descripcion)
        VALUES (:id_muestra,':descripcion');
        """
        cursor = self.db.query(sql_string, args)
        return cursor

class PuntosInterpoladosModel :

    def __init__(self):
        self.db = DBManager()

    def persist(self,args={}):
        sql_string = """
        INSERT INTO puntos_interpolados(
            id_interpolacion, cantidad, the_geom)
        VALUES ( :id_interpolacion, :cantidad,
            ST_SetSRID(ST_MakePoint(:x, :y), 900913))
        """
        cursor = self.db.query(sql_string, args)
        return cursor


if __name__ == "__main__" :
    #~ da = PuntosControlModel()
    #~ dic = da.get_by(1);
    a = InterpolacionModel()
    a.persist({'id_muestra': 1, 'descripcion': 'test'})
    #print dic
