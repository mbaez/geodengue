#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Este módulo contiene la definición de datos utilizados en el simulador.

@autors Maximiliano Báez, Roberto Bañuelos
@contact mxbg.py@gmail.com, robertobanuelos@gmail.com
"""
import math
# Se impotan los modulos.
from ranking_table import *
from models import *
from huevo import *
from larva import *
from pupa import *
from adulto import *


class Poblacion:

    """
    Clase que define el comportamiento goblal de la población.
    """
    ID = 1

    @property
    def memory(self):
        """Tabla en memoria"""
        return self.__memory

    @memory.setter
    def memory(self, value):
        self.__memory = value

    @property
    def individuos(self):
        """Array de individuos de la población"""
        return self.__individuos

    @individuos.setter
    def individuos(self, value):
        self.__individuos = value

    @property
    def total_huevos(self):
        """Total de huevos generados"""
        return self.__total_huevos

    @total_huevos.setter
    def total_huevos(self, value):
        self.__total_huevos = value

    def __init__(self, args):
        """
        Constructor de la clase
        @param kargs: Parametros de inicialización de la clase

        @keyword poblacion: La población inicial.
        @keyword periodo: El periodo de simulación.
        """
        self.__memory = {}
        self.__individuos = []
        self.zonas_table = RankingTable()
        self.zonas_table.poblacion = self
        self.__total_huevos = 0
        if args.has_key("poblacion") == True:
            self.generar_poblacion(args["poblacion"])

    def gen_sub_poblacion(self, **kargs):
        """
        Se encarga de generar un sub array de individuos a partir de los parametros
        definidos.
        """
        cantidad_larvas = kargs.get('cantidad_larvas', 0)
        madurez = kargs.get("madurez", 0)
        id_padre = kargs.get("id_padre", 0)
        # se determina el estado
        state = Estado.HUEVO
        if kargs.has_key('clazz') == True:
            state = Estado.LARVA
        # se determina el tipo de individuo a instanciar
        clazz = kargs.get('clazz', Huevo)
        posicion = kargs.get('posicion', Point(kargs))
        sub_poblacion = []
        # se inicializa la población
        self.new_grupo(
            posicion=posicion, cantidad=cantidad_larvas, estado=state)

        for cantidad in range(cantidad_larvas):
            indv = clazz(posicion=posicion, zonas=self.zonas_table,
                         madurez=madurez, id_padre=id_padre)
            # id del mosquito
            indv._id_mosquito = Poblacion.ID
            Poblacion.ID += 1
            #~ se añade el individuo a la sub población
            sub_poblacion.append(indv)

        return sub_poblacion

    def generar_poblacion(self, data):
        """
        Este método se encarga de procesar los datos de las muestras y
        generar los inidividuos para inicializar la población.
        """
        grid = Grid()
        grid.parse(data)
        for i in range(len(grid)):
            # se obtine la cantidad de individuos
            cantidad_larvas = int(grid.z[i])
            #~ se genera la sub población de larvas
            sub_poblacion = self.gen_sub_poblacion(
                cantidad_larvas=cantidad_larvas,
                #madurez=randint(0, 90),
                clazz=Larva,
                x=grid.x[i], y=grid.y[i])
            self.individuos.extend(sub_poblacion)

    def cambiar_estado(self, aedes):
        """
        Se encarga de realizar el cambio de estado para el individuo de
        acuerdo a su estado actual.
        """

        grupo = self.get(aedes.posicion)

        clazz = {
            "HUEVO": Larva,
            "LARVA": Pupa,
            "PUPA": Adulto
        }
        # diccionario que determina el siguiente estado para el estado actual.
        next_state = {
            "HUEVO": Estado.LARVA,
            "LARVA": Estado.PUPA,
            "PUPA": Estado.ADULTO
        }
        #~ Se actualizan los individuos
        grupo[aedes.estado]["cantidad"] -= 1
        grupo[aedes.estado]["cantidad_ant"] -= 1
        grupo[next_state[aedes.estado]]["cantidad"] += 1

        return clazz[aedes.estado](sexo=aedes.sexo, posicion=aedes.posicion,
                                   zonas=self.zonas_table, id=aedes.id_mosquito, id_padre=aedes.id_padre)

    def gen_key(self, punto):
        """
        Genera una clave única para el punto, la clave se genera de la siguiente
        forma : punto.x + "-" +  punto.y
        """
        return str(punto.x) + "_" + str(punto.y)

    def new_grupo(self, **kargs):
        """
        Este método se encarga de inicializar un nodo para la tabla de memoria
        que almacena todoa la información de los inidividuos de la poblacion. Si
        el nodo existe actualiza la cantidad de correspondiente para el estado
        del individuo;
        """
        estados = [Estado.HUEVO, Estado.LARVA, Estado.PUPA, Estado.ADULTO]
        grupo = {}
        punto = kargs.get('posicion', Point(kargs))
        state = kargs.get('estado')
        cantidad = kargs.get('cantidad', 0)
        # se genera la clave  para el punto
        key = self.gen_key(punto)
        if self.memory.has_key(key):
            self.memory[key][state]["cantidad"] += cantidad
            return self.memory[key]

        for estado in estados:
            grupo[estado] = {}
            grupo[estado]["cantidad"] = 0
            grupo[estado]["cantidad_ant"] = 0
            grupo[estado]["to_kill"] = 0
            grupo[estado]["inhibicion"] = 0
            grupo[estado]["periodo"] = -1
            grupo[estado]["dia"] = -1
            grupo[estado]["killed"] = 0

        grupo[state]["cantidad"] = cantidad
        self.memory[key] = grupo
        return self.memory[key]

    def get(self, punto):
        """
        Se ecarga de verificar si la zona ya fue rankeada, de ser así
        se retorna el valor de la tabla de zonas rankeadas. Si no fue
        rankeada se rankea la zona y se guarda en la tabla de ranking.
        """
        key = self.gen_key(punto)
        if not self.memory.has_key(key):
            return None

        return self.memory[key]

    def kill(self, aedes):
        """
        Se encarga de eliminar un idividuo de la población y actualizar la
        información de la población.
        """
        if aedes.estado == Estado.ADULTO:
            grupo = self.get(aedes.posicion_origen)
        else:
            grupo = self.get(aedes.posicion)

        if grupo != None:
            grupo[aedes.estado]["cantidad"] -= 1
            grupo[aedes.estado]["to_kill"] -= 1
            grupo[aedes.estado]["killed"] += 1

        aedes._expectativa_vida = 0

        self.individuos.remove(aedes)

    def regular(self, aedes, dia, periodo):
        """
        Se encarga de realizar las validaciones para realizar la reducción de
        la población.
        """
        if aedes.estado == Estado.ADULTO:
            grupo = self.get(aedes.posicion_origen)
        else:
            grupo = self.get(aedes.posicion)

        grupo_estado = grupo[aedes.estado]
        if grupo_estado["periodo"] < periodo:
            # se actualiza el periodo
            grupo_estado["periodo"] = periodo
            # se calcula la mortalidad del individuo
            mortalidad = aedes.mortalidad(dia.temperatura, grupo)
            """
            se actualiza la canitdad de inviduos que deben desaparecer
            en el periodo.
            """
            grupo_estado["to_kill"] = math.ceil(mortalidad)
            # print str(grupo_estado["to_kill"]) + "\t" + str(cantidad)
            self.gen_candidatos(grupo_estado)
        else:
            grupo_estado["index"] += 1

        # se verifica si el elemento actual es un candidato a eliminar
        is_candidato = False
        if grupo_estado["to_kill"] > 0:
            is_candidato = grupo_estado["index"] in grupo_estado["candidatos"]

        return grupo_estado["to_kill"] > 0 and is_candidato

    def inhibicion(self, aedes, dia, periodo):
        """
        [otero2006] se inhibe el desarrollo de huevos por influencia de las
        larvas. Se encarga de realizar las validaciones para realizar
        innibición del desarrollo.
        """
        if not aedes.estado == Estado.HUEVO:
            return False

        colonia = self.get(aedes.posicion)

        colonia_estado = colonia[aedes.estado]
        if colonia_estado["dia"] < periodo:
            # se actualiza el periodo
            colonia_estado["dia"] = periodo
            # se calcula la mortalidad del individuo
            mortalidad = aedes.inhibicion_eclosion(dia.temperatura, colonia)
            """
            se actualiza la canitdad de huevos que deben desaparecer
            en el periodo debido a la innibición de la eclosión
            """
            colonia_estado["inhibicion"] = math.ceil(mortalidad)

        # se verifica si el elemento actual es un candidato a eliminar
        return colonia_estado["inhibicion"] > 0

    def kill_inhibicion(self, aedes):
        """
        Se encarga de eliminar un idividuo de la población y actualizar la
        información de la población.
        """
        colonia = self.get(aedes.posicion)
        if colonia != None:
            # se reduce la cantidad de huevos
            colonia[aedes.estado]["cantidad"] -= 1
            colonia[aedes.estado]["inhibicion"] -= 1
            # se hace un cambio de estado para que se registre la mortalidad
            # como una larva
            aedes.estado = Estado.LARVA
            colonia[aedes.estado]["killed"] += 1

        aedes._expectativa_vida = -1
        self.individuos.remove(aedes)

    def gen_candidatos(self, colonia):
        """
        Se encarga de generar una lista aleatoria de candidatos de la
        población a ser eliminados.
        """
        candidatos = []
        for index in range(int(colonia["to_kill"])):
            candidato = randint(1, colonia["cantidad"])
            while candidato in candidatos:
                candidato = randint(1, colonia["cantidad"])
            # se añaden los candidatos
            candidatos.append(candidato)

        colonia["candidatos"] = candidatos
        colonia["index"] = 1

    def ovipostura(self, adulto, dia):
        """
        Se encarga de manejar el proceso de ovipostura del adulto hemba.
        """
        huevos = adulto.poner_huevos(dia)
        self.total_huevos += huevos
        if huevos > 0:
            return self.gen_sub_poblacion(posicion=adulto.posicion,
                                          cantidad_larvas=huevos, id_padre=adulto.id_mosquito), huevos
        return [], huevos

    def extend(self, nueva_poblacion):
        """
        Se encarga de extender la población para incluir los nuevos individuos.
        """
        self.individuos.extend(nueva_poblacion)

    def get_resumen(self):
        """
        Se encarga de generar un resumen de la poblacion
        """
        resumen = {}
        estados = [Estado.HUEVO, Estado.LARVA, Estado.PUPA, Estado.ADULTO]
        for estado in estados:
            resumen[estado] = {}
            resumen[estado]["total"] = 0
            resumen[estado]["muertas"] = 0

        for key in self.memory:
            for estado in self.memory[key]:
                resumen[estado]["total"] += self.memory[
                    key][estado]["cantidad"]
                resumen[estado]["muertas"] += self.memory[
                    key][estado]["killed"]

        resumen["total_huevos"] = self.total_huevos
        return resumen

    def to_grid(self):
        """
        Este método se encarga de traducir la población de inidviduos
        a un grid interpolable.

        Los adultos no son incluidos en el conteo de individuos.
        """
        key_map = {}
        data_array = []
        max_cantidad = 0
        all = True
        for key in self.memory:
            muertas = 0
            cantidad = 0
            for estado in self.memory[key]:
                muertas += self.memory[key][estado]["killed"]

            cantidad = self.memory[key][Estado.HUEVO]["cantidad"]
            cantidad += self.memory[key][Estado.LARVA]["cantidad"]
            cantidad += self.memory[key][Estado.PUPA]["cantidad"]
            if muertas > 0 or cantidad > 0:
                points = key.split("_")
                data = {}
                data['x'] = points[0]
                data['y'] = points[1]
                data['cantidad'] = cantidad
                data['id'] = 0
                data_array.append(data)
        print 'cantidad de puntos a interpolar: ' + str(len(data_array))

        # orden por coordenada
        print "sort por coordenada..."
        swapped = True
        while swapped:
            swapped = False
            for i in range(1, len(data_array)):
                comp1 = (data_array[i - 1]['x'], data_array[i - 1]['y'])
                comp2 = (data_array[i]['x'], data_array[i]['y'])
                if self.compare_coordinates(comp1, comp2) > 0:
                    aux = data_array[i - 1]
                    data_array[i - 1] = data_array[i]
                    data_array[i] = aux
                    swapped = True

        # se realiza el parse a grid
        grid = Grid()
        grid.parse(data_array)

        # se retorna la referencia al grid
        return grid

    def compare_coordinates(self, p1, p2):
        """
        Metodo para comparar 2 puntos
        @param p1, p2
        array puntos
            ej> p1 = (x1, y1)
        """
        if float(p1[0]) == float(p2[0]):
            return float(p1[1]) - float(p2[1])
        else:
            return float(p1[0]) - float(p2[0])

    def __str__(self):
        resumen = self.get_resumen()
        estados = [Estado.HUEVO, Estado.LARVA, Estado.PUPA, Estado.ADULTO]
        resumen = self.get_resumen()
        to_str = "Huevos Generados : " + str(self.total_huevos) + "\n"
        for estado in estados:
            to_str += str(estado) + " total :" + str(
                resumen[estado]["total"]) + "\n"
            to_str += str(estado) + " muertas :" + str(
                resumen[estado]["muertas"]) + "\n"

        return to_str
