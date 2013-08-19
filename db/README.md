Postgres & Postgis
===
Guía de instalación y configuración de la base de datos.

Dependencias
---
Instalar los paquetes necessarios :

```sh
sudo apt-get install postgresql
sudo apt-get install postgis
```
Configurar el template para las bases de datos

```sh
sudo -u postgres createdb template_postgis
sudo -u postgres psql -d template_postgis -c "UPDATE pg_database SET datistemplate=true WHERE datname='template_postgis'"
sudo -u postgres psql -d template_postgis -f /usr/share/postgresql/9.1/contrib/postgis-2.0/postgis.sql
sudo -u postgres psql -d template_postgis -f /usr/share/postgresql/9.1/contrib/postgis-2.0/spatial_ref_sys.sql
sudo -u postgres psql -d template_postgis -f /usr/share/postgresql/9.1/contrib/postgis-2.0/postgis_comments.sql
sudo -u postgres psql -d template_postgis -f /usr/share/postgresql/9.1/contrib/postgis-2.0/rtpostgis.sql
sudo -u postgres psql -d template_postgis -f /usr/share/postgresql/9.1/contrib/postgis-2.0/raster_comments.sql
```
Crear la base de datos

```sql
CREATE DATABASE geodenguedb
  WITH ENCODING='UTF8'
       TEMPLATE=template_postgis
       CONNECTION LIMIT=-1;
```
