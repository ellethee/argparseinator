#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Simple HttpClient.
"""
__file_name__ = "httpclient.py"
__author__ = "luca"
__version__ = "1.0.0"
__date__ = "2014-11-21"


from argparseinator import ArgParseInator, arg
import requests


@arg('url', help="url to retrieve")
def get(url):
    """Retrieve an url."""
    response = requests.get(url)
    if response.status_code == 200:
        writeln(response.text)
    else:
        writeln(str(response.status_code), response.reason)


@arg('var', help="Posta data in NAME=VALUE form", nargs="*")
@arg('url', help="url to retrieve")
def post(url, var):
    """Post data to an url."""
    data = {b[0]: b[1] for b in [a.split("=") for a in var]}
    writeln("Sending data to url", url)
    writeln(*var)
    response = requests.post(url, data=data)
    if response.status_code == 200:
        writeln(response.text)
    else:
        writeln(str(response.status_code), response.reason)


if __name__ == "__main__":
    ArgParseInator().check_command()
