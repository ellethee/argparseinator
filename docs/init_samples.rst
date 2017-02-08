
The project is something like this

.. code-block:: python
    :caption: project.py

    import sys
    from os.path import basename, splitext
    from importlib import import_module
    # We import the project/__init__.py to the current module
    # (thanks to Alex Martelli)
    sys.modules[__name__] = import_module(splitext(basename(sys.argv[0]))[0])

    if __name__ == "__main__":
        # check_command
        __argpi__.check_command()

.. code-block:: python
    :caption: project/__init__.py

    from argparseinator import ArgParseInator
    import project.commands
    __version__ = "0.0.1"

    ArgParseInator(auto_exit=True)

.. code-block:: python
    :caption: project/commands.py

    from argparseinator import ArgParseInated
    from argparseinator import arg
    from argparseinator import class_args


    @class_args
    class Commands(ArgParseInated):
        """Commands for Project"""

        @arg("word", help="The word", nargs="?", default="bird")
        def say(self, word):
            """says the word"""
            writeln("i said", word)
            return 0
