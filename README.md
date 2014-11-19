#ArgParserInator#

Silly but funny thing that can help you to manage argparse,functions and
classes.


##What is it?
It's a silly class, with some decorators, to use with functions or with
classes and their methods to easily add argparse's arguments and subparsers
to your script.

##How to use it
it's easy
First instantiate the singleton class ArgParseInator with some parameters.
    
```
#!python
from argparseinator import ArgParseInator, arg
AP = ArgParseInator(description="Silly script")
```

Then decorate your function.

```
#!python
@arg("name", help="print name")
def print_name(args):
    """
    Print name.
    """
    print "Printing the name...", args.name
```

ask to ArgParseInator to check_commands at script execution.

```
#!python
if __name__ == "__main__":
    AP.chek_command()
```

try your script help
```
#!bash
$ python apitest.py -h
usage: apitest.py [-h] name

Silly script

positional arguments:
  name        Name to print

optional arguments:
  -h, --help  show this help message and exit
```

try your script function
```
#!bash
$ python apitest.py Luca
Printing the name... Luca
```

```
**Note**: When we have only one fuction it automatically becomes the default.
```


##ArgParseInator object.##
__Argparseinator__(add_output=False, args=None, auth_phrase=None,
            never_single=False, **kwargs)

ArgParseInator object accepts all ArgumentParser's parameters,
plus some *personal* one.

+ **add_output** enable the --output option for set an output file see 
    [*write*](#markdown-header-methods) and
    [*writeln*](#markdown-header-methods) methods (default:__False__).

+ **args** List of ArgumentParser.add_argument parameters
    see [*ap_arg*](#markdown-header-functions) function (default:None)

+ **auth_phrase** set a generic authorization phrase for admin commands
    see [*cmd_auth*](#markdown-header-decorators) decorator (default:None).

+ **never_single** Force ArgParseInator to add subparser even if there
    is only one function (default:False).

+ __**kwargs__ ArgumentParser parameters.

#####Methods
+ **parse_args** parse arguments.

+ **chek_command** call parse_args if needed and then check for commands and
    call the rigth function. can accepts extra attrs for further use.

+ **check_auth** check authorization for given command (used internally).

+ **write** writes strings to the output (sys.stdout if not specified)

+ **writeln** writes strings to the output (sys.stdout if not specified) and 
    append a *newline* at the end.

##Decoratos
+ **arg** add to function ArgumentParser arguments in add_argument style.

+ **class_args** add class to ArgParseInator commands.

+ **cmd_auth** add an authorization request for the command if no parameters
    are passed it uses auth_phrase else check the parameter.

##Functions
+ **ap_arg** a simple wrapper that returns a tuple with *args and **kwargs.


#Examples



