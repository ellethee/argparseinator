#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Standard launcher
"""
import sys
from os.path import basename, splitext
from importlib import import_module
sys.modules[__name__] = import_module(splitext(basename(sys.argv[0]))[0])

if __name__ == "__main__":
    __argpi__.check_command()
