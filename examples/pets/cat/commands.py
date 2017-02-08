# -*- coding: utf-8 -*-
"""
============================
Commands :mod:`cat.commands`
============================
"""
from argparseinator import ArgParseInated
from argparseinator import arg
from argparseinator import class_args


@class_args
class Commands(ArgParseInated):
    """Commands for cat"""

    @arg("word", help="The word", nargs="?", default="cat")
    def say(self, word="cat"):
        """says the word"""
        writeln("I miaow", word)

    @arg()
    def name(self):
        """The pet name"""
        writeln("Fuffy")
