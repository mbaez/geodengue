#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Configuraciones para la conexión con la base de datos
"""
DB = {
    "dbname": "dengue",
    "host": "localhost",
    "port": "5432",
    "user": "postgres",
    "password": "postgres"
}

TMP_HOME = "./data/"
RASTER = {
    "schema": "public",
    "table": "tabla",
    "srid": "900913",
    "pk": "id"
}

"""
Configuraciones para la conexión con el geoserver.
"""
GEOSERVER = {
    "host": "localhost",
    "port": "8080",
    "user": "admin",
    "password": "admin",
    "workspace": "geodengue"
}

"""
Configuraciones de los servicios de datos climáticos
"""
#~ URL = 'http://www.tutiempo.net/tiempo/Asuncion_Aeropuerto/SGAS.htm?datos=por-horas'
LOCALIDADES_HORA = {
    "Asuncion": ''
    #~ "Asuncion" : 'tiempo/Asuncion_Aeropuerto/SGAS.htm?datos=por-horas'
}
# Datos utilizads para contruir los queryparams para realizar el get
API_DATA = {
    #~ "appid" : "2d9be00662629ff5c269672af48013d8",
    #~ "type" : "day",
    "id": "3439389"
    #~ "mode" : "json"
}
# URLs de las fuentes de información de datos climaticos
#~ API_URL = "http://api.openweathermap.org/data/2.5";
API_URL = "http://localhost/geodengue/api.openweathermap.30-dias"
#~ TUTIEMPO_URL = "http://localhost/geodengue/tutiempo.dom";
#~ TUTIEMPO_URL = 'http://www.tutiempo.net/'

"""
Configuraciones de las Zonas
"""
#~ El tamaño esta a un radio de 200 metros de la del punto de origen
TAMANHO_ZONA = 400
#~ la cantidad máxima de huevos que puede poner un indiviudo de una vez
MAX_HUEVOS = 150
#~ cantidad de alimento que debe ingerir el individuo hasta estar satisfecho
MAX_ALIMENTACION = 30
MIN_VUELO = 100
MAX_VUELO = 30000
#~ Porcentaje de las etapas inmaduras que abarca cada fase
TIEMPO_PUPA = 0.26
TIEMPO_LARVA = 0.74
SELECCION_NATURAL = 0.9

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
    "OPTIMA": {
        "FRIO": [0],
        "FRESCO": [10.0, 17.4],
        "NORMAL": [9,  13],
        "CALIDO": [5.00, 7.20],
        "CALUROSO": [0]
    },
    "BUENA": {
        "FRIO": [0],
        "FRESCO": [17.4, 24.8],
        "NORMAL": [13, 17],
        "CALIDO": [7.20, 9.40],
        "CALUROSO": [0]
    },
    "NORMAL": {
        "FRIO": [0],
        "FRESCO": [24.8, 32.2],
        "NORMAL": [17, 21],
        "CALIDO": [9.40, 11.6],
        "CALUROSO": [0]
    },
    "MALA": {
        "FRIO": [0],
        "FRESCO": [32.2, 39.6],
        "NORMAL": [21, 25],
        "CALIDO": [11.6, 13.8],
        "CALUROSO": [0]
    },
    "PESIMA": {
        "FRIO": [0],
        "FRESCO": [39.6, 47.0],
        "NORMAL": [25, 29],
        "CALIDO": [13.8, 16.0],
        "CALUROSO": [0]
    }
}

"""
Tabla de adultos

60 < P  Optima  [1, 3]  [15,20] [15,30] [20,30] 1
60 > P  Buena   [1, 3]  [15,20] [15,30] [20,30] 1
30 > P  Normal  [1, 3]  [15,20] [15,30] [20,30] 1
20 > P  Mala    [1, 3]  [15,20] [15,30] [20,30] 1
8 > P   Pésima  [1, 3]  [15,20] [15,30] [20,30] 1
"""
ADULTO__EXPECTATIVA = {
    "OPTIMA": {
        "FRIO": [1, 3],
        "FRESCO": [5, 15],
        "NORMAL": [5, 20],
        "CALIDO": [5, 30],
        "CALUROSO": [1]
    },
    "BUENA": {
        "FRIO": [1, 3],
        "FRESCO": [5, 15],
        "NORMAL": [5, 20],
        "CALIDO": [5, 30],
        "CALUROSO": [1]
    },
    "NORMAL": {
        "FRIO": [1, 3],
        "FRESCO": [5, 15],
        "NORMAL": [5, 20],
        "CALIDO": [5, 30],
        "CALUROSO": [1]
    },
    "MALA": {
        "FRIO": [1, 3],
        "FRESCO": [5, 15],
        "NORMAL": [5, 20],
        "CALIDO": [5, 30],
        "CALUROSO": [1]
    },
    "PESIMA": {
        "FRIO": [1, 3],
        "FRESCO": [5, 15],
        "NORMAL": [5, 20],
        "CALIDO": [5, 30],
        "CALUROSO": [1]
    }
}

"""
Tabla de expectativa de vida de las larvas y pupas

        T<15    15<T<20     20<T<25     25<T<36    T>36
        Frio    Fresco      Normal      Cálido      Caluroso
Optima  [1,42]  [3,39]      [3,28]      [4,16]      [2,7]
Buena   [1,42]  [3,39]      [3,28]      [4,16]      [2,7]
Normal  [1,42]  [3,39]      [3,28]      [4,16]      [2,7]
Mala    [1,42]  [3,39]      [3,28]      [4,16]      [2,7]
Pesima  [1,42]  [3,39]      [3,28]      [4,16]      [2,7]
        p=100   p= 60       p=23        P= 68       p= 100
"""
__LARVA_PUPA_EXPECTATIVA = {
    "OPTIMA": {
        "FRIO": [33.8, 42],
        "FRESCO": [31.8, 39],
        "NORMAL": [23, 28],
        "CALIDO": [13.6, 16],
        "CALUROSO": [6, 7]
    },
    "BUENA": {
        "FRIO": [25.6, 33.8],
        "FRESCO": [24.6, 31.8],
        "NORMAL": [18, 23],
        "CALIDO": [11.2, 13.6],
        "CALUROSO": [5, 6]
    },
    "NORMAL": {
        "FRIO": [17.4, 25.6],
        "FRESCO": [17.4, 24.6],
        "NORMAL": [13, 18],
        "CALIDO": [8.8, 11.2],
        "CALUROSO": [4, 5]
    },
    "MALA": {
        "FRIO": [9.2, 17.4],
        "FRESCO": [10.2, 17.4],
        "NORMAL": [8, 13],
        "CALIDO": [6.4, 8.8],
        "CALUROSO": [3, 4]
    },
    "PESIMA": {
        "FRIO": [1, 9.2],
        "FRESCO": [3, 10.2],
        "NORMAL": [3, 8],
        "CALIDO": [4, 6.4],
        "CALUROSO": [2, 3]
    }
}

"""
Tabla de expectativa de vida de las larvas y pupas

        T<15        15<T<20     20<T<25     25<T<36     T > 36
        Frio        Fresco      Normal      Cálido      Caluroso
Optima  2.6,21.8    23.6,26.5   15,23.6     8,16        2.6, 7.2
Buena   2.6,21.8    23.6,26.5   15,23.6     8,16        2.6, 7.2
Normal  2.6,21.8    23.6,26.5   15,23.6     8,16        2.6, 7.2
Mala    2.6,21.8    23.6,26.5   15,23.6     8,16        2.6, 7.2
Pesima  2.6,21.8    23.6,26.5   15,23.6     8,16        2.6, 7.2
"""
LARVA_PUPA_EXPECTATIVA = {
    "OPTIMA": {
        "FRIO": [2.6, 21.8],
        "FRESCO": [23.6, 26.5],
        "NORMAL": [15.0, 23.6],
        "CALIDO": [8.0, 16.0],
        "CALUROSO": [2.6, 7.2]
    },
    "BUENA": {
        "FRIO": [2.6, 17.96],
        "FRESCO": [23.6, 25.92],
        "NORMAL": [15.0, 21.88],
        "CALIDO": [8.0, 16.0],
        "CALUROSO": [2.6, 6.28]
    },
    "NORMAL": {
        "FRIO": [2.6, 14.12],
        "FRESCO": [23.6, 25.34],
        "NORMAL": [15.0, 20.16],
        "CALIDO": [8.0, 14.4],
        "CALUROSO": [2.6, 5.36]
    },
    "MALA": {
        "FRIO": [2.6, 10.28],
        "FRESCO": [23.6, 24.76],
        "NORMAL": [15.0, 18.44],
        "CALIDO": [8.0, 11.2],
        "CALUROSO": [2.6, 4.44]
    },
    "PESIMA": {
        "FRIO": [2.6, 6.44],
        "FRESCO": [23.6, 24.18],
        "NORMAL": [15.0, 16.72],
        "CALIDO": [8.0, 9.6],
        "CALUROSO": [2.6, 3.52]
    }
}


CICLO_GONOTROFICO = {
    "FRIO": [96, 120],
    "FRESCO": [72, 96],
    "NORMAL": [48, 96],
    "CALIDO": [48, 72],
    "CALUROSO": [48, 72]
}
