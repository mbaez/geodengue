"""
Este módulo contiene la definición de datos utilizados en el simulador.

@autors Maximiliano Báez, Roberto Bañuelos
@contact mxbg.py@gmail.com, robertobanuelos@gmail.com
"""
from datatype import *
from db_manager import *

DAO = PuntosControlModel()

"""
Caracterización de las zonas
"""
Zonas = Enum(["OPTIMA", "BUENA", "NORMAL", "MALA", "PESIMA"])

class RankingTable:
    """
    Se encarga de guardar en memoria  el valor de todas las zonas que ya
    fueron rankeadas en algún momento para evitar calculos incecesarios.
    """
    @property
    def memory(self) :
        """Tabla en memoria"""
        return self.__memory

    @memory.setter
    def memory(self, value):
        self.__memory = value

    @property
    def get_tipo_zona(self, pts) :
        """
                T < 13  15 < T <20   20 < T < 25    25 < T < 36 T > 36
                Zonas   Frio    Fresco  Normal  Cálido  Caluroso
        60 < Pts  Optima  0   [10, 17.4] * 0.8    [9, 13]* 0.8    [5, 7.2] * 0.8  0
        60 > Pts  Buena   0   [17.4, 24.8] * 0.8  [13, 17]* 0.8   [7.2, 9.4] * 0.8    0
        30 > Pts  Normal  0   [24.8, 32.2] * 0.8  [17, 21]* 0.8   [9.4, 11.6] * 0.8   0
        20 > Pts  Mala    0   [32.2, 39.6] * 0.8  [21, 25]* 0.8   [11.6, 13.8] * 0.8  0
        8 > Pts   Pésima  0   [39.6, 47] * 0.8    [25, 29]* 0.8   [13.8, 16] * 0.8    0
        """
        if pts  < 8 :
            return Zonas.PESIMA

        elif pts  >= 8 and pts  < 20 :
            return Zonas.MALA

        elif pts  >= 20 and pts  < 30 :
            return Zonas.MALA

        elif pts  >= 30 and pts  < 60 :
            return Zonas.BUENA

        elif pts  >= 60 :
            return Zonas.OPTIMA

    def __init__(self) :
        pass

    def gen_key (punto, distancia):
        """
        Genera una clave única para el punto y la distancia.
        """
        return str(punto.x) + "-" + str(punto.y) + "-"  + str(distancia)


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
        zona_muestras = DAO.get_within(point, distancia)
        if len(zona_muestras) == 0 :
            return 0

        #~ se evaluan los puntos de riesgo
        for i in range(len(zona_muestras)) :
            rank_value += zona_muestras[i]['cantidad'];

        #~ se calcula el promedio de riesgo
        rank_value = rank_value / len(zona_muestras)

        return rank_value


    def get_ranking (self, punto, distancia) :
        """
        Se ecarga de verificar si la zona ya fue rankeada, de ser así
        se retorna el valor de la tabla de zonas rankeadas. Si no fue
        rankeada se rankea la zona y se guarda en la tabla de ranking.
        """
        key = self.gen_key(punto, distancia)
        if not self.memory.has_key(key) :
            rank_value = self.raking_zona(punto, distancia)
            self.memory[key] = rank_value

        return self.memory[key]
