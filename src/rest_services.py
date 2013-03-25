#! /usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, request
from controller import *
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

@app.route('/larvitrampas/interpolar/<metodo>', methods=['GET'])
def interpolate_idw(metodo):
    gis = GisController();
    if metodo == 'idw' :
        resp = gis.method_idw(50, 50);
    elif metodo == 'voronoi' :
        resp = gis.method_voronoi(50, 50);

    return str(resp)


if __name__ == '__main__':
    app.run()
