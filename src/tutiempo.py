#! /usr/bin/env python
# -*- coding: utf-8 -*-

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
API_URL = "http://api.openweathermap.org/data/2.5";
TUTIEMPO_URL = 'http://www.tutiempo.net/'

import json    # or `import simplejson as json` if on Python < 2.6

class Dia :

    def __init__( self, data={}):
        if len(data) >= 6:
            self.hora = data["hora"]
            self.presion = None
            self.precipitacion = data["precipitacion"]
            self.temperatura = data["temperatura"]
            self.humedad = data["humedad"]
            self.viento = data["viento"]
            self.nuves = data["nuves"]

    def parse( self, data):
        self.precipitacion = data["rain"]["3h"]
        self.temperatura = data["main"]["temp"]
        self.presion = data["main"]["pressure"]
        self.humedad = data["main"]["humidity"]
        self.viento = data["wind"]["speed"]
        self.nuves = data["clouds"]["all"]

class Periodo :
    def __init__( self):
        self.horas = []

    def parse_json(self, data) :
        for day in data["list"] :
            d = Dia()
            d.parse(day)
            self.horas.append(d)


    def parse_dic(self , data) :
        for day in data :
            self.horas.append(Dia(day))



import lxml.html
import urllib2
import time
import datetime

class TuTiempo:

    def __init__(self,  localidad, fecha):
        self.localidad_hora = TUTIEMPO_URL +LOCALIDADES_HORA[localidad]

    def download_page(self, domain) :
        """
        Descarga el hmtl de la página en forma de string.
        """
        url =  domain
        print url
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
            'prob': 'nuves'
        }
        day = -1
        tr_els = []
        i = 0
        for elem in root.cssselect('div.DatosHorarios table'):
            for tr in elem.cssselect('tr'):

                for td in tr.cssselect('th') :
                    val = td.text_content()
                    key = td.attrib["class"]
                    if key == "Dia" :
                        day += 1
                        tr_els.insert(day,[])
                        i = 0

                tr_els[day].insert(i,{})

                for td in tr.cssselect('td') :
                    val = td.text_content()
                    key = td.attrib["class"]
                    if attributes.has_key(key) :
                        attr = attributes[key]
                        tr_els[day][i][attr] = val.encode("utf-8").strip()

                # se verifica si se añadieron elementos al array para
                # incrementar el array.
                if len(tr_els[day][i]) > 0 :
                    i += 1
                else :
                    tr_els[day].pop(i)

        for i in range(len(tr_els) ):
            print str(i) +" : "+ str(len(tr_els[i]))

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
        past = datetime.datetime(year=now.year,month=now.month,day=now.day -10)
        # se  transforma a unix time
        end = str(int(time.mktime(now.timetuple())))
        start = str(int(time.mktime(past.timetuple())))

        args ={
            "start" : start,
            "end" : end,
        }

        url = API_URL + "/history/city" + self.build_url_params(args);
        json_string = self.download_page(url);
        return json.loads(json_string)


if __name__ == "__main__":
    clima = TuTiempo("Asuncion", "07-2013")
    #~ clima.process_dom_hora();
    periodo = Periodo()
    periodo.parse_json(clima.history());
    print periodo.horas
