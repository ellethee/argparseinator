# -*- coding: utf-8 -*-
"""
    User commands for multi commands example.
"""
from argparseinator import class_args, arg, ArgParseInated


@class_args
class User(ArgParseInated):
    """
    User commands.
    """
    __cmd_name__ = "user"

    @arg()
    def files(self):
        """
        List files.
        """
        self.writeln("Listing files...")
        # listing files code.
        return 0, "Files listed\n"

    @arg('name', help="Name to greet")
    def greet(self, name):
        """
        Greeting command.
        """
        self.writeln('Greeting person...')
        self.writeln('Ciao', name)
        return 0, "person greeted\n"
