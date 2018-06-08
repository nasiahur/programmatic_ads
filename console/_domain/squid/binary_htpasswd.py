import os

#
#
#
from _domain.core import System

#
#
#
class BinaryHtPasswd:

    @staticmethod
    def full_path():

        if System.name() == System.WS_WINDOWS:
            return r"c:\Squid\lib\squid\htpasswd.exe"

        if System.name() == System.WS_FREEBSD:
            return "/usr/local/bin/htpasswd"

        return "/usr/bin/htpasswd"

# print BinaryHtPasswd.full_path()