#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Some class.
"""
__file_name__ = "classes.py"
__author__ = "luca"
__version__ = "1.0.0"
__date__ = "2014-10-23"


class EteDumbObj(dict):
    """
    Stupida classe che permette di usare un dizionario come un oggetto.

    :param dict_or_kwargs: oggetto dizionario o sequenza di chiave=valore
        (come per il dizionario).
    :type dict_or_kwargs: dict
    :param tabu: Lista di parole chiave NON utilizzabili dal dizionario.
    :type tabu: list
    """

    def __init__(self, *args, **kwargs):
        super(EteDumbObj, self).__init__(*args, **kwargs)

    def __getattr__(self, name):
        if name in self.__dict__:
            return self.__dict__[name]
        else:
            return self.get(name, None)

    def __setattr__(self, name, value):
        if name in self.__dict__:
            self.__dict__[name] = value
        else:
            if name in self.__tabu__:
                raise KeyError("%s is tabu")
            self[name] = value

    def __delattr__(self, name):
        try:
            del self[name]
        except KeyError:
            pass

    def __dir__(self):
        return self.keys() + self.__dict__.keys()


class Singleton(type):
    """
    Singleton metaclass.
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(
                Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
