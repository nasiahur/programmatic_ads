import os

#
#
#
from _domain.core import System

#
#
#
class BinarySquidClient:

    @staticmethod
    def full_path():

        if os.path.isfile("/etc/centos-release") or os.path.isfile("/etc/redhat-release") or os.path.isfile("/etc/SuSE-release"):
            return "/usr/bin/squidclient"

        if System.name() == System.WS_WINDOWS:
            return r"c:\Squid\bin\squidclient.exe"

        if System.name() == System.WS_FREEBSD:
            #if self.is_pfsense():
            #    return "/usr/local/sbin/squidclient"    
            return "/usr/local/sbin/squidclient"    

        return "/usr/bin/squidclient"
