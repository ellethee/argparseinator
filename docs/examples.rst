=============
Some examples
=============

Simple HTTP requests
====================
This simple script uses the functions approach to send simple HTTP requests
to a server.

Download :download:`this example script <../../examples/httprequest.py>`.

.. literalinclude:: ../../examples/httprequest.py
    :language: python
    :caption: httprequest.py
    :name: httprequest.py


Simple HTTP requests sub-classing :class:`ArgParseInated` object
================================================================
Let's do the same thing but by inheriting the class from :class:`ArgParseInated`.
We can define the shared argument ``url`` and pass an instance of requests.Session
to our HttpRequest class.

Download :download:`this example script <../../examples/httprequest2.py>`.

.. literalinclude:: ../../examples/httprequest2.py
    :language: python
    :caption: httprequest2.py
    :name: httprequest2.py
.. :emphasize-lines: 15, 21, 33, 43 .


Silly configuration example
===========================
This is a silly configuration example.

Download :download:`this example zip <../../examples/config.zip>`.

We have our configuration file written in yaml where we have defined username
and password.

.. literalinclude:: ../../examples/config.yaml
    :language: yaml
    :caption: config.yaml
    :name: config.yaml

.. literalinclude:: ../../examples/config.py
    :language: python
    :caption: config.py
    :name: config.py

Modular multi-commands script with sub-commands
===============================================
This script is a little more complicated anyway not so much.
It will be modular. That means it will load commands at run time.
We decided to create a script that can executes user commands and admin
commands.

For convenience we will put the admin part in a module named :mod:`admin.py`
and the user part in a module named :mod:`user.py`. And our modules will
reside in the **commands subfolder**.
(Actually we can have many modules into the commands sub folder)

Download :download:`this example zip <../../examples/multicommand.zip>`.

* `Main script`_

* `User commands`_

* `Admin commands`_

Main script
-----------
In the main script we will just import all the commands, pass all desired
arguments to the ArgParseInator and finally call the check_command method.


.. literalinclude:: ../../examples/multicommand.py
    :language: python
    :caption: multicommand.py
    :name: multicommand.py

.. note:: 

    We also defined the **__version__** at module level, ArgParseInator will
    handle it for us.


User commands
-------------
In this module we define our user commands. Its intended as example.
It doesn't really something useful.

.. literalinclude:: ../../examples/commands/user.py
    :language: python
    :caption: commnds/user.py
    :name: commands/user.py

Admin commands
--------------
And here we have our Administrations command. As you can see we used the
:ref:`authorize_commands` decorator for the :meth:`useradd` and
:meth:`userdelete` commands without the parameter, so :class:`ArgParseInator`
will use the global :ref:`auth_phrase`.
For the :meth:`deleteallusers` command, instead, we used a specif auth_phrase.

.. literalinclude:: ../../examples/commands/admin.py
    :language: python
    :caption: commands/admin.py
    :name: commands/admin.py
.. :emphasize-lines: 23, 38, 50


StandAlone Structure Example
============================
StandAlone project example.

Let's create the structure
--------------------------

.. code-block:: sh
    
    $ python -margparseinator -d ~/src/python -D"Greets people" greets

::

    ~/src/python/greets
    ├── greets
    │   ├── commands.py
    │   └── __init__.py
    └── greets.py

The running script
------------------
As you can see the script loads the submodules/package dinamically at runtime.

.. literalinclude:: ../../examples/greets/greets.py
    :language: python
    :caption: greets.py
    :name: greets.py


The __init__ module
-------------------
As you can see we can define here everything we need to run the main script.

.. literalinclude:: ../../examples/greets/greets/__init__.py
    :language: python
    :caption: greets/__init__.py
    :name: greets/__init__.py

The command module
------------------
As you can see 

.. literalinclude:: ../../examples/greets/greets/commands.py
    :language: python
    :caption: greets/commands.py
    :name: greets/commands.py


SubProjects structure example
=============================

python -margparseinator -s -d ../examples/pets dog
Let's create the structure
--------------------------

.. code-block:: sh
    
    $ python -margparseinator -s -d ~/src/python/pets dog
    $ python -margparseinator -s -d ~/src/python/pets cat
    $ python -margparseinator -s -d ~/src/python/pets bird
    # add a pets subproject for shared things
    $ python -margparseinator -s -d ~/src/python/pets pets

::

    ~/src/python/pets
    ├── bird
    │   ├── commands.py
    │   └── __init__.py
    ├── cat
    │   ├── commands.py
    │   └── __init__.py
    ├── dog
    │   ├── commands.py
    │   └── __init__.py
    ├── pets
    │   ├── commands.py
    │   └── __init__.py
    └── pets.py

The running script
------------------
As you can see the script loads the submodules/package dinamically at runtime.

.. literalinclude:: ../../examples/pets/pets.py
    :language: python
    :caption: pets.py
    :name: pets.py

The pets/main subproject
------------------------

.. literalinclude:: ../../examples/pets/pets/__init__.py
    :language: python
    :caption: pets/__init__.py
    :name: pets/__init__.py

The bird subproject
-------------------

.. literalinclude:: ../../examples/pets/bird/__init__.py
    :language: python
    :caption: bird/__init__.py
    :name: bird/__init__.py

The cat subproject
-------------------

.. literalinclude:: ../../examples/pets/cat/__init__.py
    :language: python
    :caption: cat/__init__.py
    :name: cat/__init__.py

The dog subproject
-------------------

.. literalinclude:: ../../examples/pets/dog/__init__.py
    :language: python
    :caption: dog/__init__.py
    :name: dog/__init__.py
