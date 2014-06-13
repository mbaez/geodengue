#! /usr/bin/env python
# -*- coding: utf-8 -*-

import psycopg2
from psycopg2 import connect
import psycopg2.extras
"""
@autors Maximiliano Báez, Roberto Bañuelos
@contact mxbg.py@gmail.com, robertobanuelos@gmail.com
"""


class DBManager:

    def __init__(self):
        self.connection = connect(
            """ dbname=geodenguedb
            host=localhost
            user=postgres
            password=postgres
        """)
        self.connection.autocommit = True

    def close(self):
        """
        Este método se encarga de cerrar la conexión
        """
        self.connection.close()

    def query(self, query_string, args={}, is_many=False):
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
        if not is_many:
            cursor.execute(query_string, args)
        else:
            cursor.executemany(query_string, args)
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
        dbcursor.close()
        # se retorna la lista de resultados
        return results


class PuntosControlModel:

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
        args = {'id_muestras': id_muestras}
        cursor = self.db.query(sql_string, args)
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
            SELECT id,  id_muestras, codigo, descripcion,
                cantidad, ST_X(the_geom) as x, ST_Y(the_geom) as y
            FROM puntos_control
            WHERE fecha_recoleccion is not null
            AND ST_DWithin(
            Geography(the_geom),
            Geography(
                ST_GeomFromText('POINT(%(x)s  %(y)s)',
                4326)
            ), %(distance)s)
        """
        args = {"distance": distance}
        args["x"] = point.x
        args["y"] = point.y
        # se construye el diccionario que contiene los parametros del query.
        cursor = self.db.query(sql_string, args)
        return self.db.to_dict(cursor)


class CoefSarpeDemicheleModel:

    """
    Esta clase define la capa de acceso y comunicación para la tabla
    `coef_sharpe_demichele`.
    id integer NOT NULL DEFAULT nextval('coef_sharpe_demichele_id_seq'::regclass),
    descripcion character varying(100),
    rh025 double precision,
    ha double precision,
    hh double precision,
    th double precision,
    codigo character varying(15),
    """

    def __init__(self):
        self.db = DBManager()

    def get_all(self):
        """
        Se encarga de obtener los datos de la tabla de coeficientes para
        el modelo de sharpe&demichele

            SELECT codigo, rh025, ha, hh, th
            FROM coef_sharpe_demichele

        @rtype  Dictionaries
        @return Un diccionario con el resultado de la consulta
        """
        # se definie el query de la consulta.
        sql_string = """
            SELECT codigo, rh025, ha, hh, th
            FROM coef_sharpe_demichele
        """
        # se construye el diccionario que contiene los parametros del query.
        cursor = self.db.query(sql_string)
        return self.db.to_dict(cursor)

    def get_by(self, codigo):
        """
        Se encarga de obtener los datos de la tabla de coeficientes para
        el modelo de sharpe&demichele

            SELECT codigo, rh025, ha, hh, th
            FROM coef_sharpe_demichele
            where codigo= :codigo

        @rtype  Dictionaries
        @return Un diccionario con el resultado de la consulta
        """
        # se definie el query de la consulta.
        sql_string = """
            SELECT codigo, rh025, ha, hh, th
            FROM coef_sharpe_demichele
            WHERE codigo = %(codigo)s
        """
        # se construye el diccionario que contiene los parametros del query.
        cursor = self.db.query(sql_string, {"codigo": codigo})
        return self.db.to_dict(cursor)


class InterpolacionModel:

    """
    Esta clase define la capa de acceso y comunicación para la tabla
    `interpolacion`.
    """

    def __init__(self):
        self.db = DBManager()

    def persist(self, args={}):
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


class PuntosRiesgoDao:

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
            SELECT pr.id, pr.codigo, pr.id_tipo, pr.descripcion, tr.riesgo,
            ST_X(the_geom) as x, ST_Y(the_geom) as y
            FROM puntos_riesgo pr JOIN tipo_riesgo tr
                ON pr.id_tipo = tr.id
            WHERE (fecha_fin is null
                    OR (fecha_inicio >= now() AND fecha_fin <= now())
                )
            AND ST_DWithin(
            Geography(the_geom),
            Geography(
                ST_GeomFromText('POINT(%(x)s  %(y)s)',
                4326)
            ), %(distance)s)
        """
        args = {"distance": distance}
        args["x"] = point.x
        args["y"] = point.y
        # se construye el diccionario que contiene los parametros del query.
        cursor = self.db.query(sql_string, args)
        return self.db.to_dict(cursor)


class MuestraModel:

    """
    Esta clase define la capa de acceso y comunicación para la tabla
    `muestras`.
    id integer NOT NULL DEFAULT nextval('muestras_id_seq'::regclass),
    id_tipo_dispositivo integer,
    codigo integer,
    descripcion character varying(100),
    fecha timestamp without time zone
    """

    def __init__(self):
        self.db = DBManager()

    def get_all(self):
        """
        Se encarga de obtener los datos de la tabla de muestras

            SELECT id, id_tipo_dispositivo, codigo, descripcion, fecha
            FROM muestras

        @rtype  Dictionaries
        @return Un diccionario con el resultado de la consulta
        """
        # se definie el query de la consulta.
        sql_string = """
        SELECT id, id_tipo_dispositivo, codigo, descripcion, fecha
            FROM muestras
        """
        # se construye el diccionario que contiene los parametros del query.
        cursor = self.db.query(sql_string)
        return self.db.to_dict(cursor)

    def get_by(self, id_muestra):
        """
        Se encarga de obtener los datos de la tabla de muestras filtrado
        por el id de la muestra.

        SELECT id, id_tipo_dispositivo, codigo, descripcion, fecha
            FROM muestras
            where id= :id_muestra

        @rtype  Dictionaries
        @return Un diccionario con el resultado de la consulta
        """
        # se definie el query de la consulta.
        sql_string = """
        SELECT id, id_tipo_dispositivo, codigo, descripcion,
            cast(fecha as date)
            FROM muestras
            WHERE id = %(id_muestra)s
        """
        # se construye el diccionario que contiene los parametros del query.
        cursor = self.db.query(sql_string, {"id_muestra": id_muestra})
        return self.db.to_dict(cursor)


class LayersDao:

    """
    """

    def __init__(self):
        self.db = DBManager()

    def get_by(self, layer_name):
        """

        SELECT id_muestra, layer_name,  fecha
            FROM layers
            WHERE layer_name = :layer_name

        @rtype  Dictionaries
        @return Un diccionario con el resultado de la consulta
        """
        # se definie el query de la consulta.
        sql_string = """
        SELECT id_muestra, layer_name,  fecha
            FROM layers
            WHERE layer_name = %(layer_name)s
        """
        print layer_name
        # se construye el diccionario que contiene los parametros del query.
        cursor = self.db.query(sql_string, {"layer_name": layer_name})
        return self.db.to_dict(cursor)

    def persist(self, layer):
        """

        INSERT INTO layers (id_muestra, layer_name, fecha)
            VALUES (:id_muestra, :layer_name, :fecha)
        """
        # se definie el query de la consulta.
        sql_string = """
        INSERT INTO layers (id_muestra, layer_name, fecha)
            VALUES (%(id_muestra)s, %(layer_name)s, %(fecha)s)
        """
        # se construye el diccionario que contiene los parametros del query.
        cursor = self.db.query(sql_string, layer)
        return cursor


class ReporteDao:

    """
    Esta clase define la capa de acceso y comunicación para la tabla
    'evolucionar_log'.
    En esta clase se encapsulan los metodos para el acceso a la
    informacion utilizada en los reportes
    * cantidad de muertes, por dia, por sexo, por estado
    * indices de infestacion
    * cantidad de huevos
    * otros
    """

    def __init__(self):
        self.db = DBManager()

    def get_poblacion_inicial_por_dia(self):
        """
        Se encarga de obtener los datos sobre la cantidad de individuos
        vivos de la poblacion inicial por dia de la tabla de
        evolucion_log

            select dia, count(*)
            from evolucion_log
            where expectativa_de_vida != 0
            and id_mosquito_padre = 0
            group by dia
            order by dia

        @rtype  Dictionaries
        @return Un diccionario con el resultado de la consulta
        """
        # se definie el query de la consulta.
        sql_string = """
            select dia, count(*)
            from evolucion_log
            where expectativa_de_vida != 0
            and id_mosquito_padre = 0
            group by dia
            order by dia
        """
        # se construye el diccionario que contiene los parametros del query.
        cursor = self.db.query(sql_string)
        return self.db.to_dict(cursor)

    def get_poblacion_nueva_por_dia(self):
        """
        Se encarga de obtener los datos sobre la cantidad de individuos
        vivos de la nueva por dia de la tabla de evolucion_log

            select dia, count(*)
            from evolucion_log
            where expectativa_de_vida != 0
            and id_mosquito_padre != 0
            group by dia
            order by dia

        @rtype  Dictionaries
        @return Un diccionario con el resultado de la consulta
        """
        # se definie el query de la consulta.
        sql_string = """
            select dia, count(*)
            from evolucion_log
            where expectativa_de_vida != 0
            and id_mosquito_padre != 0
            group by dia
            order by dia
        """
        # se construye el diccionario que contiene los parametros del query.
        cursor = self.db.query(sql_string)
        return self.db.to_dict(cursor)

    def get_poblacion_por_dia(self):
        """
        Se encarga de obtener los datos sobre la cantidad de individuos
        vivos por dia de la tabla de evolucion_log

            select dia, count(*)
            from evolucion_log
            where expectativa_de_vida != 0

            group by dia
            order by dia

        @rtype  Dictionaries
        @return Un diccionario con el resultado de la consulta
        """
        # se definie el query de la consulta.
        sql_string = """
            select dia, count(*)
            from evolucion_log
            where expectativa_de_vida != 0

            group by dia
            order by dia
        """
        # se construye el diccionario que contiene los parametros del query.
        cursor = self.db.query(sql_string)
        return self.db.to_dict(cursor)

    def get_distribucion_de_estados(self, dia):
        """
        Se encarga de obtener la cantidad de huevos, larvas, pupas y
        adultos en un dia especifico

        select count(*) , estado
        from evolucion_log
        where dia = <dia>
        group by estado

        """

        # se definie el query de la consulta.
        sql_string = """
            select count(*) , estado
            from evolucion_log
            where dia = %(dia)s
            group by estado
        """
         # se construye el diccionario que contiene los parametros del query.
        cursor = self.db.query(sql_string, {"dia": dia})
        return self.db.to_dict(cursor)

    def get_tiempo_promedio_de_vida(self, estado):
        """
        Se encarga de obtener los datos sobre el tiempo promedio de los
        diferentes estados.
        si :estado = ADULTO se tiene un valor x que representa el tiempo
        promedio de vida de toda la poblacion que llego al estado ADULTO

        select cast(sum(x.c) as float)/max(y.c)
        from(select max(edad) as c
            from evolucion_log
            where estado = :estado
            and id_mosquito_padre != 0
            group by id_mosquito
            order by id_mosquito) x,
            (select count(distinct(id_mosquito)) as c
            from evolucion_log
            where estado = :estado
            and id_mosquito_padre != 0) y;
        """

        # se definie el query de la consulta.
        sql_string = """
            select cast(sum(x.c) as float)/max(y.c) as tiempo_promedio
            from(select max(edad) as c
            from evolucion_log
            where estado = %(estado)s
            and id_mosquito_padre != 0
            group by id_mosquito
            order by id_mosquito) x,
            (select count(distinct(id_mosquito)) as c
            from evolucion_log
            where estado = %(estado)s
            and id_mosquito_padre != 0) y;
        """
         # se construye el diccionario que contiene los parametros del query.
        cursor = self.db.query(sql_string, {"estado": estado})
        return self.db.to_dict(cursor)

    def get_cantidad_promedio_de_huevo(self):
        """
        Obtiene la cantidad promedio de huevos depositados
        Si se realicen en total x oviposturas, el metodo
        halla la cantidad promedio de huevos generados sobre el total
        de oviposturas x dentro del periodo de estudio.

        select sum(cantidad_huevos)/count(*)
        from evolucion_log
        where cantidad_huevos > 0

        """
        # se definie el query de la consulta.
        sql_string = """
            select sum(cantidad_huevos)/count(*)
            from evolucion_log
            where cantidad_huevos > 0
        """
         # se construye el diccionario que contiene los parametros del query.
        cursor = self.db.query(sql_string)
        return self.db.to_dict(cursor)

    def get_distribucion_de_sexo(self):
        """
        Obtiene la cantidad de individuos MACHO y la cantidad de
        individuos HEMBRA dentro de la poblacion total.

        Permite determinar la distribucion de sexos
        """
        # se definie el query de la consulta.
        sql_string = """
            select sexo, count(distinct (id_mosquito))
            from evolucion_log
            group by sexo
        """
         # se construye el diccionario que contiene los parametros del query.
        cursor = self.db.query(sql_string)
        return self.db.to_dict(cursor)


class ConfiguracionesDao:

    """
    """

    def __init__(self):
        self.db = DBManager()

    def get_all(self):
        """

        SELECT id_muestra, layer_name,  fecha
            FROM configuraciones

        @rtype  Dictionaries
        @return Un diccionario con el resultado de la consulta
        """
        # se definie el query de la consulta.
        sql_string = """
        SELECT id, clave, valor
            FROM configuraciones
        """
        # se construye el diccionario que contiene los parametros del query.
        cursor = self.db.query(sql_string)
        return self.db.to_dict(cursor)


if __name__ == "__main__":
    #~ dic = da.get_by(1)
    #a = PuntosRiesgoDao()
    #dic = a.get_all();
    #~ dao = MuestraModel()
    #~ print dao.get_all()
    #~ cursor = a.persist({'id_muestra': 1, 'descripcion': 'test'})
    #~ print cursor.fetchone()[0]

    dao = ConfiguracionesDao()
    #~ print dao.get_poblacion_por_dia()
    #~ print '--------------------------'
    #~ print dao.get_poblacion_nueva_por_dia()
    #~ print '--------------------------'
    #~ print dao.get_poblacion_inicial_por_dia()
    print dao.get_all()
