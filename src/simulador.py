#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Este módulo contiene la definición del proceso evolutivo de los puntos
de control.

@autors Maximiliano Báez, Roberto Bañuelos
@contact mxbg.py@gmail.com, robertobanuelos@gmail.com
"""

# Se impotan los modulos.
from poblacion import *
# log de eventos
from logger import EventLogger


class Simulador:

    """
    El proceso de evolución de las muestras consiste en un proceso, en el
    cual las muestras obtenidas mediante los dispositivos de ovipostura son
    expuestas a un conjunto de variaciones en un periodo de tiempo. Las
    variaciones que, principalmente, afectan a las muestras son :
    * Las variaciones del clima en dicho periodo : Se someten las muestras
        obtenidas a las distintas variaciones climáticas ocurridas en el
        periodo de tiempo seleccionado para el estudio.
    * La naturaleza del mosquito : Cada elemento de la muestra, es sometido
        a cambios considerando la naturaleza del mosquito. Los aspectos que
        se tienen en cuenta son su ciclo de vida del mosquito, ciclo
        reproductivo y el desplazamiento.
    """

    def __init__(self, **kargs):
        """
        Constructor de la clase
        @param kargs: Parametros de inicialización de la clase

        @keyword poblacion: La población inicial.
        @keyword periodo: El periodo de simulación.
        """
        self.zonas_table = RankingTable()
        #~ se inicializa el atributo periodo
        self.poblacion = Poblacion(kargs)
        #~ se inicializa el atributo periodo
        self.historial_clima = []
        #~ se inicializa el atributo periodo
        self.periodo = kargs.get('periodo', [])
        # se inicializa la clase que hace log de los eventos
        codigo = kargs.get('codigo', '')
        id_muestra = kargs.get('id_muestra', 1)
        self.logger = EventLogger(id_muestra, codigo)

    def start(self):
        """
        Se encarga de iniciar el simulador.
        """
        print self.poblacion
        dia_i = 0
        args = {}
        HUEVOS = True
        for dia in self.periodo.dias:
            #~ se procesa cada individuo de la población
            j = 0
            total_huevos = 0
            nueva_poblacion = []
            print "=" * 5 + "Día Nro :" + str(dia_i) + " Temp : " + str(dia.temperatura) + " poblacion :" + str(len(self.poblacion.individuos)) + "=" * 5

            for individuo in self.poblacion.individuos:
                poner_huevos = False
                cambio_estado = False
                cantidad_huevos = 0
                individuo.desarrollar(dia)

                #~ Se verifica el estado del individuo
                if self.poblacion.regular(individuo, dia, dia_i):
                    """
                    si el individuo esta muerto se lo remueve de la poblacion
                    """
                    self.poblacion.kill(individuo)

                elif self.poblacion.inhibicion(individuo, dia, dia_i):
                    """
                    [otero2006] se inhibe el desarrollo de huevos por
                    influencia de las larvas
                    """
                    self.poblacion.kill_inhibicion(individuo)

                elif individuo.esta_maduro() == True:
                    """
                    si el individuo esta maduro, se realiza el cambio de
                    estado.
                    """
                    # se logea el individuo antes de su cambio de estado
                    args = {}
                    args['aedes'] = individuo
                    args['dia'] = dia
                    args['periodo'] = dia_i
                    args['huevos'] = cantidad_huevos
                    self.logger.add(args)

                    individuo = self.poblacion.cambiar_estado(individuo)
                    self.poblacion.individuos[j] = individuo
                    cambio_estado = True

                elif individuo.estado == Estado.ADULTO and HUEVOS:
                    if individuo.se_reproduce(dia) == True:
                        # se genera un nueva poblacion
                        sub_poblacion, cantidad_huevos = self.poblacion.ovipostura(
                            individuo, dia)
                        """
                        se extiende la poblacion unicamente si se puso
                        huevos.
                        """
                        if len(sub_poblacion) > 0:
                            cantidad_huevos = len(sub_poblacion)
                            nueva_poblacion.extend(sub_poblacion)

                if cambio_estado == False:
                    args = {}
                    args['aedes'] = individuo
                    args['dia'] = dia
                    args['periodo'] = dia_i
                    args['huevos'] = cantidad_huevos
                    self.logger.add(args)
                    if cantidad_huevos > 0:
                        individuo.reset()

                j += 1
            if len(nueva_poblacion) > 0:
                total_huevos += len(nueva_poblacion)
                self.poblacion.extend(nueva_poblacion)

            print str(self.poblacion)

            self.logger.save()
            dia_i += 1

        print 'Poblacion final'
        print str(self.poblacion)
        return self.poblacion.to_grid()


if __name__ == "__main__":
    from db_manager import *
    from models import *
    from tutiempo import *

    id_muestras = 2

    for temperatura in [15, 18, 20, 22, 24, 25, 26, 27, 30, 34]:
    # for temperatura in [26, 27, 30, 34]:
        print "=" * 10 + str(temperatura) + "=" * 10
        # se obtiene el historial climatico
        print "obteniendo los datos climaticos"
        clima = TuTiempo("Asuncion")
        periodo = clima.get_periodo(temperatura)

        print "obteniendo los datos de la bd"
        dao = PuntosControlModel()
        data = dao.get_by(id_muestras)
        print "construyendo la grilla"
        #~ print data
        codigo = str(id_muestras) + ' temp=' + \
            str(temperatura) + " D=1"
        evol = Simulador(id_muestra=id_muestras,
                         periodo=periodo, poblacion=data, codigo=codigo)

        print "iniciando simulación"
        evol.start()
    """
    for ind in evol.poblacion :
        print str(ind)
    """
