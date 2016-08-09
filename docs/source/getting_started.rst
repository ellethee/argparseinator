Getting Started
===============

The use of ArgParseInator is very simple. 

Decorate the functions and / or classes by setting the necessary parameters and
putting into the \__doc__\ string the function description.

.. code-block:: python

    from argparseinator import ArgParseInator
    from argparseinator import arg


    @arg("name", help="The name to print")
    @arg('-s', '--surname', default='', help="optional surname")
    def print_name(name, surname=""):
        """
        Will print the passed name.
        """
        print "Printing the name...", name, surname

.. note::

    functions can have positional arguments and keyword argument to reflect
    the ArgParseInator arguments. Anyway there are some tricks that we will
    see later in the function declaration section. 


Get the ArgParseInator instance passing some parameters if necessary.
Then verify the commands passed to the script.

.. code-block:: python

    if __name__ == "__main__":
        ArgParseInator(description="Silly script").check_command()

Try out your script help

.. code-block:: bash

    $ python apitest.py -h

Will output

.. code-block:: bash

    usage: apitest.py [-h] [-s SURNAME] name

    Silly script

        Will print the passed name.
        

    positional arguments:
      name                  The name to print

    optional arguments:
      -h, --help            show this help message and exit
      -s SURNAME, --surname SURNAME
                            optional surname

Try out your script

.. code-block:: bash

    $python apitest.py --surname=Smith John

Will output

.. code-block:: bash

    Printing the name... John Smith

.. note::

    If we have only one function decorated it will become the default command
    and Argparseinator appends the function description to the main
    parser's description.
