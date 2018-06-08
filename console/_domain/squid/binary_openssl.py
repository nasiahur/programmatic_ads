import os

#
#
#
from _domain.core import System

#
#
#
class BinaryOpenSsl:

    @staticmethod
    def full_path():

    	if System.name() == System.WS_WINDOWS:
    		return r"c:\OpenSSL-Win32\bin\openssl.exe"

        return "/usr/bin/openssl"
