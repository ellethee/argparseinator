from argparseinator import ArgParseInator, arg, ArgParseInated, class_args


@class_args
class Greetings(ArgParseInated):
    """
    Greet somebody.
    """

    @arg("name", help="The name")
    def ciao(self, name):
        """
        say ciao.
        """
        self.writeln(6, "We say ciao to", name)

    def __preinator__(self):
        if self.args.name.lower() == 'luca':
            self.args.name = "who? nobody?"

ArgParseInator().check_command()
