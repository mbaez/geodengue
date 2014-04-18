#! /usr/bin/env python
# -*- coding: utf-8 -*-
import httplib
import urllib
import urllib2
import base64
import time
import os
from config import *
from db_manager import MuestraModel

import datetime


class Geoserver:

    @property
    def rest_path(self):
        return "/geoserver/rest/workspaces/" + GEOSERVER["workspace"]

    @property
    def coverage_path(self):
        return self.rest_path + "/coveragestores.json"

    @property
    def layer_path(self):
        return self.rest_path + "/coveragestores/"

    def create_coverage_store(self, name):
        """
        Este método se encarga de crear el store para la capa raster.
        """
        ts = int(time.time())

        tmpl = {
            "coverageStore": {
                "name": "",
                "type": "ArcGrid",
                "enabled": "true",
                "url": ""
            }
        }
        # se construyen los atributos
        file_url = "file:coverages/geodengue/{0}.asc".format(name)
        # se setan los atributos
        tmpl["coverageStore"]["name"] = name
        tmpl["coverageStore"]["url"] = file_url
        # se realiza el post para crear el workspace
        self.make_request(self.coverage_path, str(tmpl))
        return name

    def gen_layer_name(self, args):
        """
        Se encarga de genear el nombre del layer
        @param args: Parametros utilizados para la generación de layers

        @keyword tipo: El tipo de layer a genear (inst|evol)
        @keyword id_muestra: El identificador de la muestra de origen
        """
        dao = MuestraModel()
        muestra = dao.get_by(args['id_muestra'])
        # se setea la fecha de inicio
        args["inicio"] = muestra[0]['fecha']
        args["fin"] = datetime.date.today()
        # se construye el template del layer
        layer_name = "raster_{tipo}_{id_muestra}_{inicio}_{fin}"
        return layer_name.format(**args)

    def make_request(self, path, data, method="POST"):
        """
        Esta función realiza un post para persistir el json
        """
        username = GEOSERVER["user"]
        password = GEOSERVER["password"]

        headers = {
            'Authorization': b'Basic ' + base64.b64encode(username + b':' + password),
            'Content-type': b'application/json'
        }

        host = GEOSERVER["host"] + ":" + GEOSERVER["port"]
        conn = httplib.HTTPConnection(host)
        req = conn.request(method, path, data, headers)

        response = conn.getresponse()
        self.print_result(response, method)
        conn.close()

    def publish_coverage(self, store_name):
        """
        Esta función realiza un post para persistir el json
        """
        path = self.layer_path + store_name + "/coverages.json"

        username = GEOSERVER["user"]
        password = GEOSERVER["password"]

        tmpl = {
            "coverage": {
                "name": "",
                "nativeName": "",
                "title": "",
                "srs": "EPSG:4326",
                "enabled": "true"
            }
        }
        #~ se setean los parametros
        tmpl["coverage"]["name"] = store_name
        tmpl["coverage"]["nativeName"] = store_name
        tmpl["coverage"]["title"] = store_name

        self.make_request(path, str(tmpl))

    def tmp_buffer(self, name, content):
        """
        Este método se encarga de genear el archivo de forma temporal
        """
        path = '/var/www/geodengue_server'
        name = path + "/data/{0}.tmp".format(name)
        fo = open(name, "wb")
        fo.write(content)
        fo.close()
        #~ se retorna el path absoluto del archivo
        return os.path.abspath(name)

    def upload_file(self, src_file, layer_name):
        """
        Este método se encarga de subir un archivo al geoserver.
        """
        method = "GET"
        username = GEOSERVER["user"]
        password = GEOSERVER["password"]
        layer_name = "coverages/{0}/{1}".format(
            GEOSERVER["workspace"], layer_name)

        # se construye la url
        path = "/geoserver/script/apps/upload-file"
        path += "?layer_name=" + urllib2.quote(layer_name.encode("utf8"))
        path += "&src_file=" + urllib2.quote(src_file.encode("utf8"))
        #~ header para la autenticación
        headers = {
            'Authorization': b'Basic ' + base64.b64encode(username + b':' + password),
        }
        #~ se establece la conexión
        host = GEOSERVER["host"] + ":" + GEOSERVER["port"]
        conn = httplib.HTTPConnection(host)
        #~ Se encarga de realizar al get
        req = conn.request(method, path, None, headers)
        #~ Se obtiene la respuesta del servidor.
        response = conn.getresponse()
        self.print_result(response, method)
        conn.close()

    def print_result(self, result, method):
        """
        Esta función imprime el response obtenido al ejecutar el metodo
        'method'
        """
        print method + " : " + str(result.status) + " : " + result.reason


if __name__ == "__main__":
    geo = Geoserver()
    workspace = "geodengue"
    #~ geo.upload_file(filename, workspace)
    store = geo.create_coverage_store("evol")
    layer_name = store + ".asc"
    content = """
    ncols   300
    nrows   300
    xllcorner   -6411192.00319
    yllcorner   -2917373.78955
    cellsize    10.3189988184
    NODATA_value    -9999
    """
    src_file = geo.tmp_buffer(store, content)
    geo.upload_file(src_file, layer_name)
    geo.publish_coverage(store)
    #~ geo.create_raster_layer(store);
