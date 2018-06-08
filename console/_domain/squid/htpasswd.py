import os

#
#
#
from _domain.utils import Command

#
#
#
from binary_htpasswd import BinaryHtPasswd

#
# a wrapper for the htpasswd command
#
class CommandHtPasswd:

    def __init__(self, htpasswd):

        self.htpasswd = htpasswd
        self.exe      = BinaryHtPasswd.full_path()

    def delete_user(self, user):

        if not os.path.exists(self.htpasswd):
            return

        # construct args
        args = [self.exe, "-D", self.htpasswd, user]

        # and run the command
        return Command().run(args)

    def create_user(self, user, pasw):

        # construct args
        args = [self.exe, "-b"]
        if not os.path.exists(self.htpasswd):
            args.append("-c")

        args.append(self.htpasswd)
        args.append(user)
        args.append(pasw)

        # and run
        return Command().run(args)
