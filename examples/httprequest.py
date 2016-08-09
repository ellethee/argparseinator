#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Simple Http retrieving.
"""
from argparseinator import ArgParseInator, arg
import requests


@arg('url', help="url to retrieve")
def get(url):
    """Retrieve an url."""
    writeln("Getting data from url", url)
    response = requests.get(url)
    if response.status_code == 200:
        writeln(response.text)
    else:
        writeln(str(response.status_code), response.reason)


@arg('var', help="Post data in NAME=VALUE form", nargs="*")
@arg('url', help="url to retrieve")
def post(url, var):
    """Post data to an url."""
    data = {b[0]: b[1] for b in [a.split("=") for a in var]}
    writeln("Sending data to url", url)
    response = requests.post(url, data=data)
    if response.status_code == 200:
        writeln(response.text)
    else:
        writeln(str(response.status_code), response.reason)

if __name__ == "__main__":
    ArgParseInator(
        add_output=True,
        default_cmd="get",
    ).check_command()
