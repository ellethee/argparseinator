#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Configuration example.
"""
import sys
import yaml
from argparseinator import ArgParseInator, arg

def config_factory(self, filename):
    """Configuration handler"""
    return yaml.load(open(filename, 'rb'))

def config_error(self, error):
    """ Configuration error handler"""
    print error
    sys.exit(1)

@arg()
def name():
    """
        Prints configuration username and password
        using then __argpi__ global reference to the ArgParseInator instance
    """
    print __argpi__.cfg['username'], __argpi__.cfg['password']

if __name__ == "__main__":
    ArgParseInator(
        config=('config.yaml', config_factory, config_error)
    ).check_command()

