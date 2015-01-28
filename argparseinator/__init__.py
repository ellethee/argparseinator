#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    ArgParseInator.
    silly but funny thing thats can help you to manage argparse and functions
"""
__file_name__ = "__init__.py"
__author__ = "luca"
__version__ = "1.0.0"
__date__ = "2014-10-23"

from gettext import gettext as _
import argparse
from argparseinator import utils
from argparseinator import exceptions
import sys
import types
import inspect
from os import linesep
import os
import gettext


class ArgParseInated(object):
    """
        Class for deriving from
    """

    def __init__(self, parseinator, **new_attributes):
        self.__dict__.update(**new_attributes)
        self.args = parseinator.args
        self.write = parseinator.write
        self.writeln = parseinator.writeln
        self.__preinator__()

    def __preinator__(self):
        """
        Funzione di preparazione dopo l'init, da overloadare in caso di
        utilizzo.
        """
        pass


class ArgParseInator(object):
    """
    ArgParseInator class.

    """
    __metaclass__ = utils.Singleton
    _output = sys.stdout
    parser = None
    _is_parsed = False
    _single = False
    add_output = False
    never_single = False
    formatter_class = argparse.RawDescriptionHelpFormatter
    args = None
    argparse_args = {}
    # commands
    commands = {}
    # subparsers
    subparsers = None
    # parsed arguments
    ap_args = None
    # authorizations
    auths = {}
    # authorization phrase
    auth_phrase = None
    # write name
    write_name = "write"
    # write line name
    write_line_name = 'writeln'
    # auto_exit
    auto_exit = False
    cmd_name = None
    default_cmd = None

    def __init__(
            self, add_output=None, args=None, auth_phrase=None,
            never_single=None, formatter_class=None, write_name=None,
            write_line_name=None, auto_exit=None, default_cmd=None,
            **argparse_args):
        self.auth_phrase = auth_phrase or self.auth_phrase
        self.never_single = never_single or self.never_single
        self.add_output = add_output or self.add_output
        self.ap_args = args or self.ap_args
        self.auto_exit = auto_exit or self.auto_exit
        self.argparse_args.update(**argparse_args)
        self.formatter_class = formatter_class or self.formatter_class
        self.write_name = write_name or self.write_name
        self.write_line_name = write_line_name or self.write_line_name
        self.default_cmd = default_cmd or self.default_cmd

    def _compile(self):
        """
        Compile functions for argparsing.
        """
        gettext.install("argparseinator", os.path.join(
            os.path.dirname(__file__), 'locale'))
        frm = inspect.stack()[-1]
        mod = inspect.getmodule(frm[0])
        version = getattr(mod, '__version__', None)
        if version:
            self.argparse_args['version'] = (
                self.argparse_args.get('version') or version)
        self.parser = argparse.ArgumentParser(
            formatter_class=self.formatter_class, **self.argparse_args)
        if self.add_output:
            self.parser.add_argument(
                '-o', '--output', metavar="FILE", help="Output to file")
        if self.ap_args is not None:
            for aargs, akargs in self.ap_args:
                self.parser.add_argument(*aargs, **akargs)
        if self.auths:
            self.parser.add_argument(
                '--auth',
                help="Authorization phrase for special commands.")
        if len(self.commands) == 1 and self.never_single is False:
            func = self.commands.values()[0]
            for args, kwargs in func.__arguments__:
                self.parser.add_argument(*args, **kwargs)
            self._single = func
            if not self.parser.description:
                self.parser.description = _(func.__doc__)
            else:
                self.parser.description += linesep + _(func.__doc__)
            utils.set_subcommands(func, self.parser)
        else:
            self._single = None
            self.subparsers = self.parser.add_subparsers(
                title=_(utils.COMMANDS_LIST_TITLE), dest='command',
                description=_(utils.COMMANDS_LIST_DESCRIPTION))
            for func in self.commands.values():
                parser = utils.get_parser(func, self.subparsers)
                utils.set_subcommands(func, parser)

    def parse_args(self):
        """
        Parse our arguments.
        """
        self._compile()
        self.args = None
        if (len(sys.argv) > 1 and not utils.check_help() and self.default_cmd
                and sys.argv[1] not in self.commands):
            sys.argv.insert(1, self.default_cmd)
        self.args = self.parser.parse_args()
        # set up the output.
        if self.args:
            if 'output' in self.args and self.args.output is not None:
                import codecs
                self._output = codecs.open(
                    self.args.output, 'w', encoding='utf8')
            self._is_parsed = True

    def check_auth(self, name):
        """
        Verifica l'autorizzazione per il comando.
        """
        if name in self.auths:
            auth = self.auths[name]
            if self.args.auth is None:
                raise exceptions.ArgParseInatorAuthorizationRequired
            elif ((auth is True and self.args.auth != self.auth_phrase) or
                  (auth is not True and self.args.auth != auth)):
                raise exceptions.ArgParseInatorNotValidAuthorization
        return True

    def check_command(self, **new_attributes):
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
        # Recuperiamo il comando.
        if not self.commands:
            raise exceptions.ArgParseInatorNoCommandsFound
        elif self._single:
            func = self._single
        else:
            func = self.commands[self.args.command]

        # Vediamo se abbiamo un sottocomando e in caso lo impostiamo
        if func.__subcommands__ is not None:
            command = func.__subcommands__[self.args.subcommand]
        # Altrimenti vediamo se abbiamo un metodo e impostiamo quello come
        # sottocomando.
        else:
            command = func
        self.cmd_name = command.__cmd_name__
        # Verifichiamo l'autorizzazione.
        if not self.check_auth(id(command)):
            return 0
        # let's execute the command.
        return self._execute(func, command, **new_attributes)

    def _execute(self, func, command, **new_attributes):
        """
        Execute command.
        """
        arg_specs = inspect.getargspec(command)
        if arg_specs.defaults:
            count = len(arg_specs.defaults)
            args_names = arg_specs.args[:count]
            kwargs_name = arg_specs.args[count:]
        else:
            args_names = arg_specs.args
            kwargs_name = []
        pargs = []
        kwargs = {}
        for name in args_names:
            if name == 'args':
                pargs.append(self.args)
            elif name == 'self':
                if ArgParseInated in inspect.getmro(func.__cls__):
                    pargs.append(func.__cls__(self, **new_attributes))
                else:
                    pargs.append(func.__cls__())
            else:
                pargs.append(getattr(self.args, name))
        for name in kwargs_name:
            if name == 'args':
                kwargs[name] = self.args
            elif name in self.args:
                kwargs[name] = getattr(self.args, name)
        import __builtin__
        setattr(__builtin__, self.write_name, self.write)
        setattr(__builtin__, self.write_line_name, self.writeln)
        retval = command(*pargs, **kwargs)
        if self.auto_exit:
            if retval is None:
                raise TypeError("Return value must not be None")
            elif isinstance(retval, basestring):
                self.exit(0, retval)
            elif isinstance(retval, int):
                self.exit(retval)
            elif isinstance(retval, (tuple, list,)):
                self.exit(retval[0], retval[1])
            self.exit()
        else:
            return retval

    def write(self, *string):
        """
        Scrive sull'output o sullo STDOUT.
        """
        self._output.write(' '.join(string))

    def writeln(self, *string):
        """
        Scrive una riga sull'output o sullo STDOUT.
        """
        self._output.write(' '.join(string) + linesep)

    def exit(self, status=0, message=None):
        """
        Terminate the script.
        """
        self.parser.exit(status, message)


def arg(*args, **kwargs):
    """
    Decora una funzione o un metodo di classe per aggiungerlo ai parser degli
    argomenti.
    """
    def decorate(func):
        """
        Docora la funzione.
        """
        func.__cmd_name__ = kwargs.pop('cmd_name', func.__name__)
        if utils.check_class() is not None:
            arguments = utils.get_arguments(func, True)
            if len(args):
                arguments.append((args, kwargs))
        elif isinstance(func, types.FunctionType):
            ap_ = ArgParseInator()
            if func.__cmd_name__ not in ap_.commands:
                func.__arguments__ = utils.get_functarguments(func)
                func.__subcommands__ = None
                func.__cls__ = None
                ap_.commands[func.__cmd_name__] = func
            if len(args) or len(kwargs):
                idx = None
                try:
                    idx = func.__named__.index(args[-1])
                except IndexError:
                    pass
                if idx is not None:
                    func.__arguments__[idx] = (args, kwargs,)
                else:
                    func.__arguments__.append((args, kwargs,))
        return func
    return decorate


def class_args(cls):
    """
    Decora una classe *preparandola* per gestire il parser di argomenti.
    """
    ap_ = ArgParseInator()
    if hasattr(cls, '__cmd_name__'):
        if cls.__cmd_name__ not in ap_.commands:
            cls.__subcommands__ = {}
            cls.__arguments__ = []
            utils.get_arguments(cls, True, cls)
            cls.__cls__ = cls
            for name, func in cls.__dict__.iteritems():
                arguments = utils.get_arguments(func)
                if arguments is not None:
                    cls.__subcommands__[name] = func
            ap_.commands[cls.__cmd_name__] = cls
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
        ap_ = ArgParseInator()
        auth_name = id(func)
        if auth_phrase is None:
            ap_.auths[auth_name] = True
        else:
            ap_.auths[auth_name] = str(auth_phrase)
        return func
    return decorate


def import_commands(commands_folder):
    """
    Imports commands modules for the script.
    """
    import importlib
    import os
    commands = os.path.split(commands_folder)[1]
    for filename in os.listdir(commands_folder):
        mod_name = os.path.splitext(filename)[0]
        try:
            importlib.import_module("{}.{}".format(commands, mod_name))
        except ImportError as err:
            print err
