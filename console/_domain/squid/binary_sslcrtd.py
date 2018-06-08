import os

#
#
#
from _domain.core import System

#
#
#
class BinarySslCrtd:

    @staticmethod
    def full_path():

        if os.path.isfile("/etc/centos-release") or os.path.isfile("/etc/redhat-release"):
            return "/usr/lib64/squid/ssl_crtd"

        if System.name() == System.WS_WINDOWS:
            return r"c:\Squid\bin\ssl_crtd.exe"

        if System.name() == System.WS_FREEBSD:
            return "/usr/local/libexec/squid/ssl_crtd"    

        return "/usr/lib/squid/ssl_crtd"

    @staticmethod
    def get_dir():

        if os.path.isfile("/etc/centos-release") or os.path.isfile("/etc/redhat-release"):
            return "/var/spool/squid_ssldb"

        if System.name() == System.WS_WINDOWS:
            return r"c:\Squid\bin\unknown.dir"

        if System.name() == System.WS_FREEBSD:
            return "/var/squid/ssldb"    

        return "/var/spool/squid_ssldb"


