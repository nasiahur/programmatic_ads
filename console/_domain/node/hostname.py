import os
import subprocess

#
#
#
from _domain.core import Paths, System, Distrib
from _domain.utils import CommandElevated


#
# hostname
#
class HostName:

    def __init__(self):
        self.default = "localhost"     

    def configured_hostname(self):

        value = self.default

        # get the one from linux
        if System.WS_LINUX == System.name():

            with open('/etc/hostname') as fin:
                value = fin.read()                
                value = value.strip()

        return value

    def running_hostname(self):
        return subprocess.check_output('hostname').strip()

    def set(self, value):

        assert(len(value) > 0)

        exe  = os.path.join(Paths.bin_dir(), "hostname.py")
        arg1 = "--hostname=%s" % value
        arg2 = "--system=%s" % System.name()
        arg3 = "--distrib=%s" % Distrib.name()
        args = [exe, arg1, arg2, arg3]

        return CommandElevated().run(args)
