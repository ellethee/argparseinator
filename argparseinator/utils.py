#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Some util.
"""
__file_name__ = "utils.py"
__author__ = "luca"
__version__ = "1.0.0"
__date__ = "2014-10-23"

import argparse
import inspect
import os
import glob
import sys
import platform

SYSTEM = platform.system()
IS_WINDOWS = 'windows' in SYSTEM.lower()
IS_LINUX = 'linux' in SYSTEM.lower()
IS_FROZEN = hasattr(sys, 'frozen')
IS_WIN_FROZEN = getattr(sys, 'frozen', '') == "windows_exe"

COMMANDS_LIST_TITLE = "Commands"
COMMANDS_LIST_DESCRIPTION = "Commands for %(prog)s"
SUBCOMMANDS_LIST_TITLE = "Sub Commands"
SUBCOMMANDS_LIST_DESCRIPTION = "Sub commands for {}"


class SillyClass(object): # pylint: disable=too-few-public-methods
    """
    SIlly class.
    """
    __shared_arguments__ = []
    __arguments__ = []
    __cls_name__ = ''

    def __init__(self, **kwargs):
        # set all parameters
        self.__dict__.update(**kwargs)


class Singleton(type):
    """
    Singleton metaclass.
    """
    _instances = {}

    def __call__(cls, *args, **kwa):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwa)
        elif getattr(cls, '__reinit__', False):
            cls._instances[cls].__init__(*args, **kwa)
        return cls._instances[cls]


class SubcommandHelpFormatter(argparse.RawDescriptionHelpFormatter):
    """
    Help Formatter
    """
    def _format_action(self, action):
        parts = super(SubcommandHelpFormatter, self)._format_action(action)
        if action.nargs == argparse.PARSER:
            parts = "\n".join(parts.split("\n")[1:])
        return parts


def check_class():
    """
    Return the class name for the current frame.
    If the result is ** None ** means that the call is made from a module.
    """
    # get frames
    frames = inspect.stack()
    cls = None
    # should be the third frame
    # 0: this function
    # 1: function/decorator
    # 2: class that contains the function
    if len(frames) > 2:
        frame = frames[2][0]
        if '__module__' in frame.f_code.co_names:
            cls = SillyClass(**frame.f_locals)
            cls.__cls_name__ = frame.f_code.co_name
    return cls


def collect_appendvars(ap_, cls):
    """
    colleziona elementi per le liste.
    """
    for key, value in cls.__dict__.items():
        if key.startswith('appendvars_'):
            varname = key[11:]
            if varname not in ap_.appendvars:
                ap_.appendvars[varname] = []
            if value not in ap_.appendvars[varname]:
                if not isinstance(value, list):
                    value = [value]
                ap_.appendvars[varname] += value


def isglob(value):
    """
    Windows non traduce automaticamente i wildchars così lo facciamo
    a mano tramite glob.

    :param value: Espressione glob per la lista dei files.
    :type value: str
    """
    if os.name == 'nt':
        if isinstance(value, basestring):
            value = glob.glob(value)
    return value


def string_or_bool(value):
    """
    Ritorna True o False in caso venga passata la stringa 'true' o 'false'
    (o 't' o 'f') altrimenti ritorna una stringa.

    :param value: Stringa da analizzare.
    :type value: str
    """
    if value.lower() in ['t', 'true']:
        value = True
    elif value.lower() in ['f', 'false']:
        value = False
    elif str.isdigit(str(value)):
        value = int(value) != 0
    else:
        value = str(value) # pylint: disable=redefined-variable-type
    return value


def has_shared(arg, shared):
    """
    Verifica se ci sono shared.
    """
    try:
        if isinstance(shared, list):
            shared_arguments = shared
        else:
            shared_arguments = shared.__shared_arguments__
        for idx, (args, kwargs) in enumerate(shared_arguments):
            arg_name = kwargs.get(
                'dest', args[-1].lstrip('-').replace('-', '_'))
            if arg_name == arg:
                return idx
        idx = False
    except (ValueError, AttributeError):
        idx = False
    return idx


def has_argument(arg, arguments):
    """
    Verifica se ci sono argument con la classe.
    """
    try:
        if not isinstance(arguments, list):
            arguments = arguments.__arguments__
        for idx, (args, kwargs) in enumerate(arguments):
            arg_name = kwargs.get(
                'dest', args[-1].lstrip('-').replace('-', '_'))
            if arg_name == arg:
                return idx
        idx = False
    except (ValueError, AttributeError):
        idx = False
    return idx


def get_functarguments(func):
    """
    Recupera gli argomenti dalla funzione stessa.
    """
    argspec = inspect.getargspec(func)
    if argspec.defaults is not None:
        args = argspec.args[:-len(argspec.defaults)]
        kwargs = dict(
            zip(argspec.args[-len(argspec.defaults):], argspec.defaults))
    else:
        args = argspec.args
        kwargs = {}
    if args and args[0] == 'self':
        args.pop(0)
    func.__named__ = []
    arguments = []
    shared = get_shared(func)
    for arg in args:
        if has_shared(arg, shared) is not False:
            continue
        if has_argument(arg, func.__cls__) is not False:
            continue
        arguments.append(([arg], {}, ))
        func.__named__.append(arg)
    for key, val in kwargs.items():
        if has_shared(key, shared) is not False:
            continue
        if has_argument(key, func.__cls__) is not False:
            continue
        if isinstance(val, dict):
            flags = [val.pop('lflag', '--%s' % key)]
            short = val.pop('flag', None)
            dest = val.get('dest', key).replace('-', '_')
            if short:
                flags.insert(0, short)
        else:
            flags = ['--%s' % key]
            val = dict(default=val)
            dest = key.replace('-', '_')
        func.__named__.append(dest)
        arguments.append((flags, val, ))
    return arguments


def get_parser(func, parent):
    """
    Imposta il parser.
    """
    parser = parent.add_parser(func.__cmd_name__, help=func.__doc__)
    exc_grps = {}
    for args, kwargs in func.__arguments__:
        exc_grp = kwargs.pop("exc_grp", None)
        if exc_grp:
            if isinstance(exc_grp, (list, tuple)):
                name, required = exc_grp
            else:
                name, required = exc_grp, False
            if not name in exc_grps:
                exc_grps[name] = parser.add_mutually_exclusive_group(
                    required=required)
            exc_grps[name].add_argument(*args, **kwargs)
        else:
            parser.add_argument(*args, **kwargs)
    return parser


def get_shared(func):
    """
    return shared.
    """
    shared = []
    if not hasattr(func, '__cls__'):
        return shared
    if not hasattr(func.__cls__, '__shared_arguments__'):
        return shared
    if hasattr(func, '__no_share__'):
        if func.__no_share__ is True:
            return shared
        else:
            shared += [
                s for s in func.__cls__.__shared_arguments__
                if (s[0][-1].replace('--', '').replace('-', '_'))
                not in func.__no_share__]
    else:
        shared = func.__cls__.__shared_arguments__
    return shared


def set_subcommands(func, parser):
    """
    Set subcommands.
    """
    if hasattr(func, '__subcommands__') and func.__subcommands__:
        sub_parser = parser.add_subparsers(
            title=SUBCOMMANDS_LIST_TITLE, dest='subcommand',
            description=SUBCOMMANDS_LIST_DESCRIPTION.format(
                func.__cmd_name__),
            help=func.__doc__)
        for sub_func in func.__subcommands__.values():
            parser = get_parser(sub_func, sub_parser)
            for args, kwargs in get_shared(sub_func):
                parser.add_argument(*args, **kwargs)
    else:
        for args, kwargs in get_shared(func):
            parser.add_argument(*args, **kwargs)


def check_help():
    """
    check know args in argv.
    """
    # know arguments
    know = set(('-h', '--help', '-v', '--version'))
    # arguments
    args = set(sys.argv[1:])
    # returns True if there is at least one known argument in arguments
    return len(know.intersection(args)) > 0
