#! /usr/bin/env python
# -*- coding: utf-8 -*-

#~ Configuraciones para la conexión con la base de datos
DB = {
    "dbname" : "dengue",
    "host": "localhost",
    "port": "5432",
    "user": "postgres",
    "password": "postgres"
}

TMP_HOME = "./data/"
RASTER = {
    "schema": "public",
    "table" : "tabla",
    "srid" : "900913",
    "pk" : "id"
}
#~ Configuraciones para la conexión con el geoserver.
GEOSERVER = {
    "host":"localhost",
    "port":"8080",
    "user": "admin",
    "password": "admin",
    "workspace": "geodengue"
}
