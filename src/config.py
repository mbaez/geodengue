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

#~ URL = 'http://www.tutiempo.net/tiempo/Asuncion_Aeropuerto/SGAS.htm?datos=por-horas'
LOCALIDADES_HORA ={
    "Asuncion" : 'tiempo/Asuncion_Aeropuerto/SGAS.htm?datos=por-horas'
}
# Datos utilizads para contruir los queryparams para realizar el get
API_DATA = {
    "appid" : "2d9be00662629ff5c269672af48013d8",
    "type" : "day",
    "id" : "3439389",
    "mode" : "json"
}
# URLs de las fuentes de información de datos climaticos
#~ API_URL = "http://api.openweathermap.org/data/2.5";
API_URL = "http://localhost/geodengue/api.openweathermap.json";
TUTIEMPO_URL = 'http://www.tutiempo.net/'
