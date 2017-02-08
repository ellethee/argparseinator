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

.. literalinclude:: ../../../examples/greets/greets.py
    :language: python
    :caption: greets.py
    :name: greets.py


The __init__ module
-------------------
As you can see we can define here everything we need to run the main script.

.. literalinclude:: ../../../examples/greets/greets/__init__.py
    :language: python
    :caption: greets/__init__.py
    :name: greets/__init__.py

The command module
------------------
As you can see 

.. literalinclude:: ../../../examples/greets/greets/commands.py
    :language: python
    :caption: greets/commands.py
    :name: greets/commands.py
