# -*- coding: utf-8 -*-
"""
======
Greets
======

Greets people
"""
from argparseinator import ArgParseInator
# we import the get_compiled function in case of sphinx.
from argparseinator import get_compiled
import yaml
import greets.commands
__version__ = "0.0.1"

# We don't really need a configuration but it's for example propouse.
def cfg_factory(filename):
    """Config Factory"""
    try:
        # try to load config as yaml file.
        with open(filename, 'rb') as stream:
            return yaml.load(stream)
    except StandardError as error:
        # In case of error we use the **__argpi__** builtin to exit from
        # script
        __argpi__.exit(1, str(error))


ArgParseInator(
    # Add the possibility of writing the output to file.
    add_output=True,
    # we will append to existing file.
    write_mode='ab',
    # Add the cfg_factory with the default config name to None.
    config=(None, cfg_factory,)
)
