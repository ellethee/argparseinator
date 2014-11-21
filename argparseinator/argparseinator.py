# -*- coding: utf-8 -*-
"""
    Argparseinator
"""
__file_name__ = "ep_decorators.py"
__author__ = "luca"
__version__ = "1.0.0"
__date__ = "2013-07-26"


import sys
import argparse
from .classes import EteDumbObj, Singleton
import types
import exceptions
import utils


class ArgParseInatorBase(object):
    """
    Classe di default per la gestione delle classi **argomentate**.

    :param epsubargs: riferimento alla classe ArgParseInator di base.
    :type epsubargs: ArgParseInator
    """

    def __init__(self, epsubargs):
        self.args = epsubargs.args
        self.logger = epsubargs.logger
        self.log = self.logger
        self.write = epsubargs.write
        self.writeln = epsubargs.writeln
        self.__dict__.update(epsubargs.new_attrs)
        self.__prepare__()

    def __prepare__(self):
        """
        Funzione di preparazione dopo l'init, da overloadare in caso di
        utilizzo.
        """
        pass




def ap_arg(*args, **kwargs):
    """
    Semplice funzione per ritornare una tupla per l'add_argument del parser.

    :param args: Argomenti compatibili con
        argparse.ArgumentParser.add_argument_
    :type args: list
    :param kwargs: Argomenti compatibili con
        argparse.ArgumentParser.add_argument_
    :type kwargs: dict
    :return: una tupla contenente args e kwargs.
    :rtype: tuple
    """
    return args, kwargs


def arg(*args, **kwargs):
    """
    Decora una funzione o un metodo di classe per aggiungerlo ai parser degli
    argomenti.

    :param args: Argomenti compatibili con
        argparse.ArgumentParser.add_argument_
    :type args: list
    :param kwargs: Argomenti compatibili con
        argparse.ArgumentParser.add_argument_
    :type kwargs: dict

    .. code:: python

        @arg('stringa', help="Stringa da stampare")
        def print_string(args):
            print args.stringa

    Il nome della funzione diventerà il nome del comando da eseguire

    .. code-block:: bash

        $ script.py <nome_funzione> [options] [arguments]
        # Quindi...
        $ script.py print_string "Ciao Mondo"

    Se il metodo decorato è un metodo di classe e la classe ha specificato
    la proprieta *nome* (vedi :func:`class_args`) allora il nome della
    funzione sarà il sottocomando::

        script.py <nome_classe> <nome_funzione> [options] [arguments]

    .. note::

        L'ordine in una sequeza di :func:`arg` è significativo;
        gli argomenti più vicini alla definizione della funzione saranno
        i primi in ordine di parsing.
    """
    def decorate(func):
        """
        Docora la funzione.
        """
        if check_class() is not None:
            options = get_options(func, True)
            if len(args):
                options.append((args, kwargs))
        elif isinstance(func, types.FunctionType):
            esa = ArgParseInator()
            if func.__name__ not in esa.commands:
                esa.commands[func.__name__] = EteDumbObj(
                    method=func,
                    argp=esa.subparsers.add_parser(
                        func.__name__, help=func.__doc__,
                        conflict_handler='resolve'))
            if len(args) or len(kwargs):
                esa.commands[func.__name__].argp.add_argument(*args, **kwargs)
            func.arguments = esa.commands[func.__name__].argp
        return func
    return decorate


def cmd_auth(auth_phrase=None):
    """
    Imposta l'autorizzazione per un comando o sottocomando.

    :param auth_phrase: frase di autorizzazione o None per usare quella
        predefinita.
    :type auth_phrase: str

    .. code:: python

        @arg('stringa', help="Stringa da stampare")
        @cmd_auth('mario')
        def print_string(args):
            print args.stringa

    .. code-block:: bash

        $ script.py print_string "Ciao Mondo"
        Autorizzazione richiesta per il comando print_string
        $ script.py --auth=mario print_string "Ciao Mondo"
        Ciao Mondo
    """
    def decorate(func):
        """
        Decora la funzione.
        """
        esa = ArgParseInator()
        auth_name = id(func)
        if auth_phrase is None:
            esa.auths[auth_name] = True
        else:
            esa.auths[auth_name] = str(auth_phrase)
        return func
    return decorate


def class_args(cls):
    """
    Decora una classe *preparandola* per gestire il parser di argomenti.

    Nella definizione della classe si puo decidere se specificare la
    proprità *name* che indica il nome del *comando*; di conseguenza
    il nome sarà il comando mentre le funzioni diventeranno
    sottocomandi.

    **con nome**

    .. code:: python

        @class_args
        class ConNome(object):
            name = 'test'
            @arg('stringa')
            def stampa_stringa(self, args):
                print args.stringa

    .. code-block:: bash

        $ script.py test stampa_stringa "Ciao Mondo"
        Ciao Mondo

    **senza nome**

    .. code:: python

        @class_args
        class SenzaNome(object):
            @arg('stringa')
            def stampa_stringa(self, args):
                print args.stringa

    .. code-block:: bash

        $ script.py stampa_stringa "Ciao Mondo"
        Ciao Mondo

    """
    esa = ArgParseInator()
    if hasattr(cls, 'service'):
        esa.services.append(cls.service)
    if hasattr(cls, 'name'):
        parser = esa.subparsers.add_parser(
            cls.name, help=cls.__doc__, conflict_handler='resolve')
        if hasattr(cls, 'args'):
            for aargs, akargs in cls.args:
                parser.add_argument(*aargs, **akargs)
        subparser = parser.add_subparsers(
            title="Sottocomandi",
            dest='subcommand',
            description='Comandi di %s' % cls.name,
            help=cls.__doc__)
        esa.commands[cls.name] = EteDumbObj(subcommands={}, cls=cls)
        subcommands = esa.commands[cls.name].subcommands
        for name, method in cls.__dict__.iteritems():
            options = utils.get_options(method)
            if options is not None:
                subcommands[name] = method
                argp = subparser.add_parser(
                    name, help=method.__doc__,
                    conflict_handler='resolve')
                if hasattr(cls, 'sub_args'):
                    for aargs, akargs in cls.sub_args:
                        argp.add_argument(*aargs, **akargs)
                for args, kwargs in options:
                    argp.add_argument(*args, **kwargs)
    else:
        for name, method in cls.__dict__.iteritems():
            options = get_options(method)
            if options is not None:
                esa.commands[name] = EteDumbObj(method=method, cls=cls)
                argp = esa.subparsers.add_parser(
                    name, help=method.__doc__,
                    conflict_handler='resolve')
                if hasattr(cls, 'sub_args'):
                    for aargs, akargs in cls.sub_args:
                        argp.add_argument(*aargs, **akargs)
                for args, kwargs in options:
                    argp.add_argument(*args, **kwargs)
    return cls
