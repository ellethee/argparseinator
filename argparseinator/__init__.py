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
    new_attrs = {}
    # commands
    commands = {}
    # parsed arguments
    args = None
    # authorizations
    auths = {}
    # authorization phrase
    auth_phrase = None

    def __init__(self, **kwargs):
        if self.parser is None:
            self.auth_phrase = kwargs.pop('auth', None)
            #: parser wide arguments (if any)
            ap_args = kwargs.pop('args', None)
            # set some default.
            kwargs.update({
                'conflict_handler': 'resolve',
                'formatter_class': (
                    kwargs.get('formatter_class') or
                    utils.SubcommandHelpFormatter),
            })
            # create the parser
            self.parser = argparse.ArgumentParser(**kwargs)
            # if we defined an authorization phrase set up the parametr
            if self.auth_phrase is not None:
                self.parser.add_argument(
                    '--auth',
                    help="Authorization phrase for special commands.")
            add_output = kwargs.pop('add_output', False)
            if add_output:
                from argparse import FileType
                self.parser.add_argument(
                    '-o', '--output', type=FileType('wb'),
                    help="Output to file")
            # let's add parser arguments if we have them
            if ap_args is not None:
                for aargs, akargs in ap_args:
                    self.parser.add_argument(*aargs, **akargs)
            # self.subparsers = self.parser.add_subparsers(
                # title='Comandi', dest='command',
                # description="Comandi validi per %(prog)s.")

    def parse_args(self):
        """
        Parse our arguments.
        """
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
        if not self.args.commands and len(self.commands) == 1:
            act = self.commands.values()[0]
        else:
            act = self.commands[self.args.command]
        # Vediamo se abbiamo un sottocomando e in caso lo impostiamo
        if act.subcommands is not None:
            subcommand = act.subcommands[self.args.subcommand]
        # Altrimenti vediamo se abbiamo un metodo e impostiamo quello come
        # sottocomando.
        elif act.method is not None:
            subcommand = act.method
        # Se non troviamo nulla diamo un errore di comando non valido.
        else:
            raise exceptions.ArgParseInatorInvalidCommand
        # Verifichiamo l'autorizzazione.
        if not self.check_auth(id(subcommand)):
            return 0
        # Se abbiamo una classe la utilizziamo per chiamare il comando
        if act.cls is not None:
            try:
                # Proviamo ad instanziare la classe passando self come
                # argomento.
                return subcommand(act.cls(self), self.args)
            except TypeError:
                # Se da un errore instaziamo la classe senza parametri.
                return subcommand(act.cls(), self.args)
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
            options = utils.get_options(func, True)
            if len(args):
                options.append((args, kwargs))
        elif isinstance(func, types.FunctionType):
            esa = ArgParserInator()
            if func.__name__ not in esa.commands:
                esa.commands[func.__name__] = dict(
                    method=func,
                    # argp_params=(
                    #     func.__name__, help=func.__doc__,
                    #     conflict_handler='resolve',),
                    args=args,
                    kwargs=kwargs)
        # if len(args) or len(kwargs):
        #     esa.commands[func.__name__].argp.add_argument(*args, **kwargs)
            # func.arguments = esa.commands[func.__name__].argp
        return func
    return decorate
