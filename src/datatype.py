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

import warnings

def deprecated(func):
    """
    This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emmitted
    when the function is used.
    """
    def newFunc(*args, **kwargs):
        warnings.warn("Call to deprecated function %s." % func.__name__,
                      category=DeprecationWarning)
        return func(*args, **kwargs)
    newFunc.__name__ = func.__name__
    newFunc.__doc__ = func.__doc__
    newFunc.__dict__.update(func.__dict__)
    return newFunc
"""
Enum que representa los estados por lo cuales atravieza el individuo.
"""
Estado = Enum(["HUEVO", "LARVA","PUPA","ADULTO"])

"""
Sexo válidos del individuo
"""
Sexo = Enum(["MACHO", "HEMBRA"])

"""
Caracterización de las zonas
"""
Zonas = Enum(["OPTIMA", "BUENA", "NORMAL", "MALA", "PESIMA"])

