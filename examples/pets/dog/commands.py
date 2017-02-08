# -*- coding: utf-8 -*-
"""
============================
Commands :mod:`dog.commands`
============================
"""
from argparseinator import ArgParseInated
from argparseinator import arg
from argparseinator import class_args


@class_args
class Commands(ArgParseInated):
    """Commands for dog"""

    @arg("word", help="The word", nargs="?", default="dog")
    def say(self, word="dog"):
        """says the word"""
        writeln("I woof", word)

    @arg()
    def name(self):
        """The pet name"""
        writeln("Walle")
