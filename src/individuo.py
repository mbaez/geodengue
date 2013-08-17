#! /usr/bin/env python
# -*- coding: utf-8 -*-


__author__ = "Maximiliano Báez"
__mail__ = "mxbg.py@gmail.com"

#Se impotan los modulos.
from models import *

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
    INDEX_IND = 1
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
        @keyword [id]: El identificador del punto de control de origen.
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
        #~ TODO : ver estado inicial para los individuos que provienen de
        #~ las larvitrampas
        self.estado = kargs.get('estado', Estado.HUEVO);
        self.espectativa_vida = 100.0
        self.coordenada_x = kargs.get('x', None);
        self.coordenada_y = kargs.get('y', None);
        self.id_dispositivo = kargs.get('id', None);
        self.index = kargs.get('index', None);
        self.ultima_oviposicion = 0;
        self._id = Individuo.INDEX_IND
        Individuo.INDEX_IND += 1

    def esta_muerto (self):
        """
        La supervivencia de los mosquitos depende de la capacidad para alimentarse,
        reproducirse, protegerse y dispersarse.
        esta_muerto : si espectativa de vida <= 0, si edad >= 30 dias.
        """
        return (self.espectativa_vida <= 0 or self.edad >= 30*24 )

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
            and hora.temperatura > 18 \
            and self.estado == Estado.ADULTO

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
        Se verifica si el individuo debe o no cambiar de estado segun su
        edad.
        El cambio de estado esta determinado de forma randomica bajo los
        siguientes parametros.
            Estado  Tiempo promedio
            huevo   2 a 3 dias
            larva   4 a 14 dias
            pupa    1 a 4 dias

        """
        if self.estado == Estado.HUEVO :
            self.__desarrollar_huevo(hora)

        elif self.estado == Estado.LARVA :
            self.__desarrollar_larva(hora)

        elif self.estado == Estado.PUPA :
            self.__desarrollar_pupa(hora)

        elif self.estado == Estado.ADULTO :
            self.__desarrollar_adulto(hora)

        #~ Se incrementa la edad del individuo
        self.edad += 1;

    def __desarrollar_huevo(self, hora) :
        """
        Este método se encarga de desarrollar el individuo que se encuentra
        en el estado inicial de huevo.

        El desarrollo embriológico generalmente se completa en 48 horas
        si el ambiente es húmedo y cálido, pero puede prolongarse hasta
        5 días a temperaturas más bajas.
        """
        #~ se verifica si el individuo puede realizar un cambio de estado
        if self.edad < 5*24 :
            estado = randint(2, 5) * 24
            if estado <= self.edad :
                print str(self)

                self.estado = Estado.LARVA
                self.espectativa_vida = 100.0
        """
        TODO Como afecta las condiciones climáticas al desarrollo del huevo ?
        """
        self.espectativa_vida -= 0.1389


    def __desarrollar_larva(self, hora) :
        """
        Este método se encarga de desarrollar el individuo que se encuentra
        en el estado de larva

        El desarrollo larval a 14oC es irregular y la mortalidad
        relativamente alta. Por debajo de esa temperatura, las larvas
        eclosionadas no alcanzan el estado adulto. En condiciones óptimas
        el período larval puede durar 5 días pero comúnmente se extiende
        de 7 a 14 días.
        """
        #~ se verifica si el individuo puede realizar un cambio de estado
        if self.edad < 14*24  :
            estado = randint(4, 14) * 24
            if estado <= self.edad :
                print str(self)

                self.estado = Estado.PUPA
                self.espectativa_vida = 100.0

        """
        TODO Como afecta las condiciones climáticas al desarrollo de la
        larva ?
        """
        self.espectativa_vida -= 0.1389


    def __desarrollar_pupa(self, hora) :
        """
        Este método se encarga de desarrollar el individuo que se encuentra
        en el estado de pupa.

        El estado de pupa demora de 2 a 3 días.
        """
        #~ se verifica si el individuo puede realizar un cambio de estado
        if self.edad < 19*24 :
            estado = randint(14, 19) * 24
            if estado <= self.edad :
                print str(self)

                self.estado = Estado.ADULTO
                self.espectativa_vida = 100.0

        """
        TODO Como afecta las condiciones climáticas al desarrollo de la
        pupa ?
        """
        self.espectativa_vida -= 0.1389


    def __desarrollar_adulto(self, hora) :
        """
        Este método se encarga de desarrollar el individuo que se encuentra
        en el estado final de adulto.

        Cómo le afecta la temperatura : Limitantes para el desarrollo poblacional.
        Entre ellos, dentro del ambiente abiótico el potencial del vector
        se ve pautado por:
        """
        if hora.temperatura >= 40 or hora.temperatura <= 0 :
            """
            Día letal: si ocurre T<0o (T mínima diaria <0o) ó T> 40o C
            (T máxima diaria >40o C), ó aire muy seco. Se consideran
            fenecidas todas las formas adultas, y larvarias en el caso térmico,
            """
            self.espectativa_vida -= 4.3;
        else :
            """
            En el mejor de los casos y en condiciones optimas el individuo
            llegaría a los 30 días. Teniendo en cuenta que su espectativa
            de vida es 100, se debería disminuir su espectativa de vida
            según el siguiente cálculo:

               delta = 100/(30*24)
            """
            self.espectativa_vida -= 0.1389

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

                huevos.append(self.get_child())
            # se reinicia el contador
            self.ultima_oviposicion = 1;

            return huevos

        # se aumenta el contador de ultima oviposición
        self.ultima_oviposicion += 1
        return None

    def get_child (self):
        """
        Este método se encarga de obtener el hijo del inidividuo, el hijo
        hedea de su padre todos sus atributos.
        """
        return Individuo(x=self.coordenada_x, y=self.coordenada_y, \
                    id=self.id_dispositivo, index=self.index)

    def __str__(self):
        """
        Metodo que se encarga de traducir la clase a un string
        """
        return str(self.estado) + "(" + str(self.sexo) + ")" + \
            "vida=" + str(self.espectativa_vida) + \
            " edad=" + str(self.edad) + \
            " id=" +str(self._id)

