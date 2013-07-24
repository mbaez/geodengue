#! /usr/bin/env python
# -*- coding: utf-8 -*-

#~ http://espanol.weather.com/weather/almanacHourly-Asuncion-PAXX0001:1:PA?day=N
#~ Se traen los datos de N días antes de la fecha actual
#~ Se pueden obtener datos de años pasados por hora
#~ No trae datos de las precipitaciones, se debe complementar con datos
#~ de tutiempo

LOCALIDADES_HORA ={
    #~ "Asuncion" : 'tiempo/Asuncion_Aeropuerto/SGAS.htm?datos=por-horas'
    "Asuncion" : 'asuncion.html'
}

LOCALIDADES_DIA = {
    "Asuncion": 'clima/Asuncion_Aeropuerto/mm-yyyy/862180.htm'
}

#~ URL = 'http://www.tutiempo.net/tiempo/Asuncion_Aeropuerto/SGAS.htm?datos=por-horas'
#~ URL =  'http://www.tutiempo.net/Asuncion_Aeropuerto/SGAS.htm?datos=por-horas'

class Tiempo :
    """
    T Temperatura media (°C)
    TM Temperatura máxima (°C)
    Tm Temperatura mínima (°C)
    SLP Presión atmosférica a nivel del mar (hPa)
    H Humedad relativa media (%)
    PP Precipitación total de lluvia y/o nieve derretida (mm)
    VV Visibilidad media (Km)
    V Velocidad media del viento (Km/h)
    VM Velocidad máxima sostenida del viento (Km/h)
    VG Velocidad de ráfagas máximas de viento (Km/h)
    RA Índica si hubo lluvia o llovizna (En la media mensual, total días que llovió)
    SN Índica si nevó (En la media mensual, total días que nevó)
    TS Indica si hubo tormenta (En la media mensual, total días con tormenta)
    FG Indica si hubo niebla (En la media mensual, total días con niebla)
    """
    def __init__ (self):
        self.temp_med = 0
        self.temp_max = 0
        self.temp_min = 0
        self.presion_atm = 0
        self.humedad_rel = 0
        self.presipitacion = 0
        self.visibilidad = 0
        self.vel_med = 0
        self.vel_max = 0
        self.vel_rafaga = 0
        self.lluvia = False
        self.nieve = False
        self.tormenta= False
        self.niebla= False




import lxml.html
import urllib2

class TuTiempo:
    """
    Esta clase se encarga de otener los datos climáticos de la página
    www.tutiempo.net
    """
    URL_BASE = 'http://www.tutiempo.net/'

    def __init__(self,  localidad, fecha):
        self.localidad_hora = LOCALIDADES_HORA[localidad]
        self.localidad_dia = LOCALIDADES_DIA[localidad].replace('mm-yyyy', fecha);


    def download_page(self, domain) :
        """
        Descarga el hmtl de la página en forma de string.
        """
        url = TuTiempo.URL_BASE + domain
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
        Procesa el dom de la página de clima por hora
        """
        root = self.get_dom(self.localidad_hora + "?datos=por-horas")
        tr_els = []
        i=0
        for elem in root.cssselect('div.DatosHorarios table'):
            for tr in elem.cssselect('tr'):
                tr_els.insert(i,{});
                for td in tr.cssselect('th'):
                    val = td.text_content()
                    attr = td.attrib["class"]
                    tr_els[i][attr] = val;

                for td in tr.cssselect('td'):
                    val = td.text_content()
                    attr = td.attrib["class"]
                    tr_els[i][attr] = val;
                i+=1

        for i in range(len(tr_els) ):
            print str(tr_els[i])

    def process_dom_dia (self) :
        """
        Procesa el dom de la página de clima por día
        """
        root = self.get_dom(self.localidad_dia)
        tr_els = []
        i=0
        for elem in root.cssselect('table.TablaClima'):
            for tr in elem.cssselect('tr'):
                tr_els.insert(i,[]);
                for td in tr.cssselect('td'):
                    value = 0
                    #se verifica que el elemento sea numerico
                    val = td.text_content()
                    val = unicode(val)
                    if val.isnumeric() :
                        value = float(val)
                    #se añade el elemento al array
                    tr_els[i].append(value);
                i+=1

        for i in range(len(tr_els) ):
            for j in range(len(tr_els[i])):
                print str(tr_els[i][j]) + "\t",
            print "\n"

    def process_dom_dia_15(self):
        """
        Procesa el dom de la página de clima por día
        """
        root = self.get_dom(self.localidad_hora+"?datos=detallados")
        tr_els = []
        i=0
        for elem in root.cssselect('#Pronostico15Dias tbody'):
            tr = elem.cssselect('tr')
            tr_els.insert(0,[]);
            tr_els.insert(1,[]);

            for td in tr[0].cssselect('td'):
                #~ value = 0
                #se verifica que el elemento sea numerico
                val = td.text_content()
                if td.attrib.has_key("class") :
                    attr = td.attrib["class"]
                    if attr == "TMax" or attr == "TMin" :
                        #se añade el elemento al array
                        print val

            for td in tr[1].cssselect('td'):
                #se verifica que el elemento sea numerico
                if not td.attrib.has_key("class") :
                    val = td.text_content()
                    #se añade el elemento al array
                    #~ if val != "-" :
                    print val
            i+=1

        for i in range(len(tr_els) ):
            for j in range(len(tr_els[i])):
                print str(tr_els[i][j]) + "\t",
            print "\n"



if __name__ == "__main__":
    clima = TuTiempo("Asuncion", "07-2013")
    clima.process_dom_dia_15();
    #~ clima.process_dom_dia();
    #~ clima.process_dom_hora();
