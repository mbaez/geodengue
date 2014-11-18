#! /usr/bin/env python
# -*- coding: utf-8 -*-

import psycopg2
from psycopg2 import connect
import psycopg2.extras
"""
@autors Maximiliano Báez
@contact mxbg.py@gmail.com
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

    def get_codigos_by_muestra(self, id_muestra):
        """
        Se encarga de obtener la lista de códigos exitentes para un id de muestra especificado
        previamente.

            SELECT DISTINCT codigo
            FROM evolucion_log
            WHERE id_muestra = %(id_muestra)s
        """
        # se definie el query de la consulta.
        sql_string = """
            SELECT DISTINCT codigo, id_muestra, max(dia), min(dia)
            FROM evolucion_log
            WHERE id_muestra = %(id_muestra)s
            GROUP BY codigo, id_muestra
        """
        # se construye el diccionario que contiene los parametros del query.
        cursor = self.db.query(sql_string, {"id_muestra": id_muestra})
        return self.db.to_dict(cursor)

    def get_tasa_desarrollo(self, codigo):
        """
        Se encarga de calcular la tasa de desarrollo diaria para todas la estapas del ciclo de vida
        del mosquito.
        """

        sql_string = """
        select * from (
            select x.codigo, x.estado, round (sum(x.c - x.m)*1.0/count(x),2) as dias
            from(
                select codigo,estado, min(dia) as m, max(dia) as c
                from evolucion_log tmp
                where estado = 'HUEVO'
                and expectativa_de_vida != 0
                and exists (
                    select *
                    from evolucion_log
                    where id_mosquito = tmp.id_mosquito and estado = 'LARVA'
                    and codigo = tmp.codigo
                )
                group by codigo, id_mosquito, estado
                order by id_mosquito
            ) x
            group by x.codigo,x.estado
            UNION
            select x.codigo, x.estado, round (sum(x.c - x.m)*1.0/count(x),2) as dias
            from(
                select codigo,estado, min(dia) as m, max(dia) as c
                from evolucion_log tmp
                where estado = 'LARVA'
                and expectativa_de_vida != 0
                and exists (
                    select *
                    from evolucion_log
                    where id_mosquito = tmp.id_mosquito and estado = 'PUPA'
                    and codigo = tmp.codigo
                )
                group by codigo, id_mosquito, estado
                order by id_mosquito
            ) x
            group by x.codigo,x.estado
            UNION
            select x.codigo, x.estado, round (sum(x.c - x.m)*1.0/count(x),2) as dias
            from(
                select codigo,estado, min(dia) as m, max(dia) as c
                from evolucion_log tmp
                where estado = 'PUPA'
                and expectativa_de_vida != 0
                and exists (
                    select *
                    from evolucion_log
                    where id_mosquito = tmp.id_mosquito and estado = 'ADULTO'
                    and codigo = tmp.codigo
                )
                group by codigo, id_mosquito, estado
                order by id_mosquito
            ) x
            group by x.codigo,x.estado
            UNION
            select x.codigo, x.estado, round (sum(x.c - x.m)*1.0/count(x),2) as dias
            from(
                select codigo,estado, min(dia) as m, max(dia) as c
                from evolucion_log tmp
                where estado = 'ADULTO'
                and id_mosquito_padre =0
                group by codigo, id_mosquito, estado
                order by id_mosquito
            ) x
            group by x.codigo,x.estado
        ) todos
        where  todos.codigo= %(codigo)s
        """
        # se construye el diccionario que contiene los parametros del query.
        cursor = self.db.query(sql_string, {"codigo": codigo})
        return self.db.to_dict(cursor)

    def get_tasa_mortalidad(self, codigo):
        """
        Se encarga de calcular la tasa de mortalidad diaria para todas la estapas del ciclo de vida
        del mosquito.
        """
        # se definie el query de la consulta.
        sql_string = """
        select tmp.codigo, tmp.estado, sum(tmp.total) as muertos,
        sum(tmp2.total) as total, round(sum(tmp.total)/sum(tmp2.total), 4) * 100.0 as "porcentaje"
        from (
            select codigo,dia,estado, count(*) as total
            from evolucion_log as tmp
            where expectativa_de_vida = 0
            group by codigo,dia, estado
            order by dia
        ) as tmp, (
            select codigo, dia,estado, count(*) as total
            from evolucion_log as tmp
            group by codigo,dia, estado
            order by dia
        ) tmp2
        where tmp.codigo = tmp2.codigo
        and tmp.estado = tmp2.estado
        and tmp.codigo= %(codigo)s
        and tmp.dia = tmp2.dia
        group by tmp.codigo,tmp.estado
        order by codigo, estado;
        """
        # se construye el diccionario que contiene los parametros del query.
        cursor = self.db.query(sql_string, {"codigo": codigo})
        return self.db.to_dict(cursor)

    def get_poblacion_diaria(self, codigo):
        """
        Se encarga de calcular el estado diario de la poblacion
        """
        # se definie el query de la consulta.
        sql_string = """
        select tmp.codigo, tmp.dia, tmp.estado, sum(tmp.total) as muertos,
        sum(tmp2.total) as total, round(sum(tmp.total)/sum(tmp2.total), 4) * 100.0 as "porcentaje"
        from (
            select codigo,dia,estado, count(*) as total
            from evolucion_log as tmp
            where expectativa_de_vida = 0
            group by codigo,dia, estado
            order by dia
        ) as tmp, (
            select codigo, dia,estado, count(*) as total
            from evolucion_log as tmp
            group by codigo,dia, estado
            order by dia
        ) tmp2
        where tmp.codigo = tmp2.codigo
        and tmp.estado = tmp2.estado
        and tmp.codigo= %(codigo)s
        and tmp.dia = tmp2.dia
        group by tmp.codigo,tmp.estado,tmp.dia
        order by codigo, estado;
        """
        # se construye el diccionario que contiene los parametros del query.
        cursor = self.db.query(sql_string, {"codigo": codigo})
        return self.db.to_dict(cursor)

    def get_dispersion(self, codigo):
        """
        Se encarga de calcular el estado diario de la poblacion
        """
        # se definie el query de la consulta.
        sql_string = """
        select codigo, tipo_zona, sum(distancia_recorrida)/count(*) as distancia
        from evolucion_log as tmp
        where estado='ADULTO'
            and sexo = 'HEMBRA'
            and tmp.codigo = %(codigo)s
        group by tmp.codigo, tipo_zona
        order by tmp.codigo, tipo_zona
        """
        # se construye el diccionario que contiene los parametros del query.
        cursor = self.db.query(sql_string, {"codigo": codigo})
        return self.db.to_dict(cursor)

    def get_ciclo_gonotrofico(self, codigo):
        """
        Se encarga de calcular el estado diario de la poblacion
        """
        # se definie el query de la consulta.
        sql_string = """
        select * from (
        select codigo,2 as tipo,sum(tmp.cg_dias)/count(tmp) as dias
        from (
            select codigo, id_mosquito,cantidad_oviposicion, ciclo_gonotrofico as cg_dias
            from evolucion_log
            where ciclo_gonotrofico is not null
            and ciclo_gonotrofico > 0
            and estado='ADULTO'
            and sexo = 'HEMBRA'
            and se_alimenta = 'TRUE'
            and cantidad_oviposicion > 0
            group by codigo, id_mosquito,cantidad_oviposicion ,ciclo_gonotrofico
        ) as tmp
        group by codigo
        --order by codigo

        UNION

        select codigo,1 as tipo, sum(tmp.cg_dias)/count(tmp)  as dias
        from (
            select codigo, id_mosquito,cantidad_oviposicion, ciclo_gonotrofico as cg_dias
            from evolucion_log
            where ciclo_gonotrofico is not null
            and ciclo_gonotrofico > 0
            and estado='ADULTO'
            and sexo = 'HEMBRA'
            and se_alimenta = 'TRUE'
            and cantidad_oviposicion = 0
            group by codigo, id_mosquito,cantidad_oviposicion ,ciclo_gonotrofico
        ) as tmp
        group by codigo

        UNION

        select codigo,0 as tipo, sum(tmp.cg_dias)/count(tmp)  as dias
        from (
            select codigo, id_mosquito,cantidad_oviposicion, ciclo_gonotrofico as cg_dias
            from evolucion_log
            where ciclo_gonotrofico is not null
            and ciclo_gonotrofico > 0
            and estado='ADULTO'
            and sexo = 'HEMBRA'
            and se_alimenta = 'TRUE'
            --and cantidad_oviposicion = 0
            group by codigo, id_mosquito,cantidad_oviposicion ,ciclo_gonotrofico
        ) as tmp
        group by codigo

        ) as todos
        where todos.codigo=%(codigo)s
        order by todos.codigo

        """
        # se construye el diccionario que contiene los parametros del query.
        cursor = self.db.query(sql_string, {"codigo": codigo})
        return self.db.to_dict(cursor)

    def get_cantidad_dias(self, codigo):
        # se definie el query de la consulta.
        sql_string = """
        select max(dia), min(dia) from evolucion_log
        where codigo = %(codigo)s
        """
        # se construye el diccionario que contiene los parametros del query.
        cursor = self.db.query(sql_string, {"codigo": codigo})
        return self.db.to_dict(cursor)

    def get_poblacion_control(self, codigo, dia):
        # se definie el query de la consulta.
        sql_string = """
        SELECT 0 as id, id_muestra, codigo, dia, count(*) as cantidad,
        ST_X(the_geom) as x, ST_Y(the_geom) as y
        FROM evolucion_log
        WHERE codigo=%(codigo)s
            AND dia = %(dia)s
            AND estado != 'ADULTO'
        GROUP BY the_geom, codigo, dia, id_muestra
        """
        # se construye el diccionario que contiene los parametros del query.
        cursor = self.db.query(sql_string, {"codigo": codigo, "dia": dia})
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

    #dao = ConfiguracionesDao()
    dao = ReporteDao()
    #~ print dao.get_poblacion_por_dia()
    #~ print '--------------------------'
    #~ print dao.get_poblacion_nueva_por_dia()
    #~ print '--------------------------'
    #~ print dao.get_poblacion_inicial_por_dia()
    list = dao.get_poblacion_control('2 temp=30 D=1', 1)
    for el in list:
        print el
