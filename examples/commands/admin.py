# -*- coding: utf-8 -*-
"""
    Administation commands for multi commands example.
"""
from argparseinator import class_args, arg, cmd_auth, ArgParseInated


class UserExistsError(Exception):
    """Fake user error"""
    pass

UserNotExistsError = UserExistsError


@class_args
class Admin(ArgParseInated):
    """Administrations commands."""
    # Our command name.
    __cmd_name__ = "admin"

    @arg("username", help="username")
    @arg("-p", "--passwd", help="User parssword")
    @cmd_auth()
    def useradd(self, username, passwd):
        """Fake Create new user command."""
        self.writeln("Creating user", username, '...')
        try:
            # ... create user code.
            pass
        except UserExistsError:
            return 1, "User {} already exists".format(username)
        if passwd:
            # ... set password code.
            pass
        return 0, "User {} created".format(username)

    @arg("username", help="username")
    @cmd_auth()
    def userdelete(self, username):
        """Fake Delete user command."""
        self.writeln("Deleting user", username, '...')
        try:
            # ... delete user code.
            pass
        except UserNotExistsError:
            return 1, "User {} do not exists".format(username)
        return 0, "User {} deleted".format(username)

    @arg()
    @cmd_auth("yesiwantit")
    def deleteallusers(self):
        """Fake delete all users command"""
        self.writeln("Deleting ALL users...")
        # ... delete all users code
        return 0, "All users deleted"
