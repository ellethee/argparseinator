Decorators and Function declarations
====================================


* :ref:`ap_arg`

* :ref:`arg`

* :ref:`authorize_commands`

* :ref:`func_dec`

* :ref:`enable_class`

* :ref:`within_classes`


.. _ap_arg:

Add arguments to parser (**ap_arg**)
------------------------------------
**ap_arg** is not a decorator, but a silly convenience function that returns
a tuple with positional arguments and keyword arguments.
Useful to pass list of arguments to the parser.

.. code-block:: python

    inator = ArgParseInator(args=[
        ap_arg('-O', '--option', help="Optional parameter")
    ])

.. _arg:

Add arguments to a function (**@arg**)
--------------------------------------
**@arg** adds arguments to function in :meth:`ArgumentParser.add_argument` style.
Or just enable the function as :class:`ArgParseInator` command if no parameters are
passed.

If no parameters are passed to **@arg** and there are function arguments they
become the command arguments and optional arguments. 
For optional arguments all the options can be specify using a dictionary and
the argument becomes **--option_name** unless you use the :keyword:`flag` and the 
:keyword:`lflag` keys in the dictionary to specify the short and the long option name.

ArgParseInator will use the *function* **name** as command name unless
you pass the special parameter **cmd_name** that can change the command name
for the function. Or you can specify the name using the **function.__cmd_name__** form.


.. code-block:: python

    # Creates an ArgParseInator command without passing parameters to **@arg**
    # decorator. But retrieves them from the function itself.
    # it defines also the path option flags using **flag** and **lflag** keywords.
    # and changes the command name with the function.__cmd_name__ form.

    @arg()
    def save(filename, overwrite={'action': 'store_true', 'default':False},
             path={'flag': '-p', 'lflag': 'pth', 'help': "the file path", 'default': ""}):
        """
        A Save Function.
        """
        # code here 
    save.__cmd_name__ = 'mysave'


.. code-block:: python

    # Creates a ArgParseInator command **with** parameters.

    @arg('filename', help="the file name")
    @arg('-p', '--path', help="the file path", default='')
    @arg('--overwrite', help="overwrite the file", default=False)
    def save(filename, path, overwrite):
        """
        A save function.
        """
        # code here


.. code-block:: python

    # Creates a ArgParseInator command **without** parameters.

    @arg()
    def foo_print():
        """
        Foo!!!
        """
        # code_here


.. code-block:: python

    # Creates a ArgParseInator command **without** parameters and the command name
    # will be **foo**

    @arg(cmd_name="foo")
    def foo_print():
        """
        Foo!!!
        """
        # code_here


.. _authorize_commands:

Authorize commands (**@cmd_auth**)
----------------------------------
Sometimes our scripts can be potentially dangerous. 
So we would like to protect some commands with a *auth phrase*. 

And here comes the **@cmd_auth** decorator. 
We can pass the **auth_phrase** parameter which will be used to check the
authorization for the command or call it without the parameter, in this case it
will use the global :ref:`auth_phrase` passed to the ArgParseInator instance.

.. code-block:: python
    
    # with global auth_phrase
    @arg()
    @cmd_auth()
    def deleteall():
        # code_here
    
    # with command specific auth_phrase
    @arg()
    @cmd_auth('im-sure')
    def deleteall():
        # code_here

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
        # code_here

is the same as

.. code-block:: python

    @arg('name', help="The name")
    @arg('-s', '--surname', help="The surname", default='')
    def print_name(surname, name):
        # code_here

We can also refer to an argument declared in the top level parser or into the
parent of the function (if it is inside a class).

.. code-block:: python

    @arg()
    def print_foo(foo):
        # code_here

    # We instantiate the class with a foo top level optional parameter.
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
  sub commands

.. code-block:: python

    @class_args
    class Greetings(object):
        """
        Greeting command.
        """
        __cmd_name__ = 'greet'
        # code here

We will discuss the classes usage in the :ref:`within_classes` section.


