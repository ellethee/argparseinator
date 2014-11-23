#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    ArgParseInator test
"""
__file_name__ = "apitest.py"
__author__ = "luca"
__version__ = "1.0.0"
__date__ = "2014-11-18"


import argparseinator
from argparseinator import arg, ap_arg, class_args


@argparseinator.arg("name", help="The name to print")
@argparseinator.arg('-s', '--surname', default='', help="optional surname")
def print_name(name, surname, address):
    """
    Will print the passed name.
    """
    print "Printing the name...", name, surname, address


@argparseinator.arg(cmd_name="foo")
def foo_name():
    """
    print foo.
    """
    print "foo"


@class_args
class CommandsContainer(object):
    """
    CommandsContainer class.
    """

    prefix = "The name is"
    __arguments__ = [ap_arg('--arguments', help="Class arguments")]
    __shared_arguments__ = [
        ap_arg('name', help="The name"),
        ap_arg('--prefix', help="string prefix", default='We have')]

    @arg()
    def name(self, name, prefix):
        """
        Print the name.
        """
        print prefix, 'name', name

    @arg()
    def surname(self, name, prefix):
        """
        Print the surname.
        """
        print prefix, 'surname', name

    @arg()
    def nickname(self, name, prefix):
        """
        Print the nickname.
        """
        print prefix, "nickname",  name

@class_args
class Greetings(object):
    """
    Greeting command.
    """
    __cmd_name__ = 'greet'
    __arguments__ = [ap_arg(
        '-p', '--prefix', help='greeting prefix', default="We say")]
    __shared_arguments__ = [ap_arg('name', help='the name')]
    
    @arg()
    def ciao(self, name, prefix):
        """
        Say ciao.
        """
        print prefix, 'Ciao', 'to', name

    @arg()
    def hello(self, name, prefix):
        """
        Say hello.
        """
        print prefix, 'hello', 'to', name
    

if __name__ == "__main__":
    inator = argparseinator.ArgParseInator(
        description="Silly script",
        args=[
            ap_arg('--address', help='Person address', default='Home'),
        ]
    )
    inator.check_command()
