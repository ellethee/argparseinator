.. _class_dec:        

==============
Within classes
==============
We can also use classes for define our commands and subcommands. 
There are three properties that we can use within classes.

* :attr:`__cmd_name__`: Declare the command name. In this way the class becames
  a SubCommand container.

* :attr:`__arguments__`: Arguments list. When the class is a subcommands
  container we can set a list of attributes for the command itself.

* :attr:`__shared_arguments__`: Shared arguments list. in any case we can
  declare a list of arguments that will be shared by all commands or
  subcommands.

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
We can declare commands simply adding arg to class methods to turn the
class into a command container.

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
        """SubCommands container class."""
        # our command is dosub
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
        CommandsContainer class.
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

Sub-commads container and command arguments
-------------------------------------------
With the :ref:`way_2` we can also specify a command specific argumengs list
using the **__arguments__** attribute.

.. code-block:: python

    @class_args
    class SubCommandsContainer(object):
        """
        CommandsContainer class.
        """
        # our command is dosub
        __cmd_name__ = 'dosub'
        # our command arguments
        __arguments__ = [
            ap_arg('--prefix', help="prefix string", default="The name is..")]
        # the subcommand shared arguments.
        __shared_arguments__ = [ap_arg('name', help="The Name")]

        @arg()
        def name(self, name, prefix):
            """
            Print the name.
            """
            print prefix, name
        ...
