#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Some util.
"""
__file_name__ = "utils.py"
__author__ = "luca"
__version__ = "1.0.0"
__date__ = "2014-10-23"

import argparse
import inspect
import os
import glob
import types


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


class SubcommandHelpFormatter(argparse.RawDescriptionHelpFormatter):
    """
    Classe per la formattazione dell' help
    """
    def _format_action(self, action):
        parts = super(SubcommandHelpFormatter, self)._format_action(action)
        if action.nargs == argparse.PARSER:
            parts = "\n".join(parts.split("\n")[1:])
        return parts


def check_class():
    """
    Ritorna il nome della classe per la frame attuale.
    Se il risultato è **None** vuol dire che la chiamata è fatta da un modulo.
    """
    frames = inspect.stack()
    class_name = None
    for frame in frames[1:]:
        if frame[3] == "<module>":
            # At module level, go no further
            break
        elif '__module__' in frame[0].f_code.co_names:
            class_name = frame[0].f_code.co_name
            break
    return class_name


def isglob(value):
    """
    Windows non traduce automaticamente i wildchars così lo facciamo
    a mano tramite glob.

    :param value: Espressione glob per la lista dei files.
    :type value: str
    """
    if os.name == 'nt':
        if isinstance(value, basestring):
            value = glob.glob(value)
    return value


def string_or_bool(value):
    """
    Ritorna True o False in caso venga passata la stringa 'true' o 'false'
    (o 't' o 'f') altrimenti ritorna una stringa.

    :param value: Stringa da analizzare.
    :type value: str
    """
    if value.lower() in ['t', 'true']:
        value = True
    elif value.lower() in ['f', 'false']:
        value = False
    elif str.isdigit(str(value)):
        value = int(value) > 0
    else:
        value = str(value)
    return value


def get_arguments(func, create=False):
    """
    Ritorna le opzioni di una funzione se ci sono o None

    :param func: Funzione da analizzare.
    :type func: function
    :param create: Indica se creare la lista di opzioni in caso non ci siano.
    :type create: bool
    """
    # Se non è un tipo di funzione valido ritorno direttamente None.
    if not isinstance(func, (
            types.FunctionType, types.MethodType, staticmethod, classmethod)):
        return None
    # Se *func* è un metodo statico le opzioni sono dentro __func__
    if isinstance(func, staticmethod):
        try:
            arguments = func.__func__.__arguments__
        except AttributeError:
            if create:
                arguments = func.__func__.__arguments__ = []
            else:
                arguments = None
    else:
        try:
            arguments = func.__arguments__
        except AttributeError:
            if create:
                arguments = func.__arguments__ = []
            else:
                arguments = None
    return arguments
