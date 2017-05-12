# -*- coding: utf-8 -*-
"""
Aggunge la direttiva exec a sphinx
"""
# pylint: disable=exec-used
import os
from sphinx.util.compat import Directive

class ResetArgParseInator(Directive):
    """ Resets ArgParseInator """
    has_content = False
    required_arguments = 1

    def run(self):
        import argparseinator
        try:
            reload(argparseinator)
        except NameError:
            from imp import reload
        reload(argparseinator)
        os.environ['ARPI_DOC_MOD'] = self.arguments[0]
        return []

def setup(app):
    """Setup"""
    app.add_directive('clear_argparseinator', ResetArgParseInator)
    os.environ['ARPI_DOC'] = 'yes'
