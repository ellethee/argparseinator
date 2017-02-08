# -*- coding: utf-8 -*-
"""
===============================
Commands :mod:`greets.commands`
===============================
"""
from argparseinator import ArgParseInated
from argparseinator import arg, ap_arg
from argparseinator import class_args


@class_args
class Commands(ArgParseInated):
    """Commands for greets"""

    # we have the same params for all the commands so we can share them
    __shared_arguments__ = [
        ap_arg("who", help="The who", nargs="?", default="World!"),
        ap_arg("-l", "--lang", default="en", help="Language")
    ]

    def __preinator__(self):
        # Actually we are not sure we have a configuration so is better
        # add some default.
        cfg = {
            'lang': 'en',
            'words_en': {
                'greet': 'Greetings',
                'hello': 'Hello',
                'bye': 'Goodbye',
            }
        }
        cfg.update(self.cfg)
        self.cfg = cfg

    def get_language(self, word, lang=None):
        """Get right word for configured language"""
        lang = lang or self.cfg.get('lang', 'en')
        # let's retrieve the word from configuration dict.
        try:
            return self.cfg['words_' + lang][word]
        except StandardError:
            return 'Do not know how to "{}" in "{}"'.format(word, lang)

    @arg()
    def greet(self, who, lang):
        """Greets"""
        # we added the add_output param so we use the writeln to greet on the
        # right output.
        writeln(self.get_language('greet', lang), who)

    @arg()
    def hallo(self, who, lang):
        """Hallo"""
        writeln(self.get_language('hello', lang), who)

    @arg()
    def bye(self, who, lang):
        """Bye"""
        writeln(self.get_language('bye', lang), who)
