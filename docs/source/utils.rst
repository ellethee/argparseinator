=====
Utils
=====
ArgParseInator comes with few simply utils, the **init** function which 
create a project structure and the **get_compiled** function which returns the
compiled parser.

:func:`init`
============
::

    .. currentmodule:: argparseinator.__main__
                            
    .. argparse::
       :module: argparseinator.__main__
       :func: get_compiled
       :prog: python -margparseinator 

The Argparse Inator project structures aims to forget about the main script
and concentrate to the commands part of the project and simplify the
distribution/integration/extendibility.

.. _standalone_approch:

The StandAlone approch
----------------------
This approch has a project structure like this::

    project
    ├── project
    │   ├── commands.py
    │   ├── __init__.py
    └── project.py

And you can run it in this way

.. code-block:: sh

    $ python project/project.py --help

.. _submodules_approch:

The SubModules approch
----------------------
This approch has a project structure like this::

    project/
    ├── project             |
    │   ├── commands.py     | - the *core* folder is optional
    │   └── __init__.py     |
    ├── project.py
    ├── submod1
    │   ├── commands.py
    │   └── __init__.py
    ├── submod2
    │   ├── commands.py
    │   └── __init__.py
    └── submod3
        ├── commands.py
        └── __init__.py

And you can run it in this way

.. code-block:: sh

    $ python project/project.py --help 
    $ python project/project.py project --help 
    $ python project/project.py submod1 --help

In this case you have a main script **project.py** which loads the submodule
you asked for.

The **ArgParseInator** main call is done in the project/project/__init__.py, if
is present, otherwise you must set it up in the **project.py** script.

.. _subprojects_approch:

The SubProjects approch
-----------------------
This approch has a project structure like this::

    project/
    ├── project             |
    │   ├── __init__.py     | - the *core* folder is optional
    │   └── utils.py        | 
    ├── project.py
    ├── subpro1
    │   ├── commands.py
    │   └── __init__.py
    ├── subpro2
    │   ├── commands.py
    │   └── __init__.py
    └── subpro3
        ├── commands.py
        └── __init__.py

And you can run it in this way

.. code-block:: sh

    $ python project/project.py --help 
    $ python project/project.py project --help 
    $ python project/project.py subpro1 --help

The **SubProjects** is mix. You have a **SubModules** structure but there isn't
a **ArgParseInator** setup in the (optional) project/__init__.py.

Every SubProject have it's **Argparseinator** setup. And the optional project 
package/folder is used for shared modules.


The Skeleton folder
-------------------
ArgParseInator uses it's own skeleton folder::

    skeleton/
    ├── standalone
    │   ├── project
    │   │   ├── commands.py
    │   │   └── __init__.py
    │   └── project.py
    ├── submodules
    │   ├── project
    │   │   ├── commands.py
    │   │   └── __init__.py
    │   ├── project.py
    │   └── submodule
    │       ├── commands.py
    │       └── __init__.py
    └── subprojects
        ├── project
        │   ├── __init__.py
        │   └── utils.py
        ├── project.py
        └── submodule
            ├── commands.py
            └── __init__.py

Which contains the base structure for StandAlone, SubProjects ans SubModules
strcutures.

You can copy and modify your own skeleton folder but keep in mind:

    - Everything in the skeleton folder will be copied in the new project folder.
    - Only *project.py* script and *project* filder will renamed to the new project name.
    - Only the *submodule* will be renamed to the subproject/submodule folder.

Everything else will be copied as it is.


:func:`get_compiled`
====================
Argparseinator can use the :func:`get_compiled` function and autodoc with the
sphinx-argparse_ extension to quickly create documentation.

Is quite easy.

.. code-block:: python
    :caption: test.py
    :emphasize-lines: 2

    from argparseinator import ArgParseInator, arg
    from argparseinator import get_compiled

    @arg("word", help="The word")
    def say(self, word):
        """ say a word """
        print "say", word
        return 0

    ArgParseInator().check_command()
    

.. code-block:: rst
    :caption: test/index.rst

    .. currentmodule:: test

    .. automodule:: test

    .. argparse::
       :module: test
       :func: get_compiled
       :prog: test

.. _sphinx-argparse: https://sphinx-argparse.readthedocs.io/en/latest/index.html
