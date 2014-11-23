======================
ArgParseInator object
======================

.. class:: ArgParseInator(add_output=None, args=None, auth_phrase=None, \
                           never_single=None , write_name=None, \
                           write_line_name=None, auto_exit=None, \**kwargs)

   Create a new :class:`ArgParseInator` object. All parameters should be passed
   as keyword arguments. 

   * add_output_ - Enable the output option (default: ``False``)

   * args_ - List of argument to pass to the parser (default: ``None``)

   * auth_phrase_ - Global authorization phrase (default: ``None``)

   * never_single_ - Force argp to have one command even is the only one
     (default: ``False``)

   * write_name_ - Name for the global function which calls
     :meth:`ArgParseInator.write` (default: "write")

   * write_line_name_ - Name for the global function which calls
     :meth:`ArgParseInator.writeln` (default: "writeln")

   * auto_exit_ - if True ArgParseInator exits just executed the command 
     using the returned value(s) as status code

   * kwargs_ - All standard :class:`ArgumentParser` parameters.


Parameters
==========

add_output
----------
Automatically append to the top level parser the ``-o`` ``--output`` optional
argument. If the argument is passed the :class:`ArgParseInator` 
:meth:`write` and :meth:`writeln` methods will write the output to the file.

.. code-block:: python

    from argparseinator import ArgParseInator, arg

    @arg('string', help="String to write")
    def write(string):
        """
        Wrtie a string 
        """
        ArgParseInator().writeln(string)

    ArgParseInator(add_output=True).check_command()

.. code-block:: bash

    $ python script.py --output=filename.txt "Hello my name is Luca"

Will create a file named **filename.txt** containing the line
**Hello my name is Luca**

args
----
Accepts a list of argument to pass to the top level parser. Every element of 
the list must be a tuple with positional args and keyword args. Something like
this ``(('-o', '--option'), {'help': 'option', 'default': 'no option'})`` but
for convenience we use the :func:`ap_arg` which simplify things.

.. code-block:: python

    from argparseinator import ArgParseInator, arg, ap_arg

    @arg('string', help="String to write")
    def write(string, prefix):
        """
        print a string 
        """
        print prefix, string

    ArgParseInator(args=[
        ap_arg('-p', '--prefix', help="string prefix", default="Now Writing..")
    ]).check_command()

.. code-block:: bash

    $ python script.py -h

will output

.. code-block:: bash

    usage: script.py [-h] [-p PREFIX] string

        print a string 
        

    positional arguments:
      string                String to write

    optional arguments:
      -h, --help            show this help message and exit
      -p PREFIX, --prefix PREFIX
                            string prefix


.. _auth_phrase:

auth_phrase
-----------
Set a global authorization phrase to protect special commands.
See :ref:`authorize_commands`

never_single
------------
When we have only one decorated function :class:ArgParseInator automatically
set it as default and adds all it arguments to the top level parser.
Anyway we can tell to :class:`ArgParseInator` to keep it as a command by setting
the **never_single** param to ``True``.

.. code-block:: python

    from argparseinator import ArgParseInator, arg

    @arg('string', help="String to write")
    def write(string):
        """
        Wrtie a string 
        """
        print string

    ArgParseInator().check_command()

.. code-block:: bash

    $ python script.py "String to print"
    String to print

.. code-block:: python

    ArgParseInator(never_single=True).check_command()

.. code-block:: bash

    $ python script.py write "String to print"
    String to print


write_name
----------
Sets the name for the global shortcut :meth:`write` (see :ref:`write_writeln`)

.. code-block:: python

    @arg()
    def write_test():
        w("this is a test.")
    
    ArgParseInator(write_name="w").check_command()

write_line_name
---------------
As write_name sets the name for the global shortcut :meth:`writeln`
(see :ref:`write_writeln`)


auto_exit
---------
If True ArgParseInator exits just executed the command using the returned
value(s) as status code.

If the command function return only a numeric value it will be used as status
code exiting the script if the command function returns a touple with numeric
and string value the string will be printed as message.

.. code-block:: python

    @arg()
    def one():
        # will exit from script with status code 1
        return 1

    @arg()
    def two():
        # will exit from script with status code 2 and print the message
        # "Error"
        return 2, "Error."


kwargs
------
\**kwargs are all the parameters to pass to the :class:`ArgumentParser`.

.. note::

    The part below is copied from the argparse_ module page.


* prog_ - The name of the program (default: ``sys.argv[0]``)

* usage_ - The string describing the program usage
  (default: generated from arguments added to parser)

* description_ - Text to display before the argument help (default: none)

* epilog_ - Text to display after the argument help (default: none)

* formatter_class_ - A class for customizing the help output

* prefix_chars_ - The set of characters that prefix optional arguments
  (default: '-')

* fromfile_prefix_chars_ - The set of characters that prefix files from which
  additional arguments should be read (default: ``None``)

* argument_default_ - The global default value for arguments
  (default: ``None``)

* add_help_ - Add a -h/--help option to the parser (default: ``True``)


.. _argparse: https://docs.python.org/2/library/argparse.html

.. _prog: https://docs.python.org/2/library/argparse.html#prog/

.. _usage: https://docs.python.org/2/library/argparse.html#usage

.. _description: https://docs.python.org/2/library/argparse.html#description

.. _epilog: https://docs.python.org/2/library/argparse.html#epilog

.. _formatter_class: https://docs.python.org/2/library/argparse.html#formatter_class

.. _prefix_chars: https://docs.python.org/2/library/argparse.html#prefix_chars

.. _fromfile_prefix_chars: https://docs.python.org/2/library/argparse.html#fromfile_prefix_chars

.. _argument_default: https://docs.python.org/2/library/argparse.html#argument_default

.. _add_help: https://docs.python.org/2/library/argparse.html#add_help

Methods
=======

.. method:: ArgParseInator.check_command(\**new_attributes)

    Essentially executes the command doing these steps.

    #. Create all the arguments parsers with arguments according with the
       decorators and classes.

    #. Parse the arguments passed by the command line.

    #. If there are no problems it calls the  command passing the parameters
       needed. In case the command is a class method instantiates the class,
       passing the **\**new_attributes** dictionary if the class is inherited
       from :class:`ArgParseInated` class.

.. method:: ArgParseInator.write(\*strings)

    Write to the output (stdout or file see add_output_). If more than a string
    is passed will be written space separated.

.. method:: ArgParseInator.writeln(\*strings)

    Exactly as :meth:`ArgParseInator.write` but append a newline at the end
    of the string.


.. _write_writeln:

:meth:`write` and :meth:`writeln`
=================================
Just before execute the command :class:`ArgParseInator` adds two global
shortcuts for it's methods :meth:`ArgParseInator.write` and
:meth:`ArgParseInator.writeln` respectvly :meth:`write` and :meth:`writeln`

Which cam be useful within function insted use the 
```ArgParseInator().write()``` and ```ArgParseInator().writeln()``` form.

The two methos name can be changed via the write_name_ and
write_line_name_ arguments while instatiate the ArgParseInator.
