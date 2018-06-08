#
#
#
import os
import subprocess

#
#
#
from _domain.core import System
#
#
#
from binary_sudo import BinarySudo

#
#
#
class Command:

    #
    # accepts arguments as [] and returns (exit_code, stdout, stderr) or throws an exception
    #
    def run(self, args):
    
        # the environment of Django contains the TZ variable that influences the time() system call in c++
        myenv = os.environ.copy()
        if 'TZ' in myenv:
            del myenv['TZ']

        # run this command
        process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=myenv)

        # wait until it is finished
        (stdout, stderr) = process.communicate()

        # and return
        return (process.returncode, stdout, stderr)

#
#
#
class CommandElevated:

    def run(self, args):

        # prepend with path to sudo
        if System.name() != System.WS_WINDOWS:
            args.insert(0, BinarySudo.full_path())

        # and execute normally
        return Command().run(args)


