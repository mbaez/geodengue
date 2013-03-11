from flask import Flask
"""
Este modulo define la interfaz de los servicios rest.
"""
__author__ = "Maximiliano Báez"
__mail__ = "mxbg.py@gmail.com"

#Se inicializa la api rest
app = Flask(__name__)

@app.route('/', methods=['GET'])
def api_root():
    """Path por defecto de los servicios"""
    return 'No se hace nada'
