#! /usr/bin/env python
# -*- coding: utf-8 -*-


__author__ = "Maximiliano Báez"
__mail__ = "mxbg.py@gmail.com"

#Se impotan los modulos.

from db_manager import *
from models import *
from tutiempo import *

from random import randint
"""
Enum que representa los estados por lo cuales atravieza el individuo.
"""
Estado = Enum(["HUEVO", "LARVA","PUPA","ADULTO"])

"""
Sexo válidos del individuo
"""
Sexo = Enum(["MACHO", "HEMBRA"])

"""
Representación de un individuo de la población.
"""
class Individuo :
    """
    Esta clase contiene la representación de un individuo de la población.
    Un mosquito de la población tiene los siguientes atributos :
    * Sexo : Macho o hembra, valor generado aleatoriamente
    * Edad : cantidad de días que lleva vivo el mosquito.
    * Estado : Huevo, Larva, Pupa, Adulto..
    * Ubicación : coordenadas longitud y latitud
    * Dispositivo de origen : el código del dispositivo de ovipostura de origen.
    * Expectativa de vida : es un valor numérico que varía de acuerdo a las
            condiciones climáticas a las que es sometido el mosquito.
    * Ultima oviposición : es el indicador de la utlima fecha en la que el
            individuo puso huevos.
    * Periodo es el intervalo de tiempo al que será sometido la población inicial a evolución.
    """
    def __init__ (self, **kargs) :
        """
        @param kargs: Parametros de inicialización de la clase

        @keyword [estado]: El estado del individuo
        @keyword [id]: El identificador del punto de control de
            de origen.
        @keyword [x]: Coordenada x del dispositivo de origen.
        @keyword [y]: Coordenada y del dispositivo de origen.
        @keyword [edad]: La edad del individuo en horas
        """
        # Se genera de forma aleatoria el sexo del mosquito
        sexo = randint(0, 1)
        if sexo == 0 :
            self.sexo = Sexo.MACHO
        else :
            self.sexo = Sexo.HEMBRA

        self.edad = kargs.get('edad', 0 );
        #~ TODO : ver estado inicial para los individuos que probienen de
        #~ las larvitrampas
        self.estado = kargs.get('estado', Estado.HUEVO);
        self.espectativa_vida = 100
        self.coordenada_x = kargs.get('x', None);
        self.coordenada_y = kargs.get('y', None);
        self.id_dispositivo = kargs.get('id', None);
        self.ultima_oviposicion = 1;

    def esta_muerto (self):
        """
        La supervivencia de los mosquitos depende de la capacidad para alimentarse,
        reproducirse, protegerse y dispersarse.
        esta_muerto : si espectativa de vida <= 0, si edad >= 30 dias.
        """
        return self.espectativa_vida <= 0 or self.edad >= 30*24

    def se_reproduce (self, hora):
        """
        El mosquito se reproduce si :
        * No está muerto = no
        * Sexo = hembra, temperatura > 18 C

        * Un día cualquiera es día de oviposición, si T>18o C en algún
        lapso del día, pero si T<18o todo el día, no pone huevos.

        """
        return self.esta_muerto() == False \
            and self.sexo == Sexo.HEMBRA \
            and hora.temperatura > 18 #~ \ and self.estado == Estado.ADULTO

    def buscar_alimento(self, hora):
        """
        Se tiene en cuenta la ubicacion del mosquito adulto y la densidad
        poblacional en dicha ubicación.

        * Día adverso, si T máxima <15oC no vuela (por debajo de este umbral
        de vuelo, no vuela, no pica, ni ovipone). En definitiva, el potencial
        climático del vector es función de la temperatura y de la no-ocurrencia
        de valores por encima o por debajo de umbrales críticos, tanto térmicos
        como de humedad. Es de notar que para el caso de deficiencias de
        humedad, lo letal es función de la duración del período.

        """
        if hora.temperatura < 15 :
            return

    def desarrollar(self, hora) :
        """
        Cómo le afecta la temperatura : Limitantes para el desarrollo poblacional.
        Entre ellos, dentro del ambiente abiótico el potencial del vector
        se ve pautado por:
        """

        if hora.temperatura >= 40 or hora.temperatura <= 0 :
            """
            Día letal: si ocurre T<0o (T mínima diaria <0o) ó T> 40o C
            (T máxima diaria >40o C), ó aire muy seco (Cuadro 7.1). Se consideran
            fenecidas todas las formas adultas, y larvarias en el caso térmico,
            """
            self.espectativa_vida -= 4;
        else :
            self.espectativa_vida -= 1;

        self.edad += 1;

    def poner_huevos(self, hora) :
        """
        Generalmente el apareamiento se realiza cuando la hembra busca
        alimentarse; se ha observado que el ruido que emite al volar es
        un mecanismo por el cual el macho es atraído.

        Una vez copulada e inseminada la hembra, el esperma que lleva es
        suficiente para fecundar todos los huevitos que produce durante su
        existencia, no aceptando otra inseminación adicional.

        Su ciclo para poner huevos es de aproximadamente cada tres días.
        Su alimentación puede hacerla en cualquier momento (puede picar
        varias veces a las personas de una casa). Las proteínas contenidas
        en la sangre le son indispensables para la maduración de los huevos.
        La variación de temperatura y humedad, así como la latitud pueden
        hacer variar estos rangos del ciclo de vida de los mosquitos.

        La hembra deposita sus huevos en las paredes de recipientes con
        agua estancada, limpia y a la sombra. Un solo mosquito puede poner
         80 a 150 huevos, cuatro veces al día.
        """

        #Su ciclo para poner huevos es de aproximadamente cada tres días a
        # cuatro días
        ciclo = randint(3, 4)
        # se verifica la cantidad de días que pasaron desde su ultima
        # oviposición.
        if self.ultima_oviposicion % (ciclo * 24) == 0 :
            # Un solo mosquito puede poner 80 a 150 huevos, cuatro veces
            # al día.
            cantidad = randint(80, 150)
            huevos = []
            for i in range(cantidad) :
                huevos.append(Individuo())
            # se reinicia el contador
            self.ultima_oviposicion = 1;

            return huevos

        # se aumenta el contador de ultima oviposición
        self.ultima_oviposicion += 1
        return None

    def __str__(self):
        return str(self.estado) + " :  " + str(self.sexo) + " - " +\
            str(self.espectativa_vida) + " - " + str(self.edad )


class Simulador :
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

    def __init__ (self, **kargs) :
        """
        Constructor de la clase
        @param kargs: Parametros de inicialización de la clase

        @keyword poblacion: La población inicial.
        @keyword periodo: El periodo de simulación.
        """
        #~ se inicializa el atributo periodo
        self.poblacion =  [];
        if kargs.has_key("poblacion") == True:
            self.__init_poblacion__(kargs["poblacion"])
        #~ se inicializa el atributo periodo
        self.historial_clima =[]
        #~ se inicializa el atributo periodo
        self.periodo = kargs.get('periodo',[])

    def __init_poblacion__ (self, grid ):
        """
        Este método se encarga de procesar los datos de las muestras y
        generar los inidividuos para inicializar la población.

        """
        grid = Grid();
        grid.parse(data);
        for i in range(len(grid)):
            # se obtine la cantidad de individuos
            cantidad_larvas = int(grid.z[i]);
            for cantidad in range(cantidad_larvas) :
                #se inicializa los inidviduos

                indv = Individuo(x=grid.x[i], y=grid.y[i], id=grid.ids[i], estado=Estado.LARVA)
                self.poblacion.append(indv)


    def start(self):
        """
        Se encarga de iniciar el simulador.
        """
        i=0
        for hora in self.periodo.horas :
            #~ se procesa cada individuo de la población
            j=0
            nueva_poblacion = []
            for individuo in self.poblacion :
                #~ Se desarrolla el inidividuo
                individuo.desarrollar(hora)

                #~ Se verifica el estado del individuo
                if(individuo.esta_muerto() == True):
                    #~ print "Esta muerto.. Individiuos restantes :" +\
                        #~ str(len(self.poblacion))
                    self.poblacion.remove(individuo)

                elif(individuo.se_reproduce(hora) == True) :
                    #~ print "se reproduce :"
                    huevos = individuo.poner_huevos(hora)
                    if not huevos == None :
                        nueva_poblacion.extend(huevos)
                #~ fin del preiodo
                j += 1
            #~ fin del preiodo
            self.poblacion.extend(nueva_poblacion)
            i += 1
            print "hora " + str(i)


if __name__ == "__main__" :
    id_muestras = 1;
    #se obtiene el historial climatico
    print "obteniendo los datos climaticos"
    clima = TuTiempo("Asuncion")
    periodo = clima.get_periodo()

    print "obteniendo los datos de la bd"
    dao = PuntosControlModel()
    data = dao.get_by(id_muestras);
    print "construyendo la grilla"
    #~ print data

    evol = Simulador(periodo=periodo, poblacion=data)

    print "iniciando simulación"
    evol.start()
    for ind in evol.poblacion :
        print str(ind)

