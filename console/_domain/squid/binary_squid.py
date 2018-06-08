import os

#
#
#
from _domain.core import System, Distrib

#
#
#
class BinarySquid:

    @staticmethod
    def full_path():

        # windows (for debug only)
        if System.name() == System.WS_WINDOWS:
            return r"c:\Squid\bin\squid.exe"

        # centos and redhat
        if os.path.isfile("/etc/centos-release") or os.path.isfile("/etc/redhat-release"):
            return "/usr/sbin/squid"

        # freebsd
        if System.name() == System.WS_FREEBSD:
            return "/usr/local/sbin/squid"

        # by default - debian and ubuntu
        return "/usr/sbin/squid"

    @staticmethod
    def runas_user():  

        if System.WS_WINDOWS == System.name():
            return "unknown"

        if System.WS_FREEBSD == System.name():
            return "squid"

        assert(System.WS_LINUX == System.name())

        if Distrib.WS_CENTOS7 == Distrib.name():
            return "squid"

        if Distrib.name() in [Distrib.WS_DEBIAN9, Distrib.WS_UBUNTU16]:
            return "proxy"

        raise Exception("Unknown distrib '%s' in BinarySquid.runas_user" % Distrib.name())




