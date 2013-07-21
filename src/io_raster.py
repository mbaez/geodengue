#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Input/Output
Para guardar los layers en la tabla postgis.
----------------------------

raster2pgsql -I -C -a-s <SRID> <PATH/TO/RASTER FILE> <SCHEMA>.<DBTABLE> | psql -d <DATABASE>


Para exportar los datos
---------------------------

SELECT oid, lowrite(lo_open(oid, 131072), png) As num_bytes
 FROM
 ( VALUES (lo_create(0),
   ST_AsPNG( (SELECT rast FROM aerials.boston WHERE rid=1) )
  ) ) As v(oid,png);
-- you'll get an output something like --
   oid   | num_bytes
---------+-----------
 2630819 |     74860

-- next note the oid and do this replacing the c:/test.png to file path location
-- on your local computer
 \lo_export 2630819 'C:/temp/aerial_samp.png'

-- this deletes the file from large object storage on db
SELECT lo_unlink(2630819);

"""

import os
from config import *

class Terminal :

    def publish_raster(self, file_name) :
        """
        Este método se encarga de publicar el raster de nombre `file_name`
        en la base de datos. La plubicación se realiza mediante el
        siguiente comando :

        $raster2pgsql -I -C -a-s <SRID> <PATH/TO/RASTER FILE> <SCHEMA>.<DBTABLE> |
            psql -d <DATABASE> -h<HOST> -p<PORT>

        @type file_name : String
        @params file_name: El nombre del archivo que describe la capa
                raster.
        """
        # Se construye el template del comando
        tmpl =  """
                raster2pgsql -I -C -a-s {0} {1} {2}.{3} |
                sed  "s/::raster);/::raster) RETURNING {4};/g|
                psql -d {5} -h{6} -p{7}
                """
        #se reemplaza los parametros
        command = tmpl.format(
            RASTER['srid'],
            TMP_HOME + file_name,
            RASTER['schema'],
            RASTER['table'],
            RASTER['pk'],
            DB['dbname'],
            DB['host'],
            DB['port']
        )
        print command.trim()
        #~ os.system(command)

if __name__== "__main__" :
    terminal = Terminal()
    terminal.publish_raster("tmp.asc")
