# -*- coding: utf-8 -*-
"""
=============================
Commands :mod:`pets.commands`
=============================
"""
import os
from os.path import dirname
from importlib import import_module
from argparseinator import ArgParseInated
from argparseinator import arg
from argparseinator import class_args


@class_args
class Commands(ArgParseInated):
    """Commands for pets"""

    @arg()
    def allsays(self):
        """Asks all pets to say something"""
        # cycle in the main dir
        for name in os.listdir(dirname(dirname(__file__))):
            # try to import the module and say something.
            try:
                mod = import_module(name)
                mod.commands.Commands(__argpi__).say()
            except (ImportError, AttributeError):
                # just pass in case of these errors
                pass
    @arg()
    def allnames(self):
        """Asks all pets their names"""
        # cycle in the main dir
        for name in os.listdir(dirname(dirname(__file__))):
            # try to import the module and say something.
            try:
                mod = import_module(name)
                mod.commands.Commands(__argpi__).name()
            except (ImportError, AttributeError):
                # just pass in case of these errors
                pass
