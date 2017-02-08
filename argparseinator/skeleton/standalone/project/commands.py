# -*- coding: utf-8 -*-
"""
{-wholetitlemark-}
{-wholetitle-}
{-wholetitlemark-}
"""
from argparseinator import ArgParseInated
from argparseinator import arg
from argparseinator import class_args


@class_args
class Commands(ArgParseInated):
    """Commands for {-prj_name-}"""

    @arg("word", help="The word", nargs="?", default="bird")
    def say(self, word):
        """says the word"""
        writeln("i said", word)
