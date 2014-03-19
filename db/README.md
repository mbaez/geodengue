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
Para veriones de Postgis <= 2.0
---
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

Para veriones de Postgis > 2.0
---
Instalar los paquetes necessarios :

```sql
sudo apt-get install build-essential postgresql-9.1 postgresql-server-dev-9.1 libxml2-dev libgdal-dev libproj-dev libjson0-dev xsltproc docbook-xsl docbook-mathml
sudo add-apt-repository ppa:ubuntugis/ubuntugis-unstable
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install postgresql-9.1-postgis
```

Crear la base de datos

```sql
CREATE DATABASE geodenguedb
  WITH ENCODING='UTF8'
       CONNECTION LIMIT=-1;

USE geodenguedb;

CREATE EXTENSION postgis;
CREATE EXTENSION postgis_topology;
```
