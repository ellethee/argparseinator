#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Modular multi commands with subcommands example
"""
# If we specify here out version ArgParseInator will include it for us.
__version__ = "1.2.3"

import os
from argparseinator import ArgParseInator, import_commands


if __name__ == "__main__":
    # Let's import commands for the script which resides into the commands
    # package.
    import_commands('commands')
    # Ok, Istantiate ArgParseInator
    ArgParseInator(
        # Enable the --output if we want to write the result on file.
        add_output=True,
        # We will automatically exit from the script with the command return
        # code and message if any
        auto_exit=True,
        # Set up the phrase for commands that needs authorization
        auth_phrase="ok",
        # And set the default command for when we don't explicitally pass it
        default_cmd="user",
    # And finally tell to ArgParseInator to check command
    ).check_command()
