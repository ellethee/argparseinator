=====================
ArgParseInated object
=====================
.. class:: ArgParseInated(parseinator, \**new_attributes)

This class is intended to be subclassed and automatically expose the 
:meth:`write`, :meth:`writeln` methods and the :attr:`args` attribute of the 
:class:`ArgParseInator`. Plus expose all passed **new_attributes** which will
passed by the :meth:`ArgParseInator.check_command`.
It has also the :ref:`preinator` method which is called just at the
__init__ end.
So we can use it to do some extra action before the command is execute.

.. code-block:: python

    class Greetings(ArgParseInated):
        """
        Greet somebody.
        """
       
        @arg()
        def ciao(self):
            """
            say ciao.
            """
            self.writeln(self.prefix, "ciao to", self.name)

    ArgParseInator().check_command(prefix="We say", name="Luca")

.. _preinator:

__preinator__
^^^^^^^^^^^^^
The original name was **__prepare__** but i've changed it to avoid problems.
It's just called at the end of the :meth:`__init__` method and is intended to
do some action before :class:`ArgParseInator` executes the command.

.. code-block:: python

    class Greetings(ArgParseInated):
        """
        Greet somebody.
        """

        @arg("name", help="The name")
        def ciao(self, name):
            """
            say ciao.
            """
            self.writeln("We say ciao to", name)


        def __preinator__(self):
            if self.args.name.lower() == 'luca':
                self.args.name = "who? nobody?"

    ArgParseInator().check_command()
