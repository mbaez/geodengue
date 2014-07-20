#! /usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, request, Response, jsonify
from controller import *
#import pdi
import traceback

"""
Este modulo define la interfaz de los servicios rest.
"""
__author__ = "Maximiliano Báez"
__mail__ = "mxbg.py@gmail.com"

# Se inicializa la api rest
app = Flask(__name__)
controller = MainController()


@app.route('/', methods=['GET'])
def api_root():
    """Path por defecto de los servicios"""
    return ""


@app.errorhandler(500)
def internal_error(error):
    print error
    return "500 error " + str(error), 500


@app.errorhandler(404)
def not_found(error):
    return "404 error", 404


@app.route('/muestras', methods=['GET'])
def get_lista_muestras():
    resp = controller.get_all_muestras()
    print "parsing"
    return jsonify(lista=resp)


@app.route('/muestras/<id_muestra>/instantanea', methods=['POST'])
def interpolate_idw(id_muestra):
    gis = GisController(id_muestra)
    resp = gis.instantanea()
    return jsonify(resp)


@app.route('/muestras/<id_muestra>/procesos', methods=['GET'])
def get_codigos(id_muestra):
    resp = controller.get_codigos_by_muestra(id_muestra)
    return jsonify(lista=resp)

@app.route('/muestras/<id_muestra>/procesos/<codigo>', methods=['POST'])
def crear_proceso(id_muestra, codigo):
    resp = controller.new_proceso_evolutivo(id_muestra, codigo)
    return jsonify(resp)

@app.route('/muestras/<id_muestra>/procesos/<codigo>/dias', methods=['GET'])
def get_cantidad_dias(codigo):
    resp = controller.get_cantidad_dias(codigo)
    return jsonify(lista=resp)

@app.route('/muestras/<id_muestra>/procesos/<codigo>/dias/<dia>/foco', methods=['POST', 'GET' ])
def identificar_focos(id_muestra, codigo, dia):
    resp = controller.instante_diario(id_muestra, codigo, dia)
    return jsonify(resp)


@app.route('/logs/<codigo>/tasa-desarrollo', methods=['GET'])
def get_tasa_desarrollo(codigo):
    resp = controller.get_tasa_desarrollo(codigo)
    return jsonify(lista=resp)


@app.route('/logs/<codigo>/poblacion-diaria', methods=['GET'])
def get_poblacion_diaria(codigo):
    resp = controller.get_poblacion_diaria(codigo)
    return jsonify(lista=resp)


@app.route('/logs/<codigo>/dispersion', methods=['GET'])
def get_dispersion(codigo):
    resp = controller.get_dispersion(codigo)
    return jsonify(lista=resp)


@app.route('/logs/<codigo>/ciclo-gonotrofico', methods=['GET'])
def get_ciclo_gonotrofico(codigo):
    resp = controller.get_ciclo_gonotrofico(codigo)
    return jsonify(lista=resp)


@app.route('/pdi-img', methods=['POST'])
def pdi_img():

    print "Metodo"
    print request.method
    print "el file!"
    f = request.files['file']
    print "6- " + str(f)
    f.save("data/file.jpeg")
    cantidad = pdi.cantidad_contornos()
    return jsonify(json=cantidad)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
