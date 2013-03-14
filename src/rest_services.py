#! /usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask
from controller import *
"""
Este modulo define la interfaz de los servicios rest.
"""
__author__ = "Maximiliano Báez"
__mail__ = "mxbg.py@gmail.com"

#Se inicializa la api rest
app = Flask(__name__)

@app.route('/interpolate/', methods=['GET'])
def api_root():
    """Path por defecto de los servicios"""
    return 'No se hace nada'

@app.route('/interpolate/idw/', methods=['GET'])
def interpolate_idw():
    gis = GisController();
    resp = gis.method_idw();
    return str(resp)


if __name__ == '__main__':
    app.run()
