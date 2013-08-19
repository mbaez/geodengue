
import os
import shutil
import urllib2

__author__ = "Maximiliano Báez"
__mail__ = "mxbg.py@gmail.com"

DATA_PATH = "/data"
WAR_PATH = "/webapps/geoserver"

def get_url_params (environ):
    """
    Esta función se encarga de extaer los parametros de la url y genear
    un diccionario que las contiene.
    """
    query =  environ["QUERY_STRING"]
    args = query.split("&")
    params ={}
    for arg in args :
        value = arg.split("=")
        params[value[0]] = urllib2.unquote(value[1])

    return params

def create_file (path,src_file , layer_name) :
    """
    Esta función se encarga de crear un archivo.
    """
    shutil.move(src_file, path +"/"+ layer_name)


def app(environ, start_response):
    """
    Definición del módulo
    """
    #~ Se obtiene el path actual
    current = os.getcwd()
    #~ Se verifica en que directorio se encuentra el cursor, si no se
    #~ encuenta en el path de datos del geoserver, se mueve el cursor.
    if DATA_PATH not in current :
        os.chdir (".." + WAR_PATH + DATA_PATH)

    #se obtiene el path completo
    pwd = os.getcwd()
    #se obtinen los parametros de la url
    args =  get_url_params(environ)
    create_file(pwd, args["src_file"], args["layer_name"])
    # se responde ok
    start_response('200 OK', [('Content-Type', 'text/plain')])
    return [str(args)]


