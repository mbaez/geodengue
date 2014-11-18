Configuración de Geoserver [deprecated]
===
Instalar Plugin
---
Primero de debe copiar el script a la carpeta correspondiente para que
el geoserver se encarge de disponibilizar el plugin como servicio.

```sh
$ cp plugin/* $GEOSERVER_HOME/data/scripts/apps/upload-file/

```
Se debe crear el directorio donde se publicaran los layers
```sh
$ cd $GEOSERVER_HOME/data/coverages
$ mkdir geodengue

```
Dependecias
----
* [GeoScript plugin](http://docs.geoserver.org/stable/en/user/community/python/overview.html)
