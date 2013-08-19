#! /usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, request, Response
from controller import *
import json
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

@app.route('/muestras/<muestra>/instantanea', methods=['POST'])
def interpolate_idw(muestra):
    gis = GisController(muestra);
    col= row = 300
    resp = gis.method_idw(col, row);
    print "parsing"
    layer = gis.to_geoserver(resp, col, row, "inst")
    res = {}
    res["layer"] = layer
    return Response(json.dumps(res), mimetype='application/json')


@app.route('/muestras/<muestra>/evolucionar', methods=['POST'])
def evolutive(muestra):
    col= row = 300
    gis = GisController(muestra);
    print "starting..."
    resp = gis.method_evolutive()
    print "parsing"
    layer = gis.to_geoserver(resp, col, row, "evol")
    res = {}
    res["layer"] = layer
    return Response(json.dumps(res), mimetype='application/json')


if __name__ == '__main__':
    app.run(debug=True)
