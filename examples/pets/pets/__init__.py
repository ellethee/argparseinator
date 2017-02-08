# -*- coding: utf-8 -*-
"""
====
Pets
====

Manages various pets.
"""
from argparseinator import ArgParseInator
import pets.commands
__version__ = "0.0.1"

# We enable the output and set the default write_mode to append binary.
ArgParseInator(add_output=True, write_mode="ab")
