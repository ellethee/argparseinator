#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Argparseinator.
    silly but funny thing thats can help you to manage argparse and functions
"""
__file_name__ = "__init__.py"
__author__ = "luca"
__version__ = "1.0.0"
__date__ = "2014-10-23"

import argparse
from argparseinator import utils
from argparseinator import exceptions
import sys
import types


class ArgParserInator(object):
    """
    ArgParserInator class.

    """
    __metaclass__ = utils.Singleton
    _output = sys.stdout
    parser = None
    _is_parsed = False
    _single = False
    never_single = False
    new_attrs = {}
    # commands
    commands = {}
    # subparsers
    subparsers = None
    # parsed arguments
    args = None
    # authorizations
    auths = {}
    # authorization phrase
    auth_phrase = None

    def __init__(
            self, auth_phrase=None, never_single=False, args=None,
            add_output=False, **kwargs):
        if self.parser is None:
            self.auth_phrase = auth_phrase
            self.never_single = never_single
            formatter_class = kwargs.get(
                'formatter_class', utils.SubcommandHelpFormatter)
            kwargs.update({
                'conflict_handler': 'resolve',
                'formatter_class': formatter_class,
            })
            # create the parser
            self.parser = argparse.ArgumentParser(**kwargs)
            if add_output:
                from argparse import FileType
                self.parser.add_argument(
                    '-o', '--output', type=FileType('wb'),
                    help="Output to file")
            # let's add parser arguments if we have them
            if args is not None:
                for aargs, akargs in args:
                    self.parser.add_argument(*aargs, **akargs)

    def _compile(self):
        """
        Compile functions for argparsing.
        """
        if self.auths:
            self.parser.add_argument(
                '--auth',
                help="Authorization phrase for special commands.")
        if len(self.commands) == 1 and self.never_single is False:
            func = self.commands.values()[0]
            for args, kwargs in func.__arguments__:
                self.parser.add_argument(*args, **kwargs)
            self._single = func
        else:
            self._single = None
            self.subparsers = self.parser.add_subparsers(
                title='Comandi', dest='command',
                description="Comandi validi per %(prog)s.")
            for func in self.commands.values():
                parser = utils.get_parser(func, self.subparsers)
                if func.__subcommands__:
                    sub_parser = parser.add_subparsers(
                        title="Sottocomandi", dest='subcommand',
                        description='Comandi di %s' % func.__subname__,
                        help=func.__doc__)
                    for sub_func in func.__subcommands__.values():
                        utils.get_parser(sub_func, sub_parser, func)

    def parse_args(self):
        """
        Parse our arguments.
        """
        self._compile()
        self.args = self.parser.parse_args()
        # set up the output.
        if 'output' in self.args and self.args.output is not None:
            self._output = self.args.output
        self._is_parsed = True

    def check_auth(self, name):
        """
        Verifica l'autorizzazione per il comando.
        """
        if name in self.auths:
            auth = self.auths[name]
            if self.args.auth is None:
                print "Autorizzazione richiesta per il comando %s" % (
                    self.args.command)
                return False
            elif ((auth is True and self.args.auth != self.auth_phrase) or
                  (auth is not True and self.args.auth != auth)):
                print "Autorizzazione non valida"
                return False
        return True

    def chek_command(self, **kwargs):
        """
        Verifica se e' stata passata un'azione valida nella riga di comando
        e in caso positivo la esegue passando i parametri e restituiendone
        il risultato.

        :return: (Any) Ritorna il risultato della funzione chiamata, se
            previsto, altrimenti None.
        """
        # let's parse arguments if we didn't before.
        if not self._is_parsed:
            self.parse_args()
        self.new_attrs.update(**kwargs)
        # Recuperiamo il comando.
        if not self.commands:
            raise exceptions.ArgParseInatorNoCommandsFound
        elif self._single:
            func = self._single
        else:
            func = self.commands[self.args.command]
        # Vediamo se abbiamo un sottocomando e in caso lo impostiamo
        if func.__subcommands__ is not None:
            subcommand = func.__subcommands__[self.args.subcommand]
        # Altrimenti vediamo se abbiamo un metodo e impostiamo quello come
        # sottocomando.
        else:
            subcommand = func
        # Verifichiamo l'autorizzazione.
        if not self.check_auth(id(subcommand)):
            return 0
        # Se abbiamo una classe la utilizziamo per chiamare il comando
        if func.__cls__ is not None:
            try:
                # Proviamo ad instanziare la classe passando self come
                # argomento.
                return subcommand(func.__cls__(self), self.args)
            except TypeError:
                # Se da un errore instaziamo la classe senza parametri.
                return subcommand(func.__cls__(), self.args)
        # Se non abbiamo la classe chiamiamo direttamente la funzione.
        else:
            return subcommand(self.args)

    def write(self, *string):
        """
        Scrive sull'output o sullo STDOUT.
        """
        self._output.write(' '.join([
            ' ' * s if isinstance(s, int) else s for s in string]))

    def writeln(self, *string):
        """
        Scrive una riga sull'output o sullo STDOUT.
        """
        self._output.write(' '.join([
            ' ' * s if isinstance(s, int) else s for s in string]) + '\n')


def arg(*args, **kwargs):
    """
    Decora una funzione o un metodo di classe per aggiungerlo ai parser degli
    argomenti.
    """
    def decorate(func):
        """
        Docora la funzione.
        """
        if utils.check_class() is not None:
            arguments = utils.get_arguments(func, True)
            if len(args):
                arguments.append((args, kwargs))
        elif isinstance(func, types.FunctionType):
            ap_ = ArgParserInator()
            if func.__name__ not in ap_.commands:
                func.__arguments__ = []
                func.__subcommands__ = None
                func.__cls__ = None
                ap_.commands[func.__name__] = func
            if len(args) or len(kwargs):
                func.__arguments__.append((args, kwargs,))
        return func
    return decorate


def class_args(cls):
    """
    Decora una classe *preparandola* per gestire il parser di argomenti.
    """
    ap_ = ArgParserInator()
    if hasattr(cls, '__subname__'):
        if cls.__subname__ not in ap_.commands:
            cls.__subcommands__ = {}
            utils.get_arguments(cls, True)
            cls.__cls__ = cls
            for name, func in cls.__dict__.iteritems():
                arguments = utils.get_arguments(func)
                if arguments is not None:
                    cls.__subcommands__[name] = func
            ap_.commands[cls.__subname__] = cls
    else:
        for name, func in cls.__dict__.iteritems():
            if name not in ap_.commands:
                arguments = utils.get_arguments(func)
                if arguments is not None:
                    func.__cls__ = cls
                    func.__subcommands__ = None
                    ap_.commands[name] = func
    return cls


def ap_arg(*args, **kwargs):
    """
    Semplice funzione per ritornare una tupla per l'add_argument del parser.
    """
    return args, kwargs


def cmd_auth(auth_phrase=None):
    """
    Imposta l'autorizzazione per un comando o sottocomando.
    """
    def decorate(func):
        """
        Decora la funzione.
        """
        ap_ = ArgParserInator()
        auth_name = id(func)
        if auth_phrase is None:
            ap_.auths[auth_name] = True
        else:
            ap_.auths[auth_name] = str(auth_phrase)
        return func
    return decorate
