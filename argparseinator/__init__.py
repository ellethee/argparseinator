# -*- coding: utf-8 -*-
"""
    ArgParseInator.
    silly but funny thing thats can help you to manage argparse and functions
"""
from __future__ import print_function
__file_name__ = "__init__.py"
__author__ = "luca"
__version__ = "1.0.13"
__date__ = "2014-10-23"

import sys
import types
import inspect
from os import linesep
import os
import argparse
from argparseinator import utils
from argparseinator import exceptions
EXIT_OK = 0


class ArgParseInated(object): # pylint: disable=too-few-public-methods
    """
    Class for deriving from
    """
    __shared_arguments__ = []
    __arguments__ = []

    def __init__(self, parseinator, **new_attributes):
        # update the class attributes
        self.__dict__.update(**new_attributes)
        # set the parseinator reference
        self.parseinator = parseinator
        # and some shortcut
        self.args = parseinator.args
        self.write = parseinator.write
        self.writeln = parseinator.writeln
        if parseinator.cfg_factory:
            # if we have a cfg_factory
            try:
                # we try to load a config with the factory
                self.cfg = parseinator.cfg_factory(parseinator.cfg_file)
            except StandardError as error:
                # if we have an exception we will rise an error.
                if parseinator.cfg_error:
                    # using the config.error function if we have one
                    parseinator.cfg_error(error, parseinator)
                else:
                    # or the oricinal exception
                    raise
        else:
            # else cfg will be None
            self.cfg = None
        # clall the initialization function
        self.__preinator__()

    def __preinator__(self):
        """
        Initialization to setup something at the __init__ end.
        """
        pass


class ArgParseInator(object): # pylint: disable=too-many-instance-attributes
    """
    ArgParseInator class.
    """
    # we will use a Singleton
    __metaclass__ = utils.Singleton
    __reinit__ = True
    # setup the standard output
    _output = sys.stdout
    # the main parser object
    parser = None
    # parsed status
    _is_parsed = False
    # single command
    _single = False
    add_output = False
    never_single = False
    # help formatter
    formatter_class = argparse.RawDescriptionHelpFormatter
    args = None
    argparse_args = {}
    # commands
    commands = {}
    # subparsers
    subparsers = None
    # parsed arguments
    ap_args = []
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
    msg_on_error_only = False
    cmd_name = None
    default_cmd = None
    setup = []
    appendvars = {}
    error = None
    cfg_file = None
    cfg_factory = None
    cfg_error = None
    # default encoding
    encoding = 'utf-8'

    def __init__( # pylint: disable=too-many-arguments
            self, add_output=None, args=None, auth_phrase=None,
            never_single=None, formatter_class=None, write_name=None,
            write_line_name=None, auto_exit=None, default_cmd=None,
            setup=None, ff_prefix=None, error=None, msg_on_error_only=None,
            config=None, skip_init=False,
            **argparse_args):
        if skip_init:
            return
        self.auth_phrase = auth_phrase or self.auth_phrase
        self.never_single = never_single or self.never_single
        self.add_output = add_output or self.add_output
        self.ap_args = args or self.ap_args
        self.auto_exit = auto_exit or self.auto_exit
        self.msg_on_error_only = msg_on_error_only or self.msg_on_error_only
        # get the main module
        mod = sys.modules['__main__']
        # setup the script version
        if hasattr(mod, '__version__'):
            version = "%(prog)s " + mod.__version__
            self.ap_args.append(
                ap_arg('-v', '--version', action='version', version=version))
        # setup the script description
        if 'description' not in argparse_args and hasattr(mod, '__doc__'):
            argparse_args['description'] = mod.__doc__
        if ff_prefix is True:
            argparse_args['fromfile_prefix_chars'] = '@'
        elif ff_prefix is not None:
            argparse_args['fromfile_prefix_chars'] = ff_prefix
        # update the arguments
        self.argparse_args.update(**argparse_args)
        # setup formatter clas
        self.formatter_class = formatter_class or self.formatter_class
        # setup the name for the write function
        self.write_name = write_name or self.write_name
        # setup the name for the writeln funcion
        self.write_line_name = write_line_name or self.write_line_name
        # setup the default command
        self.default_cmd = default_cmd or self.default_cmd
        # setup the setup function
        self.setup = setup or self.setup
        # setup the error functino
        self.error = error or self.error
        if isinstance(config, (list, tuple)):
            # if we have a config tuple/list
            # setup the config file
            self.cfg_file = config[0]
            # setup the config factory
            self.cfg_factory = config[1]
            if len(config) > 2:
                # if config has 3 elements setup the config error too
                self.cfg_error = config[2]


    def _compile(self):
        """
        Compile functions for argparsing.
        """
        # setup main parser
        self.parser = argparse.ArgumentParser(
            formatter_class=self.formatter_class, **self.argparse_args)
        if self.error:
            # setup the error method if we have one
            setattr(
                self.parser, 'error', types.MethodType(self.error, self.parser))
        if self.add_output:
            # add the output options if we have the add_output true
            self.parser.add_argument(
                '-o', '--output', metavar="FILE", help="Output to file")
            self.parser.add_argument(
                '--encoding', default="utf-8",
                help="Encoding for output file.")
        if self.cfg_factory:
            # if we have a config factory add the config options
            self.parser.add_argument(
                '-c', '--config', metavar="FILE", default=self.cfg_file,
                help="Configuration file (default %(default)s)")
        if self.ap_args is not None:
            # if we have argment parser args we will add them to the main parser
            for aargs, akargs in self.ap_args:
                self.parser.add_argument(*aargs, **akargs)
        if self.auths:
            # if we have authorizations enabled add the auth options
            self.parser.add_argument(
                '--auth',
                help="Authorization phrase for special commands.")
        if len(self.commands) == 1 and self.never_single is False:
            # if we have only one command ad never_single is False
            # setup the command as the only command.
            func = self.commands.values()[0]
            # add the arguments to the main parser
            for args, kwargs in func.__arguments__:
                self.parser.add_argument(*args, **kwargs)
            # shortcut for the single command
            self._single = func
            if not self.parser.description:
                # replace the description if we dont' have one
                self.parser.description = func.__doc__ or ""
            else:
                # or add to the main description
                self.parser.description += linesep + (func.__doc__ or "")
            utils.set_subcommands(func, self.parser)
        else:
            # if we have more than one command or we don't want a single command
            # set the single to None
            self._single = None
            # setup the subparsers
            self.subparsers = self.parser.add_subparsers(
                title=utils.COMMANDS_LIST_TITLE, dest='command',
                description=utils.COMMANDS_LIST_DESCRIPTION)
            # add all the commands
            for func in self.commands.values():
                parser = utils.get_parser(func, self.subparsers)
                utils.set_subcommands(func, parser)

    def parse_args(self):
        """
        Parse our arguments.
        """
        # compile the parser
        self._compile()
        # clear the args
        self.args = None
        # list commands/subcommands in argv
        cmds = [c for c in sys.argv[1:] if not c.startswith("-")]
        if (len(cmds) > 0 and not utils.check_help() and self.default_cmd
                and cmds[0] not in self.commands):
            # if we have at least one command which is not an help command
            # and we have a default command and the first command in arguments
            # is not in commands we insert the default command as second
            # argument (actually the first command)
            sys.argv.insert(1, self.default_cmd)
        # let's parse the arguments
        self.args = self.parser.parse_args()
        # set up the output.
        if self.args:
            # if we have some arguments
            if self.add_output and self.args.output is not None:
                # If add_output is True and we have an output file
                # setup the encoding
                self.encoding = self.args.encoding
                if self.args.encoding.lower() == 'raw':
                    # if we have passed a raw encoding we will write directly
                    # to the output file.
                    self._output = open(self.args.output, 'wb')
                else:
                    # else we will use the codecs module to write to the
                    # output file.
                    import codecs
                    self._output = codecs.open(
                        self.args.output, 'wb', encoding=self.args.encoding)
            if self.cfg_factory:
                # if we have a config factory setup the config file with the
                # right param
                self.cfg_file = self.args.config
            # now is parsed.
            self._is_parsed = True
        return self

    def check_auth(self, name):
        """
        Check the authorization for the command
        """
        if name in self.auths:
            # if the command name is in the **need authorization list**
            # get the authorization for the command
            auth = self.auths[name]
            if self.args.auth is None:
                # if we didn't pass the authorization phrase raise the
                # appropriate exception
                raise exceptions.ArgParseInatorAuthorizationRequired
            elif ((auth is True and self.args.auth != self.auth_phrase) or
                  (auth is not True and self.args.auth != auth)):
                # else if the authorization phrase is wrong
                raise exceptions.ArgParseInatorNotValidAuthorization
        return True

    def check_command(self, **new_attributes):
        """
        Check if 'was passed a valid action in the command line and if so,
        executes it by passing parameters and returning the result.

        :return: (Any) Return the result of the called function, if provided,
                 or None.
        """
        # let's parse arguments if we didn't before.
        if not self._is_parsed:
            self.parse_args()
        if not self.commands:
            # if we don't have commands raise an Exception
            raise exceptions.ArgParseInatorNoCommandsFound
        elif self._single:
            # if we have a single function we get it directly
            func = self._single
        else:
            if not self.args.command:
                self.parser.error("too few arguments")
            # get the right command
            func = self.commands[self.args.command]

        if hasattr(func, '__subcommands__') and func.__subcommands__:
            # if we have subcommands get the command from them
            command = func.__subcommands__[self.args.subcommand]
        else:
            # else the command IS the function
            command = func
        # get the command name
        self.cmd_name = command.__cmd_name__
        # check authorization
        if not self.check_auth(id(command)):
            return 0
        # let's setup something.
        for setup_func in self.setup:
            setup_func(self)
        # let's execute the command.
        return self._execute(func, command, **new_attributes)

    def _execute(self, func, command, **new_attributes):
        """
        Execute command.
        """
        # let's get command(function) argspec
        arg_specs = inspect.getargspec(command)
        if arg_specs.defaults:
            # if we have defaults
            # count defaults arguments
            count = len(arg_specs.defaults)
            # get arguments names
            args_names = arg_specs.args[:count]
            # get keyword arguments names
            kwargs_name = arg_specs.args[count:]
        else:
            # else all names are the args only
            args_names = arg_specs.args
            # and keyword arguments is empty
            kwargs_name = []
        pargs = []
        kwargs = {}
        # for every argument in argument names
        for name in args_names:
            if name == 'args':
                # if argument name is *special name* **args**
                # we append a reference to self.args
                pargs.append(self.args)
            elif name == 'self':
                # else if argment name is *special name* **self**
                if ArgParseInated in inspect.getmro(func.__cls__):
                    # if the class that holds the function is subclass of
                    # ArgParseInated we'll instantiate it, passing some
                    # parameter
                    pargs.append(func.__cls__(self, **new_attributes))
                else:
                    # else we'll instatiate the class without parameters
                    pargs.append(func.__cls__())
            else:
                # else we'll append the argument getting it from the self.args
                pargs.append(getattr(self.args, name))
        # for every argument in keyword arguments
        for name in kwargs_name:
            if name == 'args':
                # if argument name is *special name* **args**
                # we set for the arg a reference to self.args
                kwargs[name] = self.args
            elif name in self.args:
                # else if name is in self.args we'll set the relative value.
                kwargs[name] = getattr(self.args, name)
        # try to import the builtin module
        try:
            import __builtin__
        except ImportError:
            import builtins as __builtin__
        # set the **global** write function
        setattr(__builtin__, self.write_name, self.write)
        # set the **global** write line function
        setattr(__builtin__, self.write_line_name, self.writeln)
        # let's execute the command and assign the returned value to retval
        retval = command(*pargs, **kwargs)
        if self.auto_exit:
            # if we have auto_exit is True
            if retval is None:
                # if retval is None we'll raise an error
                raise TypeError("Return value must not be None")
            elif isinstance(retval, basestring):
                # else if retval is a string we will exit with the message and
                # ERRORCODE is equal to 0
                self.exit(0, retval)
            elif isinstance(retval, int):
                # else if retval is an integer we'll exits with it as ERRORCODE
                self.exit(retval)
            elif isinstance(retval, (tuple, list,)):
                # if retval is a tuple or a list we'll exist with ERRORCODE and
                # message
                self.exit(retval[0], retval[1])
            self.exit()
        else:
            # else if auto_exit is not True
            # we'll simply return  retval
            return retval

    def _tounicode(self, string):
        """Silly converter"""
        if not isinstance(string, unicode):
            # if string is not unicode we'll comverte it
            string = unicode(string, self.encoding)
        return string

    def write(self, *string):
        """
        Writes to the output
        """
        self._output.write(' '.join([self._tounicode(s) for s in string]))
        return self

    def writeln(self, *string):
        """
        Wrtie lines to the output
        """
        self._output.write(' '.join([
            self._tounicode(s) for s in string]) + linesep)
        return self

    def exit(self, status=EXIT_OK, message=None):
        """
        Terminate the script.
        """
        if self.msg_on_error_only:
            # if msg_on_error_only is True
            if status != EXIT_OK:
                # if we have an error we'll exit with the message also.
                self.parser.exit(status, message)
            else:
                # else we'll exit with the status ongly
                self.parser.exit(status, None)
        else:
            # else if msg_on_error_only is not True
            # we'll exit with the status and the message
            self.parser.exit(status, message)


def arg(*args, **kwargs):
    """
    Dcorates a function or a class method to add to the argument parser
    """
    def decorate(func):
        """
        Decorate
        """
        # we'll set the command name with the passed cmd_name argument, if
        # exist, else the command name will be the function name
        func.__cmd_name__ = kwargs.pop('cmd_name', func.__name__)
        # retrieve the class (SillyClass)
        func.__cls__ = utils.check_class()
        if not hasattr(func, '__arguments__'):
            # if the funcion hasn't the __arguments__ yet, we'll setup them
            # using get_functarguments.
            func.__arguments__ = utils.get_functarguments(func)
        if len(args) or len(kwargs):
            # if we have some argument or keyword argument
            # we'll try to get the destination name from the kwargs ('dest')
            # else we'll use the last arg name as destination
            arg_name = kwargs.get(
                'dest', args[-1].lstrip('-').replace('-', '_'))
            try:
                # we try to get the command index.
                idx = func.__named__.index(arg_name)
                # and delete it from the named list
                del func.__named__[idx]
                # and delete it from the arguments list
                del func.__arguments__[idx]
            except ValueError:
                pass
            # append the args and kwargs to the function arguments list
            func.__arguments__.append((args, kwargs,))
        if func.__cls__ is None and isinstance(func, types.FunctionType):
            # if the function don't have a class and is a FunctionType
            # we'll add it directly to he commands list.
            ap_ = ArgParseInator(skip_init=True)
            if func.__cmd_name__ not in ap_.commands:
                # we'll add it if not exists
                ap_.commands[func.__cmd_name__] = func
        return func
    return decorate


def class_args(cls):
    """
    Decorates a class to handle the arguments parser.
    """
    # get the Singleton
    ap_ = ArgParseInator(skip_init=True)
    # collect special vars (really need?)
    utils.collect_appendvars(ap_, cls)
    # set class reference
    cls.__cls__ = cls
    cmds = {}
    # get eventual class arguments
    cls.__arguments__ = getattr(cls, '__arguments__', [])
    # cycle through class functions
    for func in [f for f in cls.__dict__.values()
                 if hasattr(f, '__cmd_name__') and not inspect.isclass(f)]:
        # clear subcommands
        func.__subcommands__ = None
        # set the parent class
        func.__cls__ = cls
        # assign to commands dict
        cmds[func.__cmd_name__] = func
    if hasattr(cls, '__cmd_name__') and cls.__cmd_name__ not in ap_.commands:
        # if che class has the __cmd_name__ attribute and is not already present
        # in the ArgParseInator commands
        # set the class subcommands
        cls.__subcommands__ = cmds
        # add the class as ArgParseInator command
        ap_.commands[cls.__cmd_name__] = cls
    else:
        # else if we don't have a __cmd_name__
        # we will add all the functions directly to the ArgParseInator commands
        # if it don't already exists.
        for name, func in cmds.items():
            if name not in ap_.commands:
                ap_.commands[name] = func
    return cls


def ap_arg(*args, **kwargs):
    """
    Silly function to return a tuple for add_argument parser.
    """
    return args, kwargs


def cmd_auth(auth_phrase=None):
    """
    set authorization for command or subcommand.
    """
    def decorate(func):
        """
        decorates the funcion
        """
        # get the Singleton
        ap_ = ArgParseInator(skip_init=True)
        # set the authorization name
        auth_name = id(func)
        if auth_phrase is None:
            # if we don't have a specific auth_phrase we set the
            # **authorization needed** to True
            ap_.auths[auth_name] = True
        else:
            # else if we have a specific auth_phrase we set it for the
            # command authorization
            ap_.auths[auth_name] = str(auth_phrase)
        return func
    return decorate


def import_commands(commands_package):
    """
    Imports commands modules for the script.
    """
    import pkgutil
    try:
        # try to import commands module
        mod = __import__(commands_package)
    except ImportError:
        mod = None
    if mod:
        # if we have a commands module
        # we iter the modules and try to import them
        for module in pkgutil.iter_modules(mod.__path__):
            try:
                # try to import the module
                __import__("{}.{}".format(commands_package, module[1]))
            except ImportError:
                pass


def import_commands_folder(commands_folder):
    """
    Imports commands modules for the script.
    """
    import importlib
    # get folder basename
    commands = os.path.basename(commands_folder)
    for filename in os.listdir(commands_folder):
        # for each filename we will get module name
        mod_name = os.path.splitext(filename)[0]
        try:
            # try to import module
            importlib.import_module("{}.{}".format(commands, mod_name))
        # except ImportError as err:
        except StandardError as err:
            print (err)
