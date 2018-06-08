import os

#
#
#
from _domain.core import System
from _domain.utils import Command, CommandElevated


#
#
#
from binary_cachemgr import BinaryCacheMgr
from binary_squid import BinarySquid

#
#
#
class SquidCacheDir:

    @staticmethod
    def get():

        if os.path.isfile("/etc/centos-release") or os.path.isfile("/etc/redhat-release"):
            return "/var/spool/squid"

        if System.name() == System.WS_WINDOWS:
            return r"c:\Squid\bin\unknown.dir"

        if System.name() == System.WS_FREEBSD:
            return "/var/squid/cache"    

        return "/var/spool/squid"

#
#
#
#
# 
#
class SquidCacheInitializer:

    def __init__(self):

        self.exe = BinaryCacheMgr.full_path()
        
    def initialize(self):   

        arg1 = "--action=reset-cache"
        args = [self.exe, arg1]

        (exit_code, stdout, stderr) = CommandElevated().run(args)
        if exit_code == 0:
            return

        # if we got here everything is bad
        raise Exception(
            "Command %s failed.\n\tExit Code: %d\n\tSTDOUT: %s\n\tSTDERR: %s" % (" ".join(args), exit_code, stdout, stderr)
        )

