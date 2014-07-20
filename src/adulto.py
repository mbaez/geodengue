#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Este módulo contiene la definición del estado Adulto

@autors Maximiliano Báez, Roberto Bañuelos
@contact mxbg.py@gmail.com, robertobanuelos@gmail.com
"""

from aaegypti import *


class Adulto(AeAegypti):

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
    def ultima_oviposicion(self):
        """
        Cantidad de horas desde la última oviposición.
        """
        return self._ultima_oviposicion

    @property
    def cantidad_oviposicion(self):
        """
        Cantidad de veces que el mosquito hembra ovipuso.
        """
        return self._cantidad_oviposicion

    @property
    def ultimo_alimento(self):
        """
        Tiempo transcurrido desde la ultima alimentación.
        """
        return self._ultimo_alimento

    @property
    def cantidad_alimentacion(self):
        """
        Porcentaje no digerido de la última alimentación.
        """
        return self._cantidad_alimentacion

    @property
    def ciclo_gonotrofico(self):
        return self.__ciclo_gonotrofico

    @property
    def no_se_alimenta(self):
        return self.__no_se_alimenta

    @property
    def no_pone_huevos(self):
        return self.__no_pone_huevos

    @property
    def buscando_criaderos(self):
        return self.__buscando_criaderos

    @property
    def se_alimenta(self):
        """
        Boolean que determina si se alimento o no
        """
        return self._se_alimenta

    @property
    def distancia_recorrida(self):
        """
        La distancia en metros recorrida por el mosquito adulto.
        """
        return self._distancia_recorrida

    @property
    def desplazamiento_diario(self):
        """
        La distancia en metros recorrida por el mosquito adulto.
        """
        return self._desplazamiento_diario

    @property
    def is_inseminada(self):
        """
        True si la hembra fue inseminada, False en caso contrario.
        """
        return self._is_inseminada

    @property
    def tipo_zona(self):
        """
        Indica el tipo de zona en la que se encuentra el individuo
        """
        return self._tipo_zona

    def __init__(self, **kargs):
        """
        @param kargs: Parametros de inicialización de la clase

        @keyword [sexo]: El sexo de la pupa a partir del cual evoluciono a adulto.
        @keyword [position]: El punto que determina la ubiación de la pupa
        """
        # se invoca al constructor de la clase padre.
        kargs['estado'] = Estado.ADULTO
        # se invoca al constructor de la clase padre.
        AeAegypti.__init__(self, **kargs)
        #~ print "new "+ str(self)
        self.posicion_origen = self.posicion.clone()
        self._ultima_oviposicion = 1
        self._ultimo_alimento = 1
        self._dias_vuelo = 0
        self._distancia_recorrida = 0
        self._desplazamiento_diario = 0
        self._cantidad_oviposicion = 0
        self._cantidad_alimentacion = 0
        self._alimentacion_necesaria = 0
        self._is_inseminada = False
        self._se_alimenta = False
        self._se_reproduce = False
        self.__no_pone_huevos = False
        self.__no_se_alimenta = False
        self.__buscando_criaderos = False
        self.__ciclo_gonotrofico = 0
        self.calcular_cantidad_alimentacion()
        self._tipo_zona = None

    def se_reproduce(self, dia):
        """
        El apareamiento ocurre dentro de las 24 horas siguientes a la
        emergencia. Éste se realiza durante el vuelo, pero en algunas
        ocasiones se lleva a cabo en una superficie vertical u horizontal

        El mosquito se reproduce si :
        * No está muerto = no
        * Sexo = hembra, temperatura > 18 C

        * Un día cualquiera es día de oviposición, si T>18o C en algún
        lapso del día, pero si T<18o todo el día, no pone huevos.

        @type dia : Dia
        @param dia: el objeto que contiene los datos climatologicos para
            un dia.
        """

        self._se_reproduce = self.is_inseminada == True \
            and self.sexo == Sexo.HEMBRA \
            and dia.temperatura >= 15

        return self._se_reproduce and self._se_alimenta

    def desarrollar(self, dia):
        """
        Este método se encarga de desarrollar el individuo que se encuentra
        en el estado adulto

        El tiempo de vida restante de un mosquito adulto depende de la
        calidad de su zona, el clima y su capacidad de alimentarse

        @type dia : Dia
        @param dia: el objeto que contiene los datos climatologicos para
            un dia.
        """
        #~ se envejece el adulto
        self._edad += 1
        self.inseminacion(dia)
        # se ranquea la zona
        self._tipo_zona = self.get_tipo_zona()

        if dia.temperatura > 15:
            self.volar(dia)
            self.buscar_alimento(dia)

        return self

    def buscar_alimento(self, dia):
        """
        Se tiene en cuenta la ubicacion del mosquito adulto y la densidad
        poblacional en dicha ubicación.

        Día adverso, si T máxima <15oC no vuela (por debajo de este umbral
        de vuelo, no vuela, no pica, ni ovipone). En definitiva, el potencial
        climático del vector es función de la temperatura y de la no-ocurrencia
        de valores por encima o por debajo de umbrales críticos, tanto térmicos
        como de humedad. Es de notar que para el caso de deficiencias de
        humedad, lo letal es función de la duración del período.

        @type dia : Dia
        @param dia: el objeto que contiene los datos climatologicos para
            un dia.
        """

        self._ultimo_alimento += 1

        """
        Si el individuo se marcó para no ser alimentado se omite el proceso de
        alimentación para el.
        """
        if self.no_se_alimenta == True:
            return

        elif self._se_alimenta == False:
            self._ultimo_alimento = 0
            # 2-3 mg = 20-30 cg
            self._cantidad_alimentacion += 1

        if self._cantidad_alimentacion == self._alimentacion_necesaria:
            self._se_alimenta = True

    def calcular_cantidad_alimentacion(self, is_frist=True):
        """
        Según "ESTUDIO DE LA LONGEVIDAD Y EL CICLO GONOTRÓFICO DEL Aedes
        (Stegomyia) aegypti (LINNAEUS, 1762), CEPA GIRARDOT (CUNDINAMARCA) EN
        CONDICIONES DE LABORATORIO"
        """
        prob_ovi = randint(0, 10000)
        if prob_ovi <= 2256 and is_frist:
            """
            Se puede observar  que el  22,56%(23) de la población no realizó
            ninguna toma de sangre.
            """
            self.__no_se_alimenta = True
            self._alimentacion_necesaria = 0
        if prob_ovi <= 6616:
            """
            259   43,6    Una toma de sangre durante su tiempo de vida.
            """
            self._alimentacion_necesaria = 1
            self._max_huevo = 67

        elif prob_ovi <= 8266:
            """
            98    16,5    Dos toma de sangre durante su tiempo de vida.
            """
            self._alimentacion_necesaria = 2
            self._max_huevo = 107
        elif prob_ovi <= 9108:
            """
            50    8,42    Tres toma de sangre durante su tiempo de vida.
            """
            self._alimentacion_necesaria = 3
            self._max_huevo = 137
        elif prob_ovi <= 9798:
            """
            41    6,9     Cuatro toma de sangre durante su tiempo de vida.
            """
            self._alimentacion_necesaria = 4
            self._max_huevo = 268
        else:
            """
            12    2,02    Cinco toma de sangre durante su tiempo de vida.
            """
            self._alimentacion_necesaria = 5
            self._max_huevo = 271

    def inseminacion(self, hora):
        """
        Inseminación :
        *  Antes de 24 horas ambos sexos están listos para el apareamiento
        *
        * El macho es atraído por el sonido emitido de las alas de la hembra durante
          el vuelo.
        * La inseminación,generalmente, se efectúa durante el vuelo.
        * Una vez alimentada de sangre ocurren pocos apareamientos.
        """
        if not self.sexo == Sexo.MACHO:
            self.inseminar_hembra(hora)

    def inseminar_hembra(self, hora):
        """
        Se encarga de verificar el estado de las hembras y verificar si
        estas pueden ser insemindadas.

        Sólo las hembras nulíperas son insemindandas debido a que una
        inseminación es suficiente para que la hembra pueda poner huevos
        toda su vida.

        @type hora : Hora
        @param hora: el objeto que contiene los datos climatologicos para
            una hora.

        @return True si se puede inseminar a la hembra, False en caso
            contrario.
        @rtype Boolean
        """
        porcentaje = randint(1, 100)
        #~ Para las hembras nulíperas (no ha puesto ningún huevo)
        if self.cantidad_oviposicion == 0 and self._cantidad_alimentacion == 0\
            and porcentaje <= 58 and self.is_inseminada == False:
                """
                El 58% son inseminadas antes de su primera alimentación
                sanguínea.
                """
                self._is_inseminada = True
                return True

        elif  self.cantidad_oviposicion == 0 and porcentaje <= 17 \
            and self.se_alimenta == True and self.is_inseminada == False:
                """
                El 17% durante durante la alimentación
                """
                self._is_inseminada = True
                return True

        elif  self.cantidad_oviposicion <= 1 and self.se_alimenta == True  \
            and porcentaje <= 25:
                """
                El 25% es inseminada entre la segunda alimentación y la
                primera oviposición.
                """
                self._is_inseminada = True
                return True
        """
        Una inseminación es suficiente para fecundar todos los huevos que
        la hembra produzca en toda su vida. Por lo que no es es relevante
        las inseminaciones posteriores a la primera debido que se busca
        'habilitar' la hembra para que ponga huevos.
        """
        return False

    def get_ciclo_gonotrofico(self, dia):
        """
        El ciclo gonotrófrico de los mosquitos es el nombre que se le
        adjudico al período que existe desde que el mosquito chupa la
        sangre- ovopostura- hasta que vuelve a alimentarse.

        Consiste en la absorción de sangre, seguido de la digestión, la
        maduración de los oocytos y la oviposición. El tiempo para la
        digestión de sangre y su consecuente producción de huevos varía
        de 3 a 5 días dependiendo de la temperatura ambiental.
        La temperatura influye en la duración de la digestión y el desarrollo
        de los ovarios, ya que cuando las temperaturas son bajas la digestión
        tarda más tiempo.
        """
        if self.cantidad_oviposicion == 0:
            coef = COEF_SH_DE.get_by("NULIPERA")
        else:
            coef = COEF_SH_DE.get_by(self.estado)

        cantidad_dias = 1 / self.sharpe_demichele(dia.temperatura, coef[0])

        return cantidad_dias

    def poner_huevos(self, dia):
        """
        Generalmente el apareamiento se realiza cuando la hembra busca
        alimentarse; se ha observado que el ruido que emite al volar es
        un mecanismo por el cual el macho es atraído. El mosquito hembra
        necesita la sangre para obtener proteínas y  poner sus huevos.

        La hembra embarazada es capaz de volar hasta 3km en busca de un
        sitio optimo para la ovipostura.

        @type dia : Dia
        @param dia: el objeto que contiene los datos climatologicos para
            un dia.
        """
        huevos = 0

        if self.no_pone_huevos == True:
            return -1

        """
        Según "ESTUDIO DE LA LONGEVIDAD Y EL CICLO GONOTRÓFICO DEL Aedes
        (Stegomyia) aegypti (LINNAEUS, 1762), CEPA GIRARDOT (CUNDINAMARCA) EN
        CONDICIONES DE LABORATORIO" se puede observar que el 21,9% (22) de los
        mosquitos que tomaron una ingesta de sangre no realizaron ovoposturas.
        """
        prob_ovi = randint(0, 100)
        if self.cantidad_alimentacion == 1 and self.ciclo_gonotrofico == 0:
            if prob_ovi <= 22:
                self.__no_pone_huevos = True
                return 0

        #~ se obtiene el ciclo gonotrofico
        ciclo_gonotrofico = self.get_ciclo_gonotrofico(dia)
        # se aumenta el contador de ultima oviposición
        self.__ciclo_gonotrofico += 100 / ciclo_gonotrofico
        #~ se realizan los controles de las condiciones
        if self.ciclo_gonotrofico >= 100 \
            and self.cantidad_alimentacion >= 1:
            huevos = self.generar_huevos(dia)

        return huevos

    def generar_huevos(self, dia):
        """
        Su ciclo para poner huevos es de aproximadamente cada tres días a
        cuatro días.

        Una alimentación escasa produce menos huevos por lote y si es muy
        reducida no se producen huevos.

        Este metodo se encarga de generar una cantidad aleatoria de huevos.
        Un solo mosquito hembra puede poner 80 a 150 huevos, cuatro veces
        al día.
        """
        # print "busqueda done.."
        self._cantidad_oviposicion += 1
        return randint(MIN_HUEVOS, MAX_HUEVOS)

    def reset(self):
        """
        Reinicia las variables de control
        """

        self._ultima_oviposicion = 0
        self._se_alimenta = False
        self.__ciclo_gonotrofico = 0
        self.calcular_cantidad_alimentacion(False)
        self._cantidad_alimentacion = 0

    def volar(self, dia):
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

        """
        dist_vuelo = MIN_VUELO

        tipo = self.get_tipo_zona()

        if self.sexo == Sexo.HEMBRA and (tipo == Zonas.MALA or tipo == Zonas.PESIMA):
            dist_vuelo = MAX_VUELO

        # Se calcula la distancia desde la posición actual a la origen
        distancia_origen = self.posicion.distance_to(self.posicion_origen)
        if distancia_origen >= dist_vuelo:
            angulo = self.posicion_origen.angle_to(self.posicion)
            # se modifica el sentido del angulo de vuelo
            angulo_vuelo = angulo + 180
            velocidad = uniform(0, distancia_origen)
        else:
            #~ se genera un angulo 'delta', para simular las corrientes de aire
            #~ que sigue el mosquito.
            delta = randint(-45, 45)
            #~ Vuelan en sentido contrario al viento
            angulo_vuelo = dia.direccion_viento + 180 + delta
            #~ se calcula la velocidad de vuelo
            velocidad = self.velocidad_vuelo(dia, angulo_vuelo)
        """
        Como la velocidad de vuelo esta en m/h y el tiempo de estudio
        es 1 hora, se utiliza la velocidad como distancia a recorrer

        distancia = Xo + Velocidad * Tiempo = Velocidad * 1h
        """
        distancia = velocidad
        self._distancia_recorrida += distancia
        self._desplazamiento_diario = distancia
        self.posicion.move(velocidad, angulo_vuelo)

    def velocidad_vuelo(self, hora, angulo_vuelo):
        """
        Al volar en busca de sangre, la hembra bate sus alas de 250 a 600
        veces/segundo, ello depende de la especie y en menor grado de su
        velocidad que puede llegar ser de 2 km por hora.

        Aedes albopictus
        TOP SPEED (FLYING) :  2km/h

        The Anopheles mosquito can fly for up to four hours continuously
        at 1–2 km/h ,traveling up to 12 km (7.5 mi) in a night.
        """
        speed = randint(0, MIN_VUELO)

        wind_speed = hora.viento

        """
        Se calcula la velocidad resultante medinte algebra de vectores.

        vx = sen(180 - angulo_vuelo) * speed + wind_speed
        vy = cos(180 - angulo_vuelo) * speed
        v = sqrt (Vx^2 + Vy^2 )
        """
        vx = math.sin(180 - angulo_vuelo) * speed - wind_speed
        vy = math.cos(180 - angulo_vuelo) * speed
        v = math.sqrt(vx ** 2 + vy ** 2)

        return v

    def mortalidad(self, temperatura, colonia):
        """

        Los adultos pueden permanecer vivos en el laboratorio durante meses y
        en la naturaleza pocas semanas. Con una mortalidad diaria de 10 %, la
        mitad de los mosquitos morirán durante la primera semana y 95 % en el
        primer mes.
        Fuente : http://scielo.sld.cu/scielo.php?pid=S0864-34662010000100015&script=sci_arttext

        Para la etapa adulto, otero2006 la define como una constante
        independiente de la temperatura.
        """

        return 0.09 * colonia[self.estado]["cantidad"]
