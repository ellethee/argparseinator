#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
==============================
Generic ArgParseInator Launcer
==============================

Generic ArgParseInator Launcer.
"""
from __future__ import print_function
import sys
from glob import glob
from os.path import basename, splitext, join, dirname
from importlib import import_module
try:
    # we try to import the core module (pets/__init__.py in this case)
    MOD = import_module(splitext(basename(sys.argv[0]))[0])
except ImportError:
    MOD = None
try:
    # we try to import the wanted module
    sys.modules[__name__] = import_module(splitext(basename(sys.argv[1]))[0])
    # modify the sys.argv to set it as starting script or the startin command.
    sys.argv[0] = sys.argv.pop(1)
except (ImportError, IndexError):
    # if we have a import error will and we have found the core module we
    # will set is as the main module.
    if MOD:
        sys.modules[__name__] = MOD
    else:
        print("Valid module are:")
        print("\n".join(set([
            basename(dirname(d))
            for d in glob(join(dirname(sys.argv[0]), "*/__init__.py*"))])))
        sys.exit(1)
# we use the builtin __argpi__ object to check the command line.
__argpi__.check_command()
