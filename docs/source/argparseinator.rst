.. currentmodule:: argparseinator

======================
ArgParseInator object
======================

.. class:: ArgParseInator(add_output=None, argpi_name=None, args=None, auth_phrase=None, \
            auto_exit=None, config=None, default_cmd=None, error=None, \
            ff_prefix=None, formatter_class=None, msg_on_error_only=None, \
            never_single=None, setup=None, \
            write_line_name=None, write_name=None, \
            **argparse_args)

   Create a new :class:`ArgParseInator` object. All parameters should be passed
   as keyword arguments. 

   * add_output_ - Enable the output option (default: ``False``).

   * argpi_name_ - Name for the global reference of the Argparseinator
     instance (default: ``__argpi__``).

   * args_ - List of argument to pass to the parser (default: ``None``).

   * auth_phrase_ - Global authorization phrase (default: ``None``).

   * auto_exit_ - if True ArgParseInator uses the functions return values as 
     exit status code. If the return statment is missing or the return value is
     None then EXIT_OK will be used (default: ``True``).

   * config_ - Tuple containing config filename, config factory and optionally
     a config error handler.

   * default_cmd_ - Name of the default command to set.

   * error_ - Error handler to pass to parser.

   * ff_prefix_ - fromfile_prefix_chars to pass to the parser.

   * formatter_class_ - A class for customizing the help output.

   * msg_on_error_only_ - if auto_exit_ is ``True``, it outputs the command
     message only if there is an exception.

   * never_single_ - Force to have one command, even it is the only one
     (default: ``False``).

   * setup_ - List of functions (having the ArgParseInator class as parameter)
     that will be executed after the arguments parsing and just before to
     execute the command.

   * write_name_ - Name for the global function which calls
     :meth:`ArgParseInator.write` (default: ``write``).

   * write_line_name_ - Name for the global function which calls
     :meth:`ArgParseInator.writeln` (default: ``writeln``).

   * `write_mode` - default write mode when using add_output_ (default: ``wb``).

   * show_defaults - If True shows default values for parameters in help (default: ``True``).

   * argparse_args_ - All standard :class:`ArgumentParser` parameters.


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

argpi_name
-----------
The **Argparseinator** instance can be accessed globally via the name ``__argpi__``.
Anyway you can change the global name using this parameter.

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

auto_exit
---------
If True ArgParseInator exits just executed the command using the returned
value(s) as status code.

If the command function return only a numeric value it will be used as status
code exiting the script if the command function returns a tuple with numeric
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

config
------
It could happen that we need a configuration dictionary or something similare,
usually loaded from a file. We can specify a dictionary with the configuration
or a tuple to handle the configuration file and optionally a configuration
error handler.
It will be available as **self.cfg** if you use a subclass of ArgParseInated or
globally using `__argpi__ <argpi_name_>`_.**cfg**

.. code-block:: python

    

    def cfg_factory(filename):
        """Configuration factory"""
        import yaml
        return yaml.load(filename)

    def cfgname():
        """Prints name"""
        print __argpi__.cfg['name']

    Argparseinator(config=('default.cfg', cfg_factory)).check_command()

.. note:

    The configuration

never_single
------------
When we have only one decorated function :class:`ArgParseInator` automatically
set it as default and adds all its arguments to the top level parser.
We can also tell to :class:`ArgParseInator` to keep it as a command by setting
the **never_single** parameter to ``True``.

.. code-block:: python

    from argparseinator import ArgParseInator, arg

    @arg('string', help="String to write")
    def write(string):
        """
        Write a string 
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
As write_name does, it sets the name for the global shortcut :meth:`writeln`
(see :ref:`write_writeln`)


default_cmd
-----------
When we have multiple commands we can set a default one to be used
if :class:`ArgParseInator` can't find a valid one in ``sys.argv``


error
-----
Usually if we need to handle argparse error we have to subclass the
ArgumentParser and override the error method. With the :class:`ArgParseInator`
we can just pass the handler as :keyword:`error` parameter.

.. code-block:: python

    def error_hander(self, message):
        """Error handler"""
        print "And the error is ...", message

    ArgParseInator(error=error_hander).check_command()


ff_prefix
---------
It's a shortcut for fromfile_prefix_chars_. Note that if its value is True then it 
automatically uses the **@** as fromfile_prefix_chars.


msg_on_error_only
-----------------
if auto_exit_ is True, it outputs the command message only if there is an exception.


setup
-----
A list or tuple of functions that will be executed just before executing the
command, receives as parameter the ArgParseInator instance.

.. code-block:: python

    def setup_1(inator):
        """first setup"""
        inator.args.name = 'Luca'

    def setup_2(inator):
        """second setup"""
        inator.args.name = inator.args.name.upper()

    ArgParseInator(setup=[setup_1, setup_2]).check_command()


argparse_args
-------------
\**argparse_args are all the parameters to pass to the :class:`ArgumentParser`.

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

.. _fromfile_prefix_chars: https://docs.python.org/2/library/argparse.html#fromfile-prefix-chars

.. _argument_default: https://docs.python.org/2/library/argparse.html#argument_default

.. _add_help: https://docs.python.org/2/library/argparse.html#add_help

Methods
=======

.. method:: ArgParseInator.check_command(\**new_attributes)

    Essentially executes the command doing these steps.

    #. Create all the arguments parsers with arguments according with the
       decorators and classes.

    #. Parse the arguments passed by the command line.

    #. Try to execute the command.

.. method:: ArgParseInator.write(\*strings)

    Write to the output (stdout or file, see add_output_). If more than a string
    is passed then it will be written space separated.

.. method:: ArgParseInator.writeln(\*strings)

    Exactly as :meth:`ArgParseInator.write` but appends a newline at the end
    of the string.


.. _write_writeln:

:class:`__argpi__`, :meth:`write` and :meth:`writeln`
=====================================================
Just before executing the command :class:`ArgParseInator` it adds two global
shortcuts for its methods :meth:`ArgParseInator.write` and
:meth:`ArgParseInator.writeln` respectively :meth:`write` and :meth:`writeln`
and the global reference to the *Singleton* instance as :class:`__argpi__`.

So you can use :func:`write` or :func:`writeln` instead of
```ArgParseInator().write()```, ```ArgParseInator().writeln()```.
And access directly to the Singleton instance using :class:`__argpi__` instead
of ```ArgParseInator()```.

The two methods names can be changed via the write_name_ and
write_line_name_ arguments and the global instance name via the argpi_name_ 
while instantiating the ArgParseInator.
