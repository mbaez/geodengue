Dependencias
---
Se deben instalar los siguientes modulos del apache

```sh
    $ sudo apt-get install libapache2-mod-proxy-html
    $ sudo apt-get install libapache2-mod-wsgi
```
Configuraciones
---

* Se deben copiar los .conf a la carpeta /etc/apache2/conf.d/ del apache

```sh
    $ cp *.conf /etc/apache2/conf.d/
```
* Incluir los conf : se debe abrir archivo httpd.conf y pegar al final las siguientes líneas

```sh
    $ sudo vim /etc/apache2/httpd.conf
```

```conf
    Include /etc/apache2/conf.d/proxy.conf
    Include /etc/apache2/conf.d/geodengue.conf
```
* Deployar los servicios de Flask : Crear un enlace la carpeta que contiene los servicios para dar visibilidad al modulo wsgi

```sh
   $ cd /var/www
   $ ln -s /path/to/proyect/geodengue/src geodengue_server
```

* Reiniciar el apache

```sh
    $ sudo service apache2 restart
```
