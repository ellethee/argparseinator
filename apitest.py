#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    ArgParserInator test
"""
__file_name__ = "apitest.py"
__author__ = "luca"
__version__ = "1.0.0"
__date__ = "2014-11-18"


from argparseinator import ArgParserInator, arg, class_args, cmd_auth, ap_arg


AP = ArgParserInator(
    description="Silly script",
    #add_output=True,
    #auth_phrase="t",
)
_ = AP.writeln


@arg("name", help="Name to print")
def print_name(args):
    """
    Print name.
    """
    print "Printing the name...", args.name


#@arg("fliename", help="File name", nargs="*")
#@cmd_auth()
#def lista(args):
#    """
#    list files.
#    """
#    for fil in ('luca', 'luigi', 'filippo'):
#        _(fil)


#@arg("fliename", help="File name", nargs="*")
#@cmd_auth('luca')
#def lista2(args):
#    """
#    list files.
#    """
#    for fil in ('luca', 'luigi', 'filippo'):
#        AP.writeln(fil)


#@class_args
#class Prova(object):
#    """
#    Classe di prova.
#    """

#    @arg("name", help="Test coso")
#    def clslist(self, args):
#        """
#        cls test.
#        """
#        AP.writeln("cls test")


#@class_args
#class Prova2(object):
#    """
#    Classe di prova.
#    """
#    __subname__ = "mario"
#    __arguments__ = [
#        ap_arg('-j', '--jump', help="Salta il coso", action="store_true")
#    ]
#    __shared_arguments__ = [
#        ap_arg('-k', '--kill', help="killa il coso", action="store_true")
#    ]

#    @arg("name", help="Test coso")
#    def clslist2(self, args):
#        """
#        cls test.
#        """
#        AP.writeln("cls test")

if __name__ == "__main__":
    AP.chek_command()
