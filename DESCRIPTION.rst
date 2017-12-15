ArgParseInator
===============

`Argparseinator`_ is a silly, but useful, thing that permit you to easily add
`argparse`_'s arguments and options to your script directly within functions
and classes with the use of some decorators.

.. _ArgParseInator: https://github.com/ellethee/argparseinator
.. _argparse: https://docs.python.org/2/library/argparse.html
.. _ArgumentParser: https://docs.python.org/2/library/argparse.html#argumentparser-objects

Install
=======
pip install argparseinator


Quick example (sayciao.py module)
=================================

.. code-block:: python

    """
    Say ciao script.
    """

    __version__ = "1.2.3"


    from argparseinator import ArgParseInator, arg


    @arg()
    def sayciao(name):
        """
        I will say ciao.
        """
        print "Ciao", name

    if __name__ == '__main__':
        ArgParseInator().check_command()


call:

.. code-block:: bash

    $ python sayciao.py --help

will output:

.. code-block:: bash

    usage: sayciao.py [-h] [-v] name

    Say ciao script.

        I will say ciao.


    positional arguments:
      name

    optional arguments:
      -h, --help     show this help message and exit
      -v, --version  show program's version number and exit


call:

.. code-block:: bash

    $ python sayciao.py --version

will output:

.. code-block:: bash

    sayciao.py 1.2.3

call:

.. code-block:: bash

    $ python sayciao.py luca

will output:

.. code-block:: bash

    Ciao luca


Docs
====
See readthedocs_

.. _readthedocs: http://argparserinator.readthedocs.org/it/latest
