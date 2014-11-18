#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    ArgParserInator test
"""
__file_name__ = "apitest.py"
__author__ = "luca"
__version__ = "1.0.0"
__date__ = "2014-11-18"


from argparseinator import ArgParserInator, arg, class_args


AP = ArgParserInator(description="ArgParserInator test")


@arg("fliename", help="File name", nargs="*")
def lista(args):
    """
    list files.
    """
    for fil in ('luca', 'luigi', 'filippo'):
        print fil


@arg("fliename", help="File name", nargs="*")
def lista2(args):
    """
    list files.
    """
    for fil in ('luca', 'luigi', 'filippo'):
        print fil


@class_args
class Prova(object):
    """
    Classe di prova.
    """

    @arg("name", help="Test coso")
    def clslist(self, args):
        """
        cls test.
        """
        print "cls test"


@class_args
class Prova2(object):
    """
    Classe di prova.
    """
    __subname__ = "mario"

    @arg("name", help="Test coso")
    def clslist2(self, args):
        """
        cls test.
        """
        print "cls test"

if __name__ == "__main__":
    AP.chek_command()
