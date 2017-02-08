# -*- coding: utf-8 -*-
"""
=============================
Commands :mod:`bird.commands`
=============================
"""
from argparseinator import ArgParseInated
from argparseinator import arg
from argparseinator import class_args


@class_args
class Commands(ArgParseInated):
    """Commands for bird"""

    @arg("word", help="The word", nargs="?", default="bird")
    def say(self, word="bird"):
        """says the word"""
        writeln("I tweet", word)

    @arg()
    def name(self):
        """The pet name"""
        writeln("Polly")
