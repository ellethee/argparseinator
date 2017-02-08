======
Events
======

ArgParseInator can handle two simply events **before_execute** and **after_execute**.
These events can be used on two levels: **class level** and **command level**.
The **command level** event overrides the **class level** event.
If the **before_execute** event returns something different than **None** or 
than a **3 elements tuple** which the first item is different than **None** will
interrupt the process and return the **before_execute** value.

The two levels differs in declaration but have the same return type.
Obvously the command level leacks the *_cmd_name* parameter.

.. code-block:: python
    
    # class level event
    def event(self, _cmd_name, *args, **kwargs):
        pass

    # command level event
    def event(self, *args, **kwargs):
        pass

    # simple breaking return
    return 1

    # 2 values breaking return
    return 2, "I Will stop executions"

    # 3 values NON breaking return
    return None, ['new', 'positional', 'args'], {'new': 'keywords args'}
    
    # 3 values breaking return
    return 1, ['new', 'positional', 'args'], {'new': 'keywords args'}

    # 3 values breaking tuple return
    return (2, "I Will stop executions", ), ['new', 'positional', 'args'], {'new': 'keywords args'}


Examples
--------
Some silly example.

.. code-block:: python

    from argparseinator import ArgParseInated
    from argparseinator import arg, ap_arg
    from argparseinator import class_args


    @class_args
    class Commands(ArgParseInated):
        """test commands"""

        # we can share the only argument
        __shared_arguments__ = [ap_arg("word", help="The word")]

        def before_execute(self, _cmd_name, *args, **kwargs):
            """Class Level Before execute event"""
            # if we are going to whisper we will replace the word.
            if _cmd_name == 'whisper':
                # return None as first element so we will continue the execution.
                return None, ['pst, pst'], kwargs

        @arg()
        def whisper(self, word):
            """ whisper a word """
            print "Whisper", word
            return 0

        @arg()
        def say(self, word):
            """ say a word """
            print "Say", word
            return 0

        @arg()
        def shout(self, word):
            """ shout a word """
            print "Shout", word
            return 0

        def shout_before_execute(self, *args, **kwargs):
            """Command Level Before execute event"""
            print "Please dont shout!"
            # we will break the execution with a message too
            return 1, "\nBe quiet\n"
        shout.before_execute = shout_before_execute


