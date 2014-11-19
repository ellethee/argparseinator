# ArgParserInator #

Silly but funny thing that can help you to manage argparse,functions and classes


What is it?
-----------
It's a silly class, with some decorators, to use with functions or with classes and their methods to easily add argparse's arguments and subparsers to your script.

How to use it
-------------
it's easy
First instantiate the singleton class ArgParseInator with some parameters.

    AP = ArgParseInator(description="Silly script")

Then decorate your function.

ask to ArgParseInator to check_commands at script execution.

try your script