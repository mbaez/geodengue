# -*- coding: utf-8 -*-
"""
Archivo wsgi utilizado para deployar los servicios en apache.

@autors Maximiliano Báez
@contact mxbg.py@gmail.com

Fuente : http://flask.pocoo.org/docs/deploying/mod_wsgi/
"""
import sys
sys.path.insert(0, '/var/www/geodengue_server')
sys.stdout = sys.stderr
#~  se importa el modulo rest
from rest_services import app as application
