#! /usr/bin/env python
# -*- coding: utf-8 -*-

LOCALIDADES_HORA ={
    "Asuncion" : 'tiempo/Asuncion_Aeropuerto/SGAS.htm?datos=por-horas'
}

LOCALIDADES_DIA = {
    "Asuncion": 'clima/Asuncion_Aeropuerto/mm-yyyy/862180.htm'
}

#~ URL = 'http://www.tutiempo.net/tiempo/Asuncion_Aeropuerto/SGAS.htm?datos=por-horas'
#~ URL =  'http://www.tutiempo.net/Asuncion_Aeropuerto/SGAS.htm?datos=por-horas'

import lxml.html
import urllib2

class TuTiempo:
    URL_BASE = 'http://www.tutiempo.net/'

    def __init__(self,  localidad, fecha):
        print localidad
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
        root = self.get_dom(self.localidad_hora)
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



if __name__ == "__main__":
    clima = TuTiempo("Asuncion", "07-2013")
    clima.process_dom_dia();
    clima.process_dom_hora();
