#! /usr/bin/env python
# -*- coding: utf-8 -*-
import json
from config import *
from datatype import *
from random import randint
# para convertir horas
"""
@autors Maximiliano Báez
@contact mxbg.py@gmail.com
"""

class Dia:

    """
    Define los datos climáticos para una hora en especifico.
    """

    def __init__(self, data={}):
        self.hora = data.get("hora", 0)
        self.presion = data.get("presion", 0)
        self.precipitacion = data.get("precipitacion", 0)
        self.temperatura = data.get("temperatura", 0)
        self.humedad = data.get("humedad", 0)
        self.viento = data.get("viento", 0.0)
        self.direccion_viento = data.get("direccion_viento", 0.0)
        self.nuves = data.get("nuves", 0)

    def parse(self, data, temperatura, future):
        """
        Se encarga de parsear los datos obtenidos del openweathermap.org
        """
        if future == True:
            if temperatura == None:
                self.temperatura = float(data["temp"].get("day", 0))
                # de kelvin a centigrados
                self.temperatura = self.temperatura - 273.15
            else:
                self.temperatura = float(temperatura)

            self.presion = float(data.get("pressure", 0))
            self.humedad = float(data.get("humidity", 0))
            self.viento = float(data.get("speed", 0.0))
            self.precipitacion = float(data.get("rain", 0.0))
            self.direccion_viento = float(data.get('deg', 0))
            self._parse_datetime(data)

        elif future == False:
            self._parse_rain_node(data)
            self._parse_main_node(data)
            self._parse_wind_node(data)
            self._parse_clouds_node(data)
            self._parse_datetime(data)

        else:
            temp = data["temp"].get('v', 0)
            self.temperatura = float(temp) - 273.15
            self.presion = data["pressure"].get('v', 0)
            self.humedad = data["humidity"].get('v', 0)
            if not data.has_key("wind"):
                data["wind"]={"speed":{}, "deg":{}}

            self.viento = float(data["wind"]["speed"].get('v', randint(0,10)))
            self.direccion_viento = float(data["wind"]["deg"].get('v', randint(0,360)))
            self._parse_datetime(data)

    def _parse_rain_node(self, data):
        """
        rain         Precipitation volume for period
            1h   rain in recent hour
            3h   rain in recent 3 hours
            6h   rain in recent 6 hours
            12h  rain in recent 12 hours
            24h  rain in recent 24 hours
            day  rain in recent day
        """
        attrs = ["1h", "3h", "6h", "12h", "24h", "day"]
        if data.has_key("rain"):
            for attr in attrs:
                if data["rain"].has_key(attr):
                    self.precipitacion = data["rain"][attr]
                    return

        self.precipitacion = 0

    def _parse_main_node(self, data):
        """
        main     temp    Temperature in Kelvin. Subtracted 273.15 from
                         this figure to convert to Celsius.
        main     humidity    Humidity in %
        main     temp_min temp_max   Minimum and maximum temperature
        main     pressure    Atmospheric pressure in kPa
        """
        if data.has_key("main"):
            # se transforma los grados Kelvin a celcius.
            temp = data["main"].get('temp', 0)
            self.temperatura = float(temp) - 273.15
            self.presion = float(data["main"].get('pressure', 0))
            self.humedad = float(data["main"].get('humidity', 0))


    def _parse_wind_node(self, data):
        """
        wind         Wind
            speed    Wind speed in mps ( m/s )
            deg  Wind direction in degrees ( meteorological)
            gust     speed of wind gust
            var_beg  Wind direction
            var_end  Wind direction
        """
        if data.has_key("wind"):
            self.viento = float(data["wind"].get('speed', 0))
            self.direccion_viento = float(data["wind"].get('deg', 0))
        else:
            self.viento = 0.0
            self.direccion_viento = 0.0

    def _parse_clouds_node(self, data):
        if data.has_key("clouds"):
            self.nuves = float(data["clouds"].get('all', 0))
        else:
            self.nuves = 0.0
            self.direccion_viento = 0.0

    def get_tipo_clima(self):
        """
        Se encarga de clasificar el clima en alguna de las siguientes
        categorias :
        T < 15  15 < T <20   20 < T < 25    25 < T < 36  T > 36
        Frio    Fresco       Normal          Cálido      Caluroso
        """
        if self.temperatura < 15:
            return Clima.FRIO

        elif self.temperatura >= 15 and self.temperatura < 20:
            return Clima.FRESCO

        elif self.temperatura >= 20 and self.temperatura < 25:
            return Clima.NORMAL

        elif self.temperatura >= 25 and self.temperatura < 36:
            return Clima.CALIDO

        elif self.temperatura >= 36:
            return Clima.CALUROSO

    def get_tipo_hora(self):
        """
        """
        if self.hora >= 20:
            return Horario.NOCHE

        elif self.hora >= 18 and self.hora < 20:
            return Horario.TARDE_NOCHE

        elif self.hora >= 14 and self.hora < 18:
            return Horario.TARDE

        elif self.hora >= 9 and self.hora < 14:
            return Horario.MANHANA

        elif self.hora >= 5 and self.hora < 9:
            return Horario.MADUGRADA_MANHANA

        elif self.hora >= 0 and self.hora < 5:
            return Horario.MADUGRADA

    def _parse_datetime(self, data):
        """
        Convierte el timestamp obtenido del json a formato hh (hora)
        """
        from datetime import datetime

        dt = datetime.fromtimestamp(float(data.get('dt', 0)))
        self.hora = dt.strftime('%d/%m/%Y %H:%M')
        self.dt = float(data.get('dt', 0))

    def __str__(self):
        return  str(self.dt)+ " "+\
           str(self.hora) + "hs " + \
           str(self.temperatura) + " C " + \
           str(self.viento ) + " m/s " + \
           str(self.direccion_viento) + " *"


class Periodo:

    """
    Esta clase define los datos climáticos en un periodo de tiempo por
    hora.
    """

    def __init__(self):
        self.dias = []

    def parse_json(self, data, temperatura, future=False):
        """
        Se encarga de procesar los datos en forma de json y los añade a
        la lista.
        """
        for day in data["list"]:
            d = Dia()
            d.parse(day, temperatura, future)
            self.dias.append(d)


import lxml.html
import urllib2
import time
import datetime


class TuTiempo:

    """
    Se encarga de obtner los datos climaticos, por hora, de 2 fuentes
    teniendo en cuenta al tiempo al cual el periodo del cual se necesitan
    los datos.

    Datos Historicos : se obtienen utilizando OpenWeatherMap
    Predicción a 15 días : se obtienen parseando los datos del sitio de
    TuTiempo.
    """
    @property
    def grados(self):
        """
        Se encarga de inicializar el diccionario que mapea los strings a
        grados según la tabla definida en http://www.windfinder.com/wind/windspeed.htm
        """
        grados_dict = {}
        grados_dict["norte"] = 0.0
        grados_dict["nornordeste"] = 22.5
        grados_dict["nordeste"] = 45.0
        grados_dict["estenoreste"] = 67.5
        grados_dict["este"] = 90.0
        grados_dict["estesureste"] = 112.5
        grados_dict["sureste"] = 135.0
        grados_dict["sursureste"] = 157.5
        grados_dict["sur"] = 180.0
        grados_dict["sursuroeste"] = 202.5
        grados_dict["suroeste"] = 225.0
        grados_dict["oestesuroeste"] = 247.5
        grados_dict["oeste"] = 270.0
        grados_dict["oestenoroeste"] = 292.5
        grados_dict["noroeste"] = 315.0
        grados_dict["nornordoeste"] = 337.5
        return grados_dict

    def __init__(self,  localidad):
        pass

    def get_periodo(self, temperatura=None):
        """
        Se ecarga de obtener los datos historicos y predictos de la
        localidad.
        """
        periodo = Periodo()
        periodo.parse_json(self.history(),temperatura, None);
        #periodo.parse_json(self.history(),temperatura, None)
        #periodo.parse_json(self.future(), temperatura, True)
        return periodo

    def download_page(self, domain):
        """
        Descarga el hmtl de la página en forma de string.
        """
        url = domain
        print domain
        usock = urllib2.urlopen(url)
        data = usock.read()
        usock.close()
        return data

    def build_url_params(self, args={}):
        """
        Se encarga de construir el query string para la url.
        """
        params = "?"
        for key in API_DATA:
            if not args.has_key(key) :
                params += key + "=" + API_DATA[key] + "&"

        for key in args:
            params += key + "=" + args[key] + "&"
        return params

    def history(self):
        """
        Obtiene el historial del clima por hora utilizando los servicios
        de openweathermap, el servicio responde con el siguiente JSON:
        <pre>
        {   "message": "",
            "cod": "200",
            "city_id": 3439389,
            "calctime": 0.0032,
            "cnt": 13,
            "list": [{
                    "weather": [{
                            "id": 800,
                            "main": "Clear",
                            "description": "Sky is Clear",
                            "icon": "01n"
                    }],
                    "base": "global stations",
                    "main": {
                        "temp": 289.15,
                        "pressure": 1020,
                        "humidity": 59,
                        "temp_min": 289.15,
                        "temp_max": 289.15
                    },
                    "wind": {
                        "speed": 4.6,
                        "deg": 80
                    },
                    "clouds": {
                        "all": 0
                    },
                    "city": {
                        "zoom": 5,
                        "country": "PY",
                        "population": 1000000,
                        "find": [
                            "ASUNCION"
                        ],
                        "id": 3439389,
                        "name": "Asuncion"
                    },
                    "dt": 1374973200
                }, ...
            ]
        }
        </pre>
        """
        # se calcula el rango de fechas
        now = datetime.datetime.now()
        # se crea una fecha de 10 dias antes a modo de prueba
        delta = datetime.timedelta(days=60)
        past = now - delta
        #delta = datetime.timedelta(days=100)
        #now = now - delta
        # se  transforma a unix time
        end = str(int(time.mktime(now.timetuple())))
        start = str(int(time.mktime(past.timetuple())))

        args = {
            "start": start,  # 2013/03/11
            "end": end  # 2013/03/31
        }

        #url = API_URL + "/history/city" + self.build_url_params(args);
        #url = API_URL + "/history/station" + self.build_url_params(args);
        url = API_URL + ".history.json"
        json_string = self.download_page(url)
        return json.loads(json_string)

    def future(self):
        """
        Obtiene los datos futros del clima por hora utilizando los servicios
        de openweathermap, el servicio responde con el siguiente JSON:
        <pre>
        {
            "cod": "200",
            "message": 0.0013,
            "city": {
                "id": 3439389,
                "name": "Asuncion",
                "coord": {
                    "lon": -57.63591,
                    "lat": -25.300659
                },
                "country": "PY",
                "population": 1000000
            },
            "cnt": 15,
            "list": [
                {
                    "dt": 1396710000,
                    "temp": {
                        "day": 306.95,
                        "min": 300.25,
                        "max": 306.95,
                        "night": 300.25,
                        "eve": 305.79,
                        "morn": 306.95
                    },
                    "pressure": 1016.99,
                    "humidity": 46,
                    "weather": [
                        {
                            "id": 802,
                            "main": "Clouds",
                            "description": "scattered clouds",
                            "icon": "03d"
                        }
                    ],
                    "speed": 5.2,
                    "deg": 38,
                    "clouds": 36
                },
            ..]
        }
        </pre>
        """
        args = {
            "cnt": "15",
            "id": "3439389"
        }
        #url = API_URL + "/forecast/daily" + self.build_url_params(args);
        url = API_URL + ".forecast.15.json"
        json_string = self.download_page(url)
        return json.loads(json_string)

if __name__ == "__main__":
    clima = TuTiempo("Asuncion")
    #~ clima.process_dom_hora();
    periodo = clima.get_periodo()
    cnt = 0
    t_med=0
    for h in periodo.dias:
        print h
        t_med += h.temperatura
        cnt +=1

    med = t_med/cnt
    print str(cnt) +" : "+ str(med)
