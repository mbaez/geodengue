#! /usr/bin/env python
# -*- coding: utf-8 -*-
import json
from config import *
from datatype import *

#para convertir horas


class Hora :

    """
    Define los datos climáticos para una hora en especifico.
    """
    def __init__( self, data={}):
        self.hora = data.get("hora", 0)
        self.presion = data.get("presion", 0)
        self.precipitacion = data.get("precipitacion", 0 )
        self.temperatura = data.get("temperatura",0)
        self.humedad = data.get("humedad",0)
        self.viento = data.get("viento", 0.0)
        self.direccion_viento = data.get("direccion_viento",0.0)
        self.nuves = data.get("nuves", 0)

    def parse( self, data):
        """
        Se encarga de parsear los datos obtenidos del openweathermap.org
        """
        self._parse_rain_node(data)
        self._parse_main_node(data)
        self._parse_wind_node(data)
        self._parse_clouds_node(data)
        self._parse_datetime(data)

    def _parse_rain_node (self, data) :
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
        if data.has_key("rain") :
            for attr in attrs :
                if data["rain"].has_key(attr) :
                   self.precipitacion = data["rain"][attr]
                   return

        self.precipitacion = 0

    def _parse_main_node (self, data) :
        """
        main     temp    Temperature in Kelvin. Subtracted 273.15 from
                         this figure to convert to Celsius.
        main     humidity    Humidity in %
        main     temp_min temp_max   Minimum and maximum temperature
        main     pressure    Atmospheric pressure in kPa
        """
        if data.has_key("main") :
            # se transforma los grados Kelvin a celcius.
            temp = data["main"].get('temp', 0)
            self.temperatura = float(temp) - 273.15
            self.presion = float(data["main"].get('pressure', 0))
            self.humedad = float(data["main"].get('humidity', 0))

    def _parse_wind_node (self, data) :
        """
        wind         Wind
            speed    Wind speed in mps ( m/s )
            deg  Wind direction in degrees ( meteorological)
            gust     speed of wind gust
            var_beg  Wind direction
            var_end  Wind direction
        """
        if data.has_key("wind") :
            self.viento = float(data["wind"].get('speed', 0))
            self.direccion_viento = float(data["wind"].get('deg', 0))
        else :
            self.viento = 0.0
            self.direccion_viento = 0.0

    def _parse_clouds_node (self, data) :
        if data.has_key("clouds") :
            self.nuves = float(data["clouds"].get('all', 0))
        else :
            self.nuves = 0.0
            self.direccion_viento = 0.0

    def get_tipo_clima (self):
        """
        Se encarga de clasificar el clima en alguna de las siguientes
        categorias :
        T < 15  15 < T <20   20 < T < 25    25 < T < 36  T > 36
        Frio    Fresco       Normal          Cálido      Caluroso
        """
        if self.temperatura  < 15 :
            return Clima.FRIO

        elif self.temperatura  >= 15 and self.temperatura  < 20 :
            return Clima.FRESCO

        elif self.temperatura  >= 20 and self.temperatura  < 25 :
            return Clima.NORMAL

        elif self.temperatura  >= 25 and self.temperatura  < 36 :
            return Clima.CALIDO

        elif self.temperatura  >= 36 :
            return Clima.CALUROSO

    def _parse_datetime( self, data ) :
        """
        Convierte el timestamp obtenido del json a formato hh (hora)
        """
        from datetime import datetime

        dt = datetime.fromtimestamp(float(data.get('dt',0)))
        self.hora = dt.strftime('%H')

    def __str__(self) :
        return str(self.hora) + "hs " + \
        str(self.precipitacion) + " " + \
        str(self.temperatura) + "¤C " + \
        str(self.humedad) + " " + \
        str(self.viento ) + " " + \
        str(self.direccion_viento) + " "

class Periodo :
    """
    Esta clase define los datos climáticos en un periodo de tiempo por
    hora.
    """
    def __init__( self):
        self.horas = []

    def parse_json(self, data) :
        """
        Se encarga de procesar los datos en forma de json y los añade a
        la lista.
        """
        for day in data["list"] :
            d = Hora()
            d.parse(day)
            self.horas.append(d)

    def parse_dict(self , data) :
        """
        Se encarga de procesar los datos en forma de diccionarios y los
        añade a la lista.
        """
        for day in data :
            for hour in day :
                self.horas.append(Hora(hour))



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
    def grados(self) :
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
        self.localidad_hora = TUTIEMPO_URL +LOCALIDADES_HORA[localidad]

    def get_periodo (self) :
        """
        Se ecarga de obtener los datos historicos y predictos de la
        localidad.
        """
        periodo = Periodo()
        periodo.parse_json(self.history());
        #~ periodo.parse_dict(self.process_dom_hora());
        return periodo

    def download_page(self, domain) :
        """
        Descarga el hmtl de la página en forma de string.
        """
        url =  domain
        print domain
        usock = urllib2.urlopen(url)
        data = usock.read()
        usock.close()
        return data

    def get_dom (self, domain):
        """
        Procesa el html_string, y genera el dom de la pagina
        """
        html_page = self.download_page(domain)
        return lxml.html.fromstring(html_page)

    def process_dom_hora (self) :
        """
        Procesa el dom de la página de clima por hora.
        0 Hora : "hh:mm"
        1 Predicción : imagen
        2 Temp : N°C
        3 Viento : imagen N km/h
        4 H : N%
        5 Nubes : N%
        6 Precip : N mm
        """
        root = self.get_dom(self.localidad_hora)

        attributes = {
            'hora':'hora',
            'pp': 'precipitacion',
            'Temp': 'temperatura',
            'hr': 'humedad',
            'vv': 'viento',
            'IcoViento' : 'direccion_viento',
            'prob': 'nuves'
        }
        day = -1
        tr_els = []
        i = 0
        for elem in root.cssselect('div.DatosHorarios table'):
            for tr in elem.cssselect('tr'):
                #~ se encarga de procesar los headers para saber si los
                #~ datos corresponden a otro día
                for td in tr.cssselect('th') :
                    val = td.text_content()
                    key = td.attrib["class"]
                    if key == "Dia" :
                        day += 1
                        tr_els.insert(day,[])
                        i = 0

                tr_els[day].insert(i,{})

                #~  se procesan los datos
                for td in tr.cssselect('td') :
                    val = td.text_content()
                    key = td.attrib["class"]
                    if attributes.has_key(key) :
                        attr = attributes[key]
                        value = val.encode("utf-8").strip()
                        #~ se procesa los datos de forma especial
                        if attr == attributes["Temp"] :
                            value = value.replace("°C","").strip()
                            value = float(value)
                        elif attr == attributes["IcoViento"] :
                            value = self.__dom_direccion_viento(td)

                        tr_els[day][i][attr] = value

                # se verifica si se añadieron elementos al array para
                # incrementar el array.
                if len(tr_els[day][i]) > 0 :
                    i += 1
                else :
                    tr_els[day].pop(i)

        return tr_els

    def __dom_direccion_viento(self, dom) :
        """
        Se encarga de extraer la dirección del viento del atributo
        alt de tag img y mapear la dirección a grados.
        """
        img = dom.cssselect('img')[0]
        alt = img.attrib['alt']
        key = alt.split(" ")[0].lower();
        return self.grados.get(key, 0)

    def build_url_params (self, args={}):
        """
        Se encarga de construir el query string para la url.
        """
        params = "?"
        for key in API_DATA :
            params += key + "="+ API_DATA[key] + "&"

        for key in args:
            params += key + "="+ args[key] + "&"
        return params

    def history (self) :
        """
        Obtiene el historial del clima por hora utilizando los servicios
        de openweathermap, el servicio respondecon el siguiente JSON:
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
        delta = datetime.timedelta(days=150)
        delta2 = datetime.timedelta(days=170)
        now2 = now - delta;
        past = now - delta2;
        # se  transforma a unix time
        end = str(int(time.mktime(now2.timetuple())))
        start = str(int(time.mktime(past.timetuple())))

        args ={
            "start" : "1362973402", # 2013/03/11
            "end" : "1364705002", #2013/03/31
        }

        #~ url = API_URL + "/history/city" + self.build_url_params(args);
        url = API_URL;
        json_string = self.download_page(url);
        return json.loads(json_string)


if __name__ == "__main__":
    clima = TuTiempo("Asuncion")
    #~ clima.process_dom_hora();
    periodo = clima.get_periodo()
    print periodo.horas
