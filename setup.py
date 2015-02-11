# -*- coding: utf-8 -*-
"""
    ArgParseInator setup
"""

import io
import os
import re
from setuptools import setup, find_packages
from codecs import open
from os import path
here = path.abspath(path.dirname(__file__))


def read(*names, **kwargs):
    """
    Legge i files.
    """
    return io.open(
        os.path.join(os.path.dirname(__file__), *names),
        encoding=kwargs.get("encoding", "utf8")
    ).read()


def find_version(*file_paths):
    """
    Trova la versione.
    """
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


# Get the long description from the relevant file
with open(path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()
setup(
    name='ArgParseInator',
    version=find_version('argparseinator/__init__.py'),
    description=(
        "Decorators and wrapper for easily define script's arguments "
        "within functions and classes. just defining function's args."
    ),
    long_description=LONG_DESCRIPTION,
    url="https://bitbucket.org/ellethee/argparseinator/overview",
    author='ellethee',
    author_email='luca800@gmail.com',
    license='MIT',
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        "Topic :: Software Development :: Testing",
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
    keywords=(
        "simple arguments argumentparser options args command line argparse "
        "optparse optionparser script"
    ),
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
)
