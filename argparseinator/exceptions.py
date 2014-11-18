#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Some Exception
"""
__file_name__ = "exceptions.py"
__author__ = "luca"
__version__ = "1.0.0"
__date__ = "2014-10-23"


class ArgParseInatorError(Exception):
    """
    Exception per ArgParseInator.
    """
    def __init__(self, errno=255, errmsg="Generic error"):
        super(ArgParseInatorError, self).__init__(errno, errmsg)

    def __str__(self):
        return "{} - {}".format(*self.args)


class ArgParseInatorInvalidCommand(ArgParseInatorError):
    def __init__(self):
        super(ArgParseInatorInvalidCommand, self).__init__(
            225, "Invalid command")


class ArgParseInatorNoCommandsFound(ArgParseInatorError):
    def __init__(self):
        super(ArgParseInatorNoCommandsFound, self).__init__(
            226, "No commands found")
