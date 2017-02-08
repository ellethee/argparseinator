.. _within_classes:

==============
Within classes
==============
We can also use classes for define our commands and sub commands. 
There are three properties that we can use within classes.

* :attr:`__cmd_name__`: Declare the command name. In this way the class becomes
  a Sub Commands container.

* :attr:`__arguments__`: Arguments list. When the class is a sub commands
  container we can set a list of attributes for the command itself.

* :attr:`__shared_arguments__`: Shared arguments list. In any case we can
  declare a list of arguments that will be shared by all commands or
  sub commands.

* :attr:`__no_share__`: Must be defined at function level and can bypass
  __shared_arguments__.
  
    .. code-block:: python

        __shared_arguments__ = [ap_arg("name"), ap_arg("surname")]

        @arg()
        def mytime(self):
            pass
        mytime.__no_share__ = True  # None of __shared_arguments__.

        @arg()
        def nick(self):
            pass
        nick.__no_share__ = ['surname'] # all __shared_arguments__ but not surname.

The way we declare the class using these properties changes the behavior of 
ArgParseInator. Always using the :ref:`enable_class` decoration for the class
of course.


* :ref:`way_1`

* :ref:`way_2`

* :ref:`way_3`
  
* :ref:`way_4`

.. _way_1:

First way (commands container)
------------------------------
We can turn a class in a commands container using the ``@class_args`` decorator
and using the ``@arg`` decorator with the class methods to turn them into commands

.. code-block:: python

    @class_args
    class CommandsContainer(object):
        """Commands container class."""
        prefix = "The name is"

        @arg('name', help="The Name")
        def name(self, name):
            """Print the name."""
            print self.prefix, name
        ...

.. _way_2:

Second way (sub-commands container)
-----------------------------------
We can specify a **__cmd_name__** for the class so it will become the *command*
and all decorated methods will become *sub-commands*.

.. code-block:: python

    @class_args
    class SubCommandsContainer(object):
        """Sub Commands container class."""
        # our command will be dosub
        __cmd_name__ = 'dosub'
        prefix = "The name is"

        @arg('name', help="The Name")
        def name(self, name):
            """Print the name. """
            print self.prefix, name
        ...

.. _way_3:

Shared arguments
----------------
Whether we use the :ref:`way_1` or the :ref:`way_2` we can specify a 
**__shared_arguments__** with a list of arguments that will
be added to all commands contained in the class.

.. code-block:: python

    @class_args
    class CommandsContainer(object):
        """
        Commands Container class.
        """
        # share arguments with commands.
        __shared_arguments__ = [
            ap_arg('name', help="The Name"),
            ap_arg('--prefix', help="prefix string", default="The name is..")]

        @arg()
        def name(self, name, prefix):
            """
            Print the name.
            """
            print prefix, name
        ...

.. _way_4:

Sub commands container and command arguments
--------------------------------------------
With the :ref:`way_2` we can also specify a command specific arguments list
using the **__arguments__** attribute.

.. code-block:: python

    @class_args
    class SubCommandsContainer(object):
        """
        Commands Container class.
        """
        # our command is dosub
        __cmd_name__ = 'dosub'
        # our command arguments
        __arguments__ = [
            ap_arg('--prefix', help="prefix string", default="The name is..")]
        # the sub command shared arguments.
        __shared_arguments__ = [ap_arg('name', help="The Name")]

        @arg()
        def name(self, name, prefix):
            """
            Print the name.
            """
            print prefix, name
        ...

Importing commands packages
---------------------------
A good way to keep our code ordered is to put modules under a sub folder which
can become, for convenience, a package. So we can have our structure like this.

.. code-block:: bash

    ├── commands
    │   ├── admin.py
    │   ├── __init__.py
    │   ├── user.py
    ├── multicommand.py

And our multicommand.py should looks like this.

.. code-block:: python
    :caption: multicommand.py
    :name: multicommand2.py

    from argparseinator import ArgParseInator
    from commands import admin, user

    ArgParseInator().check_command()

But if we want to add other command modules we have to import all of them.
And to do this we should modify our multicommand.py script.
Or we can use the :meth:`import_commands` function which loads all modules in
a package.

.. code-block:: python

    from argparseinator import ArgParseInator, import_commands
    import_commands('commands')

    ArgParseInator().check_command()

.. deprecated:: 1.0.15
   Use normal import instead. Possibly use :ref:`standalone_approch` or 
   :ref:`submodules_approch` or :ref:`subprojects_approch`.

