#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Modular multi commands with subcommands example
    
"""
from argparseinator import ArgParseInator

import admin_commands

if __name__ == "__main__":
    ArgParseInator(
        description="Simple http retrieving",
        add_output=True,
        auto_exit=True,
        never_single=True,
    ).check_command()
