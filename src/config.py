#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Configuraciones para la conexión con la base de datos
"""
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

"""
Configuraciones para la conexión con el geoserver.
"""
GEOSERVER = {
    "host":"localhost",
    "port":"8080",
    "user": "admin",
    "password": "admin",
    "workspace": "geodengue"
}

"""
Configuraciones de los servicios de datos climáticos
"""
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

"""
Configuraciones de las Zonas
"""
#~ El tamaño esta a un radio de 200 metros de la del punto de origen
TAMANHO_ZONA = 200
#~ La duración en día de la pupa+larva de acuerdo a las condiciones climáticas
#~ y el tipo de zona
"""
Para LARVAS (P=0.8) Y PUPAS(P=0.2)

60 < Pts  Optima  0   [10, 17.4] * P    [9, 13]* P    [5, 7.2] * P  0
60 > Pts  Buena   0   [17.4, 24.8] * P  [13, 17]* P   [7.2, 9.4] * P    0
30 > Pts  Normal  0   [24.8, 32.2] * P  [17, 21]* P   [9.4, 11.6] * P   0
20 > Pts  Mala    0   [32.2, 39.6] * P  [21, 25]* P   [11.6, 13.8] * P  0
8 > Pts   Pésima  0   [39.6, 47] * P    [25, 29]* P   [13.8, 16] * P    0
"""
LARVA_PUPA_ZONE = {
    "OPTIMA" : {
        "FRIO"     : [0],
        "FRESCO"   : [10.0, 17.4],
        "NORMAL"   : [9,  13],
        "CALIDO"   : [5.00, 7.20],
        "CALUROSO" : [0]
    },
    "BUENA"  : {
        "FRIO"     : [0],
        "FRESCO"   : [17.4, 24.8],
        "NORMAL"   : [13, 17],
        "CALIDO"   : [7.20, 9.40],
        "CALUROSO" : [0]
    },
    "NORMAL"  : {
        "FRIO"     : [0],
        "FRESCO"   : [24.8, 32.2],
        "NORMAL"   : [17, 21],
        "CALIDO"   : [9.40, 11.6],
        "CALUROSO" : [0]
    },
    "MALA"  : {
        "FRIO"     : [0],
        "FRESCO"   : [32.2, 39.6],
        "NORMAL"   : [21, 25],
        "CALIDO"   : [11.6, 13.8],
        "CALUROSO" : [0]
    },
    "PESIMA"  : {
        "FRIO"     : [0],
        "FRESCO"   : [39.6, 47.0],
        "NORMAL"   : [25, 29],
        "CALIDO"   : [13.8, 16.0],
        "CALUROSO" : [0]
    }
}

