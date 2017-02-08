SubModules structure example
=============================

Let's create the structure
--------------------------

.. code-block:: sh
    
    $ python -margparseinator -s -d ~/src/python/pets dog
    $ python -margparseinator -s -d ~/src/python/pets cat
    $ python -margparseinator -s -d ~/src/python/pets bird
    # add a pets submodule for shared things
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

The pets/main submodule
-----------------------

.. literalinclude:: ../../../examples/pets/pets/__init__.py
    :language: python
    :caption: pets/__init__.py
    :name: pets/__init__.py

The pets/main commands
----------------------

.. literalinclude:: ../../../examples/pets/pets/commands.py
    :language: python
    :caption: pets/commands.py
    :name: pets/commands.py

The dog submodule
-----------------

.. literalinclude:: ../../../examples/pets/dog/__init__.py
    :language: python
    :caption: dog/__init__.py
    :name: dog/__init__.py

The dog commands
----------------

.. literalinclude:: ../../../examples/pets/dog/commands.py
    :language: python
    :caption: dog/commands.py
    :name: dog/commands.py

The running script
------------------
As you can see the script loads the submodules/package dinamically at runtime.

.. literalinclude:: ../../../examples/pets/pets.py
    :language: python
    :caption: pets.py
    :name: pets.py

We can run the script in various ways 

.. code-block:: console
    
    # Using the *core* module name *pets*
    $ python pets.py pets allsays

    # No module name uses the default pets commands.
    $ python pets.py allsays

    # both cases the result is
    I woof dog
    I miaow cat
    I tweet bird

    # Passing the submodule name
    $ python pets.py dog say "I'm a coold dog!"
    
    I woof I'm a cool dog

    # submodules preserves the core module commands
    $ python pets.py dog allsays

    I woof dog
    I miaow cat
    I tweet bird


