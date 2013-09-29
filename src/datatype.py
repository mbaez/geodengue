#! /usr/bin/env python
# -*- coding: utf-8 -*-

class Enum(set):
    """
    Calse que define el tipo de dato enum
    """
    def __getattr__(self, name):
        if name in self:
            return name
        raise AttributeError

"""
Enum que representa los estados por lo cuales atravieza el individuo.
"""
Estado = Enum(["HUEVO", "LARVA","PUPA","ADULTO"])

"""
Sexo válidos del individuo
"""
Sexo = Enum(["MACHO", "HEMBRA"])

