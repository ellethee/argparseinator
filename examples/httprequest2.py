#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Simple Http retrieving with ArgParseInated class.
"""
from argparseinator import ArgParseInator, ArgParseInated
from argparseinator import arg, ap_arg, class_args
import requests


@class_args
class HttpRequest(ArgParseInated):
    """Silly Http retrieving."""

    __shared_arguments__ = [ap_arg('url', help="url to retrieve")]

    @arg()
    def get(self, url):
        """Retrieve an url."""
        self.writeln("Getting data from url", url)
        response = self.session.get(url)
        if response.status_code == 200:
            self.writeln(response.text)
        else:
            self.writeln(str(response.status_code), response.reason)

    @arg('var', help="Posta data in NAME=VALUE form", nargs="*")
    def post(self, url, var):
        """Post data to an url."""
        data = {b[0]: b[1] for b in [a.split("=") for a in var]}
        self.writeln("Sending data to url", url)
        response = self.session.post(url, data=data)
        if response.status_code == 200:
            self.writeln(response.text)
        else:
            self.writeln(str(response.status_code), response.reason)

if __name__ == "__main__":
    ArgParseInator(
        add_output=True,
    ).check_command(session=requests.Session())
