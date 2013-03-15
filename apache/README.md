Configuraciones
---
* Copiar los .conf a la carpeta /etc/apache2/conf.d/
    $ cp *.conf /etc/apache2/conf.d/

* Abrir archivo /etc/apache2/httpd.conf e incluir
    Include /etc/apache2/conf.d/proxy.conf
    Include /etc/apache2/conf.d/geodengue.conf

* Reiniciar apache2
    $ sudo service apache2 restart
