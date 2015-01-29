=============
Some examples
=============

Simple http requests
====================
This simple script uses the functions approach to send simple http requests
to a server.

.. literalinclude:: ../../examples/httprequest.py
    :language: python


Simple http requests subclassing :class:`ArgParseInated` object
===============================================================
Let's do the same thing but subclassing the :class:`ArgParseInated` object we
can define the shared argument ``url`` and pass an instance of requests.Session
to our HttpRequest class.

.. literalinclude:: ../../examples/httprequest2.py
    :language: python
    :emphasize-lines: 15, 21, 33, 43 


Modular multi-commands script with sub-commands
===============================================
This script is a little more complicated anyway not so much.
It will be modular. That means it will load commands at runtime.
We decided to create a script that can executes user commands and admin
commands.

For convenience we will put the admin part in a module named :mod:`admin.py`
and the user part in a module named :mod:`user.py`. And our modules will
reside in the **commands subfolder**.
(Actually we can have many modules into the commands subfolder)

* `Main script`_

* `User commands`_

* `Admin commands`_

Main script
-----------
In the main script we will just import all the commands, pass all desidered
arguments to the ArgParseInator and finally call the check_command method.

.. literalinclude:: ../../examples/multicommand.py
    :language: python

.. note:: 

    We also defined the **__version__** at module level, ArgParseInator will
    handle it for us.


User commands
-------------
In this module we define our user commands. Its intended as example.
It doesn't really something useful.

.. literalinclude:: ../../examples/commands/user.py
    :language: python

Admin commands
--------------
And here we have our Administrations command. As you can see we used the
:ref:`authorize_commands` decorator for the :meth:`useradd` and
:meth:`userdelete` commands without the parameter, so :class:`ArgParseInator`
will use the global :ref:`auth_phrase`.
For the :meth:`deleteallusers` command, instead, we used a specif auth_phrase.

.. literalinclude:: ../../examples/commands/admin.py
    :language: python
    :emphasize-lines: 23, 38, 50
