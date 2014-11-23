Decorators and Function declarations
====================================


* :ref:`ap_arg`

* :ref:`arg`

* :ref:`enable_class`

* :ref:`authorize_commands`

* :ref:`func_dec`

* :ref:`class_dec`

.. _ap_arg:

Add arguments to parser (**ap_arg**)
------------------------------------
**ap_arg** is not a decorator, but a silly convenience function that returns
a tuple with positional arguments and keyword arguments.
Useful to pass list of arguments to the parsers.

.. code-block:: python

    inator = ArgParseInator(args=[
        ap_arg('-O', '--option', help="Optional parameter")
    ])

.. _arg:

Add arguments to a function (**@arg**)
--------------------------------------
**@arg** adds arguments to function in *ArgumentParser.add_argument* style.
Or just enable the function as ArgParseInator command if no parameters are
passed.

ArgParseInator will use the *function* **name** as command name unless
you pass the special param **cmd_name** that can change the the command name
for the funcion.


Create a ArgParseInator command **with** parameters.

.. code-block:: python

    @arg('filename', help="the file name")
    @arg('-p', '--path', help="the file path", default='')
    @arg('--overwrite', help="overwrite the file", default=False)
    def save(filename, path, overwrite):
        """
        A save function.
        """
        ...

Create a ArgParseInator command **without** parameters.

.. code-block:: python

    @arg()
    def foo_print():
        """
        Foo!!!
        """
        ...

Create a ArgParseInator command **without** parameters and the command name
will be **foo**

.. code-block:: python

    @arg(cmd_name="foo")
    def foo_print():
        """
        Foo!!!
        """
        ...


.. _enable_class:

Enable classes (**@class_args**)
--------------------------------
We can enable classes to become commands container simply adding a
**@class_args** decorator to the classes.

Once the class is enabled we can specify some class attributes that will
modify the commands behavior:

* **__cmd_name__** set the command name

* **__arguments__** set extra arguments for the command.

* **__shared_arguments__** set arguments which will be shared by the class
  subcommands

.. code-block:: python

    @class_args
    class Greetings(object):
        """
        Greeting command.
        """
        __cmd_name__ = 'greet'
        ...

We will discuss the classes usage in the :ref:`class_dec` section.


.. _authorize_commands:

Authorize commands (**@cmd_auth**)
----------------------------------
Sometimes our scripts can be potentially dangerous. 
So we would like to protect some commands with a *auth phrase*. 

And here comes the **@cmd_auth** decorator. 
We can pass the **auth_phrase** parameter which will be used to check the
autorization for the command or call il without the parameter, in this case it
will use the global :ref:`auth_phrase` passed to the ArgParseInator instance.

.. code-block:: python
    
    # with global auth_phrase
    @arg()
    @cmd_auth()
    def deleteall():
        ...
    
    # with command specific auth_phrase
    @arg()
    @cmd_auth('im-sure')
    def deleteall():
        ...

.. note::

    **@cmd_auth** automatically adds the **--auth** optional argument to the
    top level parser.


.. _func_dec:

Function declarations
---------------------
When we declare a function that will then be decorated, we can use both types
of parameters, positional and keyword. However, considering that the optional
parameters are declared with the decorator, we can declare all parameters as
positional without caring about the order.

.. code-block:: python

    @arg('name', help="The name")
    @arg('-s', '--surname', help="The surname", default='')
    def print_name(name, surname):
        ...

is the same as

.. code-block:: python

    @arg('name', help="The name")
    @arg('-s', '--surname', help="The surname", default='')
    def print_name(surname, name):
        ...

We can also refer to an argument declared in the top level parser or into the
parent of the function (if it is inside a class).

.. code-block:: python

    @arg()
    def print_foo(foo):
        ...

    # We istantiate che class with a foo top level optional parameter.
    inator = ArgParseInator(args=[ap_arg('--foo', help="Foo", default="bar")])

Last but not least the special parameter args.
If ArgParseInator find it in the function declaration will assign to it the
parse_args result.

.. code-block:: python

    @arg('name', help="the name")
    @arg('--surname', help="the surname")
    def print_args(args):
        print args.name, args.surname, args.foo

This can be useful if you don't know exactly what parameters you need or if
you are lazy enough (like me) to avoid typing all the parameters in the
function declaration.

