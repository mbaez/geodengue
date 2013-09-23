#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Este módulo contiene la definición del AeAegypti y sus estados (Huevo,
Larva, Pupa, Adulto) para, finalmente, representar a un individuo.

@autors Maximiliano Báez, Roberto Bañuelos
@contact mxbg.py@gmail.com, robertobanuelos@gmail.com
"""
import time
import math
#Se impotan los modulos.
from models import *
from db_manager import *
from random import randint

"""
Enum que representa los estados por lo cuales atravieza el individuo.
"""
Estado = Enum(["HUEVO", "LARVA","PUPA","ADULTO"])

"""
Sexo válidos del individuo
"""
Sexo = Enum(["MACHO", "HEMBRA"])
DAO = PuntosRiesgoDao()

total_huevos = 0

class RankingTable:
    """
    Se encarga de guardar en memoria  el valor de todas las zonas que ya
    fueron rankeadas en algún momento para evitar calculos incecesarios.
    """
    memory = {}

    @staticmethod
    def gen_key (punto, distancia):
        """
        Genera una clave única para el punto y la distancia.
        """
        return str(punto.x) + "-" + str(punto.y) + "-"  + str(distancia)



class AeAegypti :
    """
    Clase base, contiene la definición los atributos básicos.
    """
    @property
    def espectativa_vida(self):
        """
        La expectativa de vida es un valor numérico(entre 0 y 100) que
        varía de acuerdo a las condiciones climáticas a las que es
        sometido el mosquito. Cuando la espectativa de vida es creo el
        mosquito muere.
        """
        return self._espectativa_vida

    @property
    def edad(self):
        """
        La edad es la cantidad de horas que lleva el individuo lleva vivo.
        """
        return self._edad

    @property
    def sexo(self):
        """
        El sexo puede ser Macho o hembra, valor generado aleatoriamente.
        """
        return self._sexo

    @property
    def estado(self):
        """
        Indica el estado actual de la clase.
        """
        return self._estado

    @property
    def madurez (self):
        """
        La madurez es un valor numérico(entre 0 y 100) que varía de acuerdo
        a las condiciones climáticas a las que es sometido el mosquito.
        Cuando la madurez es igual a 100 el mosquito ya se encuentra
        listo para un cambio de estado.
        """
        return self._madurez

    @property
    def posicion (self):
        """
        La posición esta definida por las coordenadas x e y, se encuentra
        representada por un punto.

        @see Point
        """
        return self._posicion

    def __init__(self, **kargs) :
        """
        Inicializa la clase setenado la espectativa de vida y la edad a
        cero.

        @param kargs: Parametros de inicialización de la clase

        @keyword [sexo]: El enum que identifica el sexo del AeAegypti
        @keyword [estado]: El enum que identifica el estado del AeAegypti
        @keyword [x]: la coordenada x
        @keyword [y]: La coordenada y
        @keyword [posicion]: El punto que determina la ubiación del AeAegypti
        """
        self._sexo = kargs.get('sexo', None)
        self._estado = kargs.get('estado', None)
        if kargs.has_key('posicion') :
            self._posicion = kargs.get('posicion', None)
        else :
            self._posicion = Point(kargs)
        self._edad = 0;
        self._madurez = 0;
        self._espectativa_vida = 100;
        self.delta_vuelo = 0;

    def se_reproduce (self, hora) :
        """
        @type hora : Hora
        @param hora: el objeto que contiene los datos climatologicos para
            una hora.
        """
        return False;

    def __str__(self):
        """
        Metodo que se encarga de traducir la clase a un string
        """
        return str(self.estado) + "(" + str(self.sexo) + ")" + \
            "vida=" + str(self.espectativa_vida) + \
            " edad=" + str(self.edad) + "  madurez=" + str(self.madurez)

class Huevo(AeAegypti) :
    """
    Esta clase contiene la representación del AeAegypti en su etapa de
    huevo.
    """
    def __init__(self, **kargs) :
        """
        @param kargs: Parametros de inicialización de la clase

        @keyword [sexo]: El enum que identifica el sexo del Huevo
        @keyword [position]: El punto que determina la ubiación del huevo
        """
        # Se genera de forma aleatoria el sexo del huevo
        sexo = randint(0, 1)
        if sexo == 0 :
            sexo = Sexo.MACHO
        else :
            sexo = Sexo.HEMBRA
        kargs['sexo'] = sexo
        kargs['estado'] = Estado.HUEVO
        # se invoca al constructor de la clase padre.
        AeAegypti.__init__(self, **kargs);

    def esta_muerto (self):
        """
        La supervivencia de los mosquitos depende de la capacidad para alimentarse,
        reproducirse, protegerse y dispersarse.
            Estado  Tiempo promedio
            huevo   2 a 5 dias
        """
        return self.espectativa_vida <= 0 or self.edad > 5*24

    def desarrollar(self, hora) :
        """
        Para el estudío se supone que los criaderos disponibles estan
        delimitados por los puntos de control(dispositivos de ovipostura)
        fijados. Para el caso de los huevos, estos son depositados
        individualmente en las paredes de los recipientes(dispositivo de
        ovipostura) por encima del nivel del agua.

        Para el desarrollo del huevo se supone que una vez que culmine el
        desarrollo embriológico los huevos eclosionarán.

        La lógica de que los huevos deben mojarse para eclosionar no está
        implementada, así como que los huevos desarrollados pueden
        sobrevivir por periodos largos para posteriormente eclosionar.

        @type hora : Hora
        @param hora: el objeto que contiene los datos climatologicos para
            una hora.
        """
        #~ se verifica si el individuo puede realizar un cambio de estado
        if self.madurez >= 100 :
            #~ print "Huevo -> Larva " + str(self)
            return Larva(sexo=self.sexo,posicion=self.posicion)
        #~ Se inicializan las variables
        delta_vida = 0
        delta_madurez = 0
        #~ Se realizan los controles para aumentar y/o disminuir la
        #~ espectativa de vida y la madurez de la larva de acuerdo con
        #~ la temperatura del medio.
        if hora.temperatura >= 27 :
            """
            Se considera un clima cálido cuando la temperatura es superior
            de los 27 C.

            El desarrollo embriológico generalmente se completa en 48 horas
            si el ambiente es húmedo y cálido.
            """
            delta_madurez = 100/48.0
        elif hora.temperatura <= 15 :
            """
            El desarrollo embriológico puede prolongarse hasta 5 días a
            temperaturas bajas.
            """
            delta_madurez = 100/120.0
            #~ Arbitrariamente se disminuye la espectativa de vida del huevo
            delta_vida = 100/ 140.0
        else :
            """
            En temperaturas no optimas se calcula con regla de 3 el delta
            de maduración del huevo.
            """
            temp_med = randint(27,40)
            delta_madurez = (hora.temperatura * 48.0 )/(temp_med * 1.0)

        #~ Se disminuye la espectativa de vida en un delta
        self._espectativa_vida -= delta_vida
        #~ se incrementa la madurez del mosquito en un delta
        self._madurez += delta_madurez
        self._edad +=1
        return self;

class Larva(AeAegypti) :
    """
    Esta clase contiene la representación del AeAegypti en su etapa de
    larva.

    Los porcentajes (y rango) del tiempo total de desarrollo, en todo el
    rango de temperaturas, que pasó en cada etapa inmadura son :
    1er estadio : 19% (13,9 a 23,1)
    2do estadio : 14% (11,3 a 21,3)
    3er estadio : 17% (13,0 a 27,0)
    4to estadio : 27% (24,2 a 28,5)
    Fuente : Temperature-Dependent Development and Survival Rates of
    Culex quinquefasciatus tus and Aedes aegypti (Diptera: Culicidae
    """

    def __init__(self, **kargs) :
        """
        @param kargs: Parametros de inicialización de la clase

        @keyword [sexo]: El el sexo del huevo a partir del cual eclosionó la larva.
        @keyword [position]: El punto que determina la ubiación de la larva
        """

        if not kargs.has_key('sexo') :
            # Se genera de forma aleatoria el sexo del mosquito
            sexo = randint(0, 1)
            if sexo == 0 :
                kargs['sexo'] = Sexo.MACHO
            else :
                kargs['sexo'] = Sexo.HEMBRA
        kargs['estado'] = Estado.LARVA

        # se invoca al constructor de la clase padre.
        AeAegypti.__init__(self, **kargs);

        """
        Seleccion natural
        "...del número inicial de individuos (larvas de primer estadio)
        solamente emergió el 9%, es decir, que la mortalidad total de
        las etapas inmaduras fue del 91%. La mayor tasa de mortalidad
        se observó en las larvas de cuarto estadio (54%), mientras que
        la menor mortalidad se observó en la etapa de pupa (18%).
        La proporción de sexos de los adultos emergidos fue de 1:1..."

        "...Con una mortalidad típica diaria de 10%, la mitad de los
        mosquitos morirán durante la primera semana y el resto durante
        el primer mes... "

        Aplicamos los porcentajes asociados a la mortalidad para simular
        la seleccion natural de los mosquitos
        """
        if randint(0, 100) > 10 :
            self.espectativa_vida = 0



    def esta_muerto (self):
        """
        La supervivencia de los mosquitos depende de la capacidad para alimentarse,
        reproducirse, protegerse y dispersarse.
            Estado  Tiempo promedio
            larva   4 a 14 dias
        """
        return (self.espectativa_vida <= 0 or self.edad > 14 * 24 )


    def desarrollar(self, hora) :
        """
        Este método se encarga de desarrollar el individuo que se encuentra
        en el estado de larva

        En condiciones óptimas el período larval puede durar 5 días pero
        comúnmente se extiende de 7 a 14 días.

        @type hora : Hora
        @param hora: el objeto que contiene los datos climatologicos para
            una hora.
        """
        #~ se verifica si el individuo puede realizar un cambio de estado
        if self.madurez >= 100 :
            #~ print "Larva -> Pupa " + str(self)
            return Pupa(sexo=self.sexo,posicion=self.posicion)

        #~ Se inicializan las variables
        delta_vida = 0
        delta_madurez = 0
        #~ Se realizan los controles para aumentar y/o disminuir la
        #~ espectativa de vida y la madurez de la larva de acuerdo con
        #~ la temperatura del medio.
        if hora.temperatura >= 34 :
            """
            La temperatura más alta que permite el desarrollo es 36oC,
            con una menor duración del estado larval.

            En condiciones óptimas el período larval puede durar 5 días,
            Lo que significa que maduraría en razon a
            delta_madurez = 100/(5*24)
            """
            delta_madurez = 100.0/(5.0*24.0)

        elif hora.temperatura >= 20 and hora.temperatura <= 34 :
            """
            Las temperaturas más cálidas ayudan a la rápida maduración
            de las larvas.

            En condiciones calidas el período larvar pude durar 5 y 8 días,
            de forma aleatoria se calcula la duración del periodo larvario
            para calcular el delta de la maduración
            """
            duracion_periodo = randint(5, 8) * 24.0
            delta_madurez = 100.0/ duracion_periodo

        elif hora.temperatura <= 11 :
            """
            El desarrollo cero se sitúa en 13,3oC, con un umbral inferior
            de desarrollo ubicado entre 9 y 10oC

            Christophers (1960) señala que la actividad del insecto disminuye
            abruptamente por debajo de 15oC hasta inhibición bajo medias
            diarias de 12oC.

            Para evitar su desarrollo se disminuye la espectativa de vida
            del individuo considerablemente como para que muera en un
            lapso de 72 hs(Arbitrariamente).
            delta = 100/72
            """
            delta_vida = 100.0/72.0
            #~ delta_madurez = 100/(14*24)
            delta_madurez = 100.0/(14.0*24.0)

        elif hora.temperatura <= 15 :
            """
            El desarrollo larval a 14 C es irregular y la mortalidad
            relativamente alta. Por debajo de esa temperatura, las larvas
            eclosionadas no alcanzan el estado adulto.

            Para evitar su desarrollo se disminuye la espectativa de vida
            del individuo considerablemente como para que muera en un
            lapso de 96 hs(Arbitrariamente).
            delta = 100/96
            """
            delta_vida = 100.0/92.0
            #~ se aumenta la madurez del individuo.
            delta_madurez = 100.0/(14.0*24.0)

        else :
            """
            De forma aleatoria se calcula la duración del periodo larvario
            para calcular el delta de la maduración
            """
            duracion_periodo = randint(5, 14) * 24.0
            delta_madurez = 100.0/ duracion_periodo
            delta_vida = 0.1389

        #~ Se disminuye la espectativa de vida en un delta
        self._espectativa_vida -= delta_vida
        #~ se incrementa la madurez del mosquito en un delta
        self._madurez += delta_madurez
        self._edad +=1

        return self;

class Pupa(AeAegypti) :
    """
    Esta clase contiene la representación del AeAegypti en su etapa de
    pupa. La etapa de pupa es una etapa de no alimentación, se mueven,
    respondiendo a cambios en la luz y al movimiento. Durante esta etapa,
    el mosquito se transforma en adulto. En mosquitos Culex esto toma 2
    días en el verano. Las pupas de mosquito viven en el agua de 1 a 4
    días, según la especie y la temperatura.

    La metamorfosis del mosquito en adulto se completa dentro de la cavidad
    de la pupa. Cuando el desarrollo está terminado, la piel de la pupa se
    rompe y el mosquito adulto emerge

    @see http://medicina.tij.uabc.mx/von/ciclo.html
    @see http://www.todosobremosquitos.com.ar/index.php?id=48&titulo=pupas-de-mosquitos
    """
    def __init__(self, **kargs) :
        """
        @param kargs: Parametros de inicialización de la clase

        @keyword [sexo]: El sexo de la larva a partir del cual evoluciono a pupa.
        @keyword [position]: El punto que determina la ubiación de la pupa
        """
        # se invoca al constructor de la clase padre.
        kargs['estado'] = Estado.PUPA
        AeAegypti.__init__(self, **kargs);

    def esta_muerto (self):
        """
        El estadio de pupa dura aproximadamente dos o tres días, emergiendo
        alrededor del 88% de los adultos en cuestión de 48 horas (Méndez et al., 1996)
        @see Dengeue en Mexico

        """
        return (self.espectativa_vida <= 0 or self.edad > 4*24 )

    def desarrollar(self, hora) :
        """
        El estadio de pupa dura aproximadamente dos o tres días, emergiendo
        alrededor del 88% de los adultos en cuestión de 48 horas (Méndez et al., 1996)

        Entre los 27-32oC la pupa que da lugar al Adulto macho emerge en
        1,9 días y la pupa que originará una hembra muda en 2,5 días.

        La duración promedio de la pupa, expresada como porcentaje del
        tiempo ocupado por la larva hasta que llega a adulto es de 20,6
        (Baz-Zeed, 1958)

        [26,83 (10-47)] * 0.206 días a 20oC
        [17,59 (9-29)]  * 0.206 días a 25oC
        [9,75 (5-16) ] * 0.206  días a 30oC

        @see Dengeue en Mexico
        @see El Aedes aegypti y la transmision del dengue
        @see The effect of temperature on the growth rate and survival
             of the immature stages of Aedes aegypti
        """
        #~ se verifica si el individuo puede realizar un cambio de estado
        if self.madurez >= 100 :
            #~ print "Pupa -> Adulto " + str(self)
            return Adulto(sexo=self.sexo, posicion=self.posicion)

        #~  se inicializa la varible
        delta_madurez = 0.0
        if hora.temperatura >= 27  and hora.temperatura <= 32:
            """
            Entre los 27-32oC la pupa se transforma a un adulto, escenario
            ideal :

            Macho 1.9 días : delta_madurez = 100 /(1.9 * 24)
            Hembra 2.5 días: delta_madurez = 100 /(2.5 * 24)

            TODO : ¿Que pasa cuando la temperatura supera los 32 C ?
            """
            #~ Si es hembra el proceso de madurez tarda más
            if self.sexo == Sexo.HEMBRA :
                delta_madurez = 100/(2.5 * 24.0)
            else :
                delta_madurez = 100/(1.9 * 24)

        elif hora.temperatura > 20  and hora.temperatura <= 25:
            """
            [17,59 (9-29)] * 0.206 días a 25oC
            Para determinar  la cantidad de días que toma a un macho y
            una hembra se partio del punto que para el desarrollo, en
            condiciones optimas se dearrolla un
            Macho 1.9 días
            Hembra 2.5 días

            Suponiendo que el estado por defecto es la hembra se calcula
            la relación:

            Macho = 2.5 / 1.9 Hembras = 1,315789474 Hembras

            """
            delta_madurez = 100.0 / (randint(9, 29) * 0.206 * 24.0)
            #~  si es macho madura más rápido
            if Sexo.MACHO == self.sexo :
                delta_madurez =  delta_madurez / 1.315789474

        elif hora.temperatura <= 20:
            """
            [26,83 (10-47)] * 0.206 días a 20oC

            Para determinar  la cantidad de días que toma a un macho y
            una hembra se partio del punto que para el desarrollo, en
            condiciones optimas se dearrolla un
            Macho 1.9 días
            Hembra 2.5 días

            Suponiendo que el estado por defecto es la hembra se calcula
            la relación:

            Macho = 2.5 / 1.9 Hembras = 1,315789474 Hembras

            """
            delta_madurez =100.0 / (randint(10,47) * 0.206 * 24.0)
            #~  si es macho madura más rápido
            if Sexo.MACHO == self.sexo :
                delta_madurez =  delta_madurez / 1.315789474


        """
        TODO Como afecta las condiciones climáticas al desarrollo de la
        pupa ?
        """
        self._espectativa_vida -= 0.1389
        self._madurez += delta_madurez
        self._edad +=1

        return self

class Adulto(AeAegypti) :
    """
    ECOLOGÍA DEL ADULTO
    Emergencia
    Luego de emerger de la pupa, el insecto se posa sobre las paredes del
    recipiente durante varias horas hasta el endurecimiento de sus alas y
    su exoesqueleto.

    Apareamiento
    Dentro de las 24 h, después de la emergencia, puede ocurrir el apareamiento.
    El macho es atraído por el sonido emitido por el batir de las alas de la
    hembra durante el vuelo.

    Alimentación
    Las hembras se alimentan de la mayoría de vertebrados, pero prefieren
    a los humanos, vuelan en sentido contrario al viento y son atraídas por
    los olores y gases del hombre. La sangre sirve para el desarrollo de
    los huevos.

    Ciclo gonadotrófico
    Después de cada alimentación se desarrolla un lote de huevos. Si la
    hembra completa su alimentación sanguínea (2-3 mg) desarrollará y
    pondrá 100-200 huevos, el intervalo dura de dos a tres días. La hembra
    grávida buscará recipientes oscuros o sombreados para depositar sus
    huevos, prefiriendo aguas limpias y claras.

    Rango de vuelo
    La hembra no sobrepasa los 50-100 m durante su vida (puede permanecer
    en la misma casa donde emergió). Si no hay recipientes, una hembra
    grávida puede volar tres kilómetros para poner sus huevos. Los machos
    se dispersan menos que las hembras.

    Conducta de reposo
    Descansan en lugares sombreados como alcobas, baños, patios o cocinas.
    Se les captura sobre ropas colgadas, debajo de muebles, toallas, cortinas
    y mosquiteros.

    Longevidad
    Los adultos pueden permanecer vivos en el laboratorio durante meses y
    en la naturaleza pocas semanas. Con una mortalidad diaria de 10 %, la
    mitad de los mosquitos morirán durante la primera semana y 95 % en el
    primer mes.

    Fuente : http://scielo.sld.cu/scielo.php?pid=S0864-34662010000100015&script=sci_arttext
    """

    @property
    def ultima_oviposicion (self):
        """
        Cantidad de horas desde la última oviposición.
        """
        return self._ultima_oviposicion;

    @property
    def cantidad_oviposicion (self):
        """
        Cantidad de veces que el mosquito hembra ovipuso.
        """
        return self._cantidad_oviposicion

    @property
    def ultimo_alimento (self):
        """
        Tiempo transcurrido desde la ultima alimentación.
        """
        return self._ultimo_alimento;

    @property
    def cantidad_alimentacion (self):
        """
        Porcentaje no digerido de la última alimentación.
        """
        return self._cantidad_alimentacion;

    @property
    def distancia_recorrida (self):
        """
        La distancia en metros recorrida por el mosquito adulto.
        """
        return self._distancia_recorrida;

    @property
    def is_inseminada (self):
        """
        True si la hembra fue inseminada, False en caso contrario.
        """
        return self._is_inseminada;

    def __init__(self, **kargs) :
        """
        @param kargs: Parametros de inicialización de la clase

        @keyword [sexo]: El sexo de la pupa a partir del cual evoluciono a adulto.
        @keyword [position]: El punto que determina la ubiación de la pupa
        """
        # se invoca al constructor de la clase padre.
        kargs['estado'] = Estado.ADULTO
        # se invoca al constructor de la clase padre.
        AeAegypti.__init__(self,**kargs);
        #~ print "new "+ str(self)
        self._ultima_oviposicion = 1
        self._ultimo_alimento = 1;
        self._distancia_recorrida = 0;
        self._cantidad_oviposicion = 0;
        self._cantidad_alimentacion = 0;
        self._is_inseminada = True;

    def se_reproduce (self, hora):
        """
        El apareamiento ocurre dentro de las 24 horas siguientes a la
        emergencia. Éste se realiza durante el vuelo, pero en algunas
        ocasiones se lleva a cabo en una superficie vertical u horizontal

        El mosquito se reproduce si :
        * No está muerto = no
        * Sexo = hembra, temperatura > 18 C

        * Un día cualquiera es día de oviposición, si T>18o C en algún
        lapso del día, pero si T<18o todo el día, no pone huevos.

        @type hora : Hora
        @param hora: el objeto que contiene los datos climatologicos para
            una hora.

        """
        return self.is_inseminada == True \
            and self.esta_muerto() == False \
            and self.sexo == Sexo.HEMBRA \
            and hora.temperatura > 18

    def esta_muerto (self):
        """
        La supervivencia de los mosquitos depende de la capacidad para alimentarse,
        reproducirse, protegerse y dispersarse.

        adulto  si espectativa de vida <= 0, si edad >= 30 dias.

        * Muchos mueren al momento de emerger
        * Si la población emergente original es grande, la restante es suficiente
          para transmitir la enfermedad y mantener o provocar una epidemia (Nelson,1986).
        """
        #~ 10% de mortalidad diaria
        if randint(0,100) <= 10 and (self.edad % 24) == 0 :
            return True;

        #~ 50% mueren en la primera semana
        elif randint(0,100) <= 50 and (self.edad % (7*24)) == 0 :
            return True;

        #~ 95% durante el primer mes
        elif randint(0,100) <= 95 and (self.edad % (30*24)) == 0 :
            return True;

        return (self.espectativa_vida <= 0)

    def desarrollar(self, hora) :
        """
        Este método se encarga de desarrollar el individuo que se encuentra
        en el estado final de adulto.

        Cómo le afecta la temperatura : Limitantes para el desarrollo poblacional.
        Entre ellos, dentro del ambiente abiótico el potencial del vector

        Variable atmosférica    Valor umbral letal  Duración letal (días)
        Déficit de saturación       >30 mb              2
        Déficit de saturación       entre 25 y 30 mb    3
        Déficit de saturación       entre 20 y 25 mb    5
        Déficit de saturación       entre 15 y 20 mb    10
        Temperatura máxima          > 40 oC             1
        Temperatura mínima          < 0 oC              1


        @type hora : Hora
        @param hora: el objeto que contiene los datos climatologicos para
            una hora.
        """
        puede_volar = True
        if hora.temperatura >= 40 or hora.temperatura <= 0 :
            """
            Día letal: si ocurre T<0o (T mínima diaria <0o) ó T> 40o C
            (T máxima diaria >40o C), ó aire muy seco. Se consideran
            fenecidas todas las formas adultas, y larvarias en el caso térmico,
            """
            self._espectativa_vida -= 4.3;

        elif hora.temperatura < 15 :
            """
            Día adverso, si T máxima <15oC no vuela (por debajo de este
            umbral de vuelo, no vuela, no pica, ni ovipone)

            TODO: Averiguar cuanto tiempo puede vivir sin alimentarse
            delta = 100/(10*24)
            """
            puede_volar = False
            self._espectativa_vida -= 100/(10*24)

        else:
            """
            En el mejor de los casos y en condiciones optimas el individuo
            llegaría a los 30 días. Teniendo en cuenta que su espectativa
            de vida es 100, se debería disminuir su espectativa de vida
            según el siguiente cálculo:

               delta = 100/(30*24)
            """
            self._espectativa_vida -= 0.1389

        self._edad +=1

        if puede_volar == True :
            self.volar(hora)

        return self;

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

        * La alimentación y la postura ocurren principalmente durante el día
        * Existe una mayor actividad en las primeras horas de haber amanecido,
         a media mañana, a media tarde o al anochecer.
        *  La hembra embarazada es capaz de volar hasta 3km en busca de un
         sitio optimo para la ovipostura.
        * Los machos suelen dispersarse en menor magnitud que las hembras.

        @type hora : Hora
        @param hora: el objeto que contiene los datos climatologicos para
            una hora.
        """
        if hora.temperatura < 15 :
            return

    def alimentarse(self, hora) :
        """
        * Las hembras se alimentan de sangre de cualquier vertebrado.
        * Las hembras y machos se alimentan de carbohidratos de cualquier fuente
          accesible como frutos o néctar de flores.
        * La hembra queda completamente satisfecha con de dos a tres miligramos
          de sangre
        """
        pass

    def inseminacion (self, hora):
        """
        Inseminación :
        *  Antes de 24 horas ambos sexos están listos para el apareamiento
        *
        * El macho es atraído por el sonido emitido de las alas de la hembra durante
          el vuelo.
        * La inseminación,generalmente, se efectúa durante el vuelo.
        * Una vez alimentada de sangre ocurren pocos apareamientos.
        """
        if self.sexo == Sexo.MACHO :
            #~ buscar a hembras para inseminarse
            inseminar_macho(hora)
        else :
            self.inseminar_hembra(hora)

    def inseminar_macho (self, hora) :
        """
        Buscar hembras para inseminar
        """
        pass

    def inseminar_hembra (self, hora) :
        """
        Se encarga de verificar el estado de las hembras y verificar si
        estas pueden ser insemindadas.

        Sólo las hembras nulíperas son insemindandas debido a que una
        inseminación es sufuiciente para que la hembra pueda poner huevos
        toda su vida.

        TODO : Se debe verificar si existe algun macho cerca para poder
        realizar la inseminación.

        @type hora : Hora
        @param hora: el objeto que contiene los datos climatologicos para
            una hora.

        @return True si se puede inseminar a la hembra, False en caso
            contrario.
        @rtype Boolean
        """

        porcentaje =  randint(1, 100)
        #~ Para las hembras nulíperas (no ha puesto ningún huevo)
        if self.cantidad_oviposicion == 0  \
            and self.cantidad_alimentacion == 0 \
            and porcentaje <= 58 \
            and self.is_inseminada == False :
                """
                El 58% son inseminadas antes de su primera alimentación
                sanguínea.
                """
                self._is_inseminada = True
                return True

        elif  self.cantidad_oviposicion == 0 \
            and porcentaje <= 17 \
            and self.is_inseminada == False :
                """El 17% durante durante la alimentación"""
                self._is_inseminada = True
                return True;

        elif  self.cantidad_oviposicion <= 1 \
            and self.cantidad_alimentacion == 0 \
            and porcentaje <= 25 :
                """
                El 25% es inseminada entre la segunda alimentación y la
                primera oviposición.
                """
                self._is_inseminada = True
                return True;
        """
        Una inseminación es suficiente para fecundar todos los huevos que
        la hembra produzca en toda su vida. Por lo que no es es relevante
        las inseminaciones posteriores a la primera debido que se busca
        'habilitar' la hembra para que ponga huevos.
        """
        return False

    def digestion(self, hora):
        """
        Dependiendo a la temperatura los mosquitos-hembra adultas digieren
        más rápidamente/lentamente la sangre y se alimentan más/menos
        frecuentemente.

        @type hora : Hora
        @param hora: el objeto que contiene los datos climatologicos para
            una hora.
        """
        pass

    def get_ciclo_gonotrofico (self, hora) :
        """
        El intervalo de tiempo entre la alimentación y la postura (ciclo
        gonotrófico) es de 48 horas en condiciones óptimas de temperatura.
        """
        return randint (48, 96)

    def poner_huevos(self, parent, hora) :
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

        El mosquito hembra necesita la sangre para obtener proteínas y
        poner sus huevos.

        * La mayoría de las posturas ocurre cerca del crepúsculo.

        @type hora : Hora
        @param hora: el objeto que contiene los datos climatologicos para
            una hora.
        """

        huevos = None
        #~ se obtiene el ciclo gonotrofico
        ciclo_gonotrofico = self.get_ciclo_gonotrofico(hora)
        # se aumenta el contador de ultima oviposición
        self._ultima_oviposicion += 1

        #~ se realizan los controles de las condiciones
        if self.ultimo_alimento >= ciclo_gonotrofico \
          and self.cantidad_oviposicion == 0 \
          and self.cantidad_alimentacion >= 2:
            """
            Para hembras nuliperas, la primera generación de óvulos requiere
            por lo menos dos alimentaciones sanguíneas para su maduración.
            """
            huevos = self.generar_huevos()

        elif self.ultimo_alimento >= ciclo_gonotrofico :
            """
            Después de cada alimentación sanguínea la hembra desarrolla un
            lote de huevos.
            """
            huevos = self.generar_huevos()

        huevos = self.generar_huevos(parent)

        return huevos

    def generar_huevos (self, parent) :
        """
        Su ciclo para poner huevos es de aproximadamente cada tres días a
        cuatro días.

        Una alimentación escasa produce menos huevos por lote y si es muy
        reducida no se producen huevos.

        Este metodo se encarga de generar una cantidad aleatoria de huevos.
        Un solo mosquito hembra puede poner 80 a 150 huevos, cuatro veces
        al día.
        """
        huevos = None
        if (self.ultima_oviposicion % 6) == 0 :
            """
            Un solo mosquito puede poner 80 a 150 huevos, cuatro veces
            al día.

            24 horas / 4 veces al día = cada 6 horas
            self.ultima_oviposicion % 6 == 0 ? poner huevos : no huevos

            """
            cantidad = randint(80, 150)
            huevos = []
            for i in range(cantidad) :
                huevos.append(parent.get_child())

            # se reinicia el contador
            self._ultima_oviposicion = 1;

        return huevos

    def volar(self, hora) :
        """
        Los machos rondan como voladores solitarios aunque es más común
        que lo hagan en grupos pequeños (Bates, 1970; Kettle, 1993) atraídos
        por los mismos huéspedes vertebrados que las hembras.

        Vuelan en sentido contrario al viento, desplazándose mediante lentas
        corrientes de aire, siguen los olores y gases emitidos por el
        huésped (CO2), al estar cerca utilizan estímulos visuales para
        localizarlo mientras sus receptores táctiles y térmicos las guían
        hacia el sitio donde se posan.

        Por lo general, la hembra de Ae. aegypti no se desplaza más allá de
        5,000 m de distancia de radio de vuelo en toda su vida, permanece
        físicamente en donde emergió, siempre y cuando no halla algún factor
        que la perturbe o no disponga de huéspedes, sitios de reposo y de
        postura. En caso de no haber recipientes adecuados, la hembra grávida
        es capaz de volar hasta tres kilómetros en busca de este sitio.
        Los machos suelen dispersarse en menor magnitud que las hembras

        En un ensayo de laboratorio, con viento en calma mosquitos
        Ae. aegypti se desplazan a 17 cm/s, al introducir viento en contra
        de 33 cm/s, incrementaron su velocidad para contrarrestarle disminuyendo
        su avance a 16 cm/s, lo que implica un esfuerzo de desplazamiento
        como si hubieran volado a 49 cm/s, por consiguiente volar con
        viento de mayor velocidad le representa un mayor esfuerzo y suelen
        hacerlo (Kettle, 1993).
        """
        #~ se genera un angulo 'delta', para simular las corrientes de aire
        #~ que sigue el mosquito.
        delta = randint(-45, 45)
        #~ Vuelan en sentido contrario al viento
        angulo_vuelo = hora.direccion_viento + 180 + delta
        #~ TODO : averiguar la velocidad de vuelo en promedio
        #~ Como determinar que una zona es buena?
        se_mueve = self.move_to_neighbors(hora)
        self.delta_vuelo += 1
        """
        Permanece físicamente en donde emergió, siempre y cuando no
        halla algún factor que la perturbe o no disponga de huéspedes,
        sitios de reposo y de postura. El alcance noral es de 100 metros.
        """
        if  se_mueve == True:
            """
            En caso de no haber recipientes adecuados, la hembra grávida
            es capaz de volar hasta tres kilómetros en busca de este sitio.
            Los machos suelen dispersarse en menor magnitud que las hembras
            """
            self.posicion.move(100, angulo_vuelo)

    def raking_zona(self, point, distancia) :
        """
        Este método se encarga de analizar los puntos criticos y dar un
        puntaje a la zona. Una zona se califica teniendo en cuenta :

        * La cantidad de puntos criticos que existen en la zona.
        * El riesgo de los puntos criticos.
        """
        rank_value = 0.0
        dist_value = 0.0
        #~ Se obtienen todos los puntos de riesgo que se encuentran en la zona
        #~ para analizar si el mosquito debe volar en busca de mejores
        #~ condiciones
        puntos_riesgo = DAO.get_within(point, distancia)
        if len(puntos_riesgo) == 0 :
            return 0

        #~ se evaluan los puntos de riesgo
        for i in range(len(puntos_riesgo)) :
            rank_value += puntos_riesgo[i]['riesgo'];
            dist_value += self.posicion.distance_to(puntos_riesgo[i])
        #~ se calcula el promedio de riesgo
        rank_value = rank_value / len(puntos_riesgo)
        #~ se calcula el promedio de distancia
        dist_value = dist_value / len(puntos_riesgo)

        return rank_value / dist_value

    def get_ranking (self, punto, distancia) :
        """
        Se ecarga de verificar si la zona ya fue rankeada, de ser así
        se retorna el valor de la tabla de zonas rankeadas. Si no fue
        rankeada se rankea la zona y se guarda en la tabla de ranking.
        """
        key = RankingTable.gen_key(punto, distancia)
        if RankingTable.memory.has_key(key) :
            return RankingTable.memory[key]
        else :
            rank_value = self.raking_zona(punto, distancia)
            RankingTable.memory[key] = rank_value

    def move_to_neighbors (self, hora) :
        """
        Este método se encarga de evaluar el vecino inmediato y comparalo
        con el valor de la posicion actual, si el vecino posee un puntaje
        mayor que el puntaje actual retorna true.

        En caso de no haber recipientes adecuados, la hembra grávida
        es capaz de volar hasta tres kilómetros en busca de este sitio.
        Los machos suelen dispersarse en menor magnitud que las hembras

        Son muchos los factores que afectan el vuelo de los mosquitos:

        1. disponibilidad de sitios resguardados del sol,
        2. disponibilidad de vegetación y fuentes de néctar,
        3. ubicación, cantidad y disponibilidad de sitios de cría,
        4. dirección del viento,
        5. lluvias,
        6. urbanización,
        7. fuentes para la ingesta de sangre
        8. estado del mosquito: recién emergido, hembras grávidas, edad,
            nivel de alimentación, etc.

        @type hora : Hora
        @param hora: el objeto que contiene los datos climatologicos para
            una hora.

        @return True si el vecino posee una mayor puntación, False en caso
            contrario.
        @rtype Boolean
        """

        distancia = 100
        #~ se evalua la zona
        best_rank = self.get_ranking(self.posicion, distancia)
        #~ se calcula el angulo de vuelo
        angulo_vuelo = hora.direccion_viento + 180

        #~ se evalua el vecino
        punto_vecino = self.posicion.project(distancia, angulo_vuelo)
        #~ se rankea la zona
        rank_value = self.get_ranking(punto_vecino, distancia)
        #~ se compara el valor de la zona
        if(rank_value > best_rank) :
            return True
        return False

    def velocidad_vuelo(self, hora, angulo_vuelo) :
        """
        Al volar en busca de sangre, la hembra bate sus alas de 250 a 600
        veces/segundo, ello depende de la especie y en menor grado de su
        velocidad que puede llegar ser de 2 km por hora.

        Aedes albopictus
        TOP SPEED (FLYING) :  2km/h

        The Anopheles mosquito can fly for up to four hours continuously
        at 1–2 km/h ,traveling up to 12 km (7.5 mi) in a night.
        """

        speed = randint(1000, 2000)
        wind_speed = hora.viento

        """
        Se calcula la velocidad resultante medinte algebra de vectores.

        vx = sen(180 - angulo_vuelo) * speed + wind_speed
        vy = cos(180 - angulo_vuelo) * speed
        v = sqrt (Vx^2 + Vy^2 )
        """
        vx = math.sin(180 - angulo_vuelo) * speed - wind_speed
        vy = math.cos(180 - angulo_vuelo) * speed
        v = sqrt (vx^2 + vy^2 )

        return  v


class Individuo :
    INDEX_IND = 1
    """
    Esta clase contiene la representación de un individuo de la población.
    Un mosquito de la población tiene los siguientes atributos :
    * mosquito : Huevo, Larva, Pupa, Adulto.
    * Ubicación : coordenadas longitud y latitud
    * Dispositivo de origen : el código del dispositivo de ovipostura de origen.
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

        estado = kargs.get('estado', Estado.HUEVO);
        #~ Se inicializa el mosquito de acuerdo al estado.
        self.mosquito = None
        if estado == Estado.HUEVO :
            self.mosquito = Huevo(**kargs)
        else :
            self.mosquito = Larva(**kargs)

        #~ TODO : ver estado inicial para los individuos que provienen de
        #~ las larvitrampas
        self.coordenada_x = kargs.get('x', None);
        self.coordenada_y = kargs.get('y', None);

        self.id_dispositivo = kargs.get('id', None);
        self.index = kargs.get('index', None);

        self._id = Individuo.INDEX_IND
        Individuo.INDEX_IND += 1

    def esta_muerto (self):
        """
        La supervivencia de los mosquitos depende de la capacidad para
        alimentarse, reproducirse, protegerse y dispersarse.
        """
        return self.mosquito.esta_muerto();

    def desarrollar(self, hora) :
        """
        Se verifica si el individuo debe o no cambiar de estado segun su
        edad. El cambio de estado esta determinado de forma randomica
        bajo los siguientes parametros.
            Estado  Tiempo promedio
            huevo   2 a 3 dias
            larva   4 a 14 dias
            pupa    1 a 4 dias

        @type hora : Hora
        @param hora: el objeto que contiene los datos climatologicos para
            una hora.
        """
        self.mosquito = self.mosquito.desarrollar(hora)
        #~ print str(self.mosquito) +" temp : " + str(hora.temperatura)

    def se_reproduce (self, hora):
        """
        El apareamiento ocurre dentro de las 24 horas siguientes a la
        emergencia. Éste se realiza durante el vuelo, pero en algunas
        ocasiones se lleva a cabo en una superficie vertical u horizontal

        @type hora : Hora
        @param hora: el objeto que contiene los datos climatologicos para
            una hora.

        """
        return self.mosquito.se_reproduce(hora)

    def poner_huevos(self, hora) :
        """

        @type hora : Hora
        @param hora: el objeto que contiene los datos climatologicos para
            una hora.
        """
        return self.mosquito.poner_huevos(self, hora)

    def get_child (self):
        """
        Este método se encarga de obtener el hijo del inidividuo, el hijo
        hedea de su padre todos sus atributos.
        """
        return Individuo(x=self.coordenada_x, y=self.coordenada_y, \
                    id=self.id_dispositivo, index=self.index)



