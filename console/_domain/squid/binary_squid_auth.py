import os

#
#
#
from _domain.core import System

#
#
#
class BinaryBasicNcsaAuth:

    @staticmethod
    def full_path():

    	# windows (for debug only)
        if System.name() == System.WS_WINDOWS:
            return r"c:\Squid\bin\squidclient.exe"

        # centos and redhat
        if os.path.isfile("/etc/centos-release") or os.path.isfile("/etc/redhat-release"):
            return "/usr/lib64/squid/basic_ncsa_auth"

        # freebsd
        if System.name() == System.WS_FREEBSD:
            return "/usr/local/libexec/squid/basic_ncsa_auth"

        # by default - debian and ubuntu
        return "/usr/lib/squid/basic_ncsa_auth"


#
#
#
class BinaryBasicRadiusAuth:

    @staticmethod
    def full_path():

        # centos and redhat
        if os.path.isfile("/etc/centos-release") or os.path.isfile("/etc/redhat-release"):
            return "/usr/lib64/squid/basic_radius_auth"

        # windows (for debug only)
        if System.name() == System.WS_WINDOWS:
            return r"c:\Squid\bin\squidclient.exe"

        if System.name() == System.WS_FREEBSD:
            return "/usr/local/libexec/squid/basic_radius_auth"

        # by default - debian and ubuntu
        return "/usr/lib/squid/basic_radius_auth"

#
#
#
class BinaryBasicLdapAuth:

    @staticmethod
    def full_path():

        # centos and redhat
        if os.path.isfile("/etc/centos-release") or os.path.isfile("/etc/redhat-release"):
            return "/usr/lib64/squid/basic_ldap_auth"

        # windows (for debug only)
        if System.name() == System.WS_WINDOWS:
            return r"c:\Squid\bin\squidclient.exe"

        if System.name() == System.WS_FREEBSD:
            return "/usr/local/libexec/squid/basic_ldap_auth"

        # by default - debian and ubuntu
        return "/usr/lib/squid/basic_ldap_auth"

#
#
#
class BinaryNegotiateKerberosAuth:

    @staticmethod
    def full_path():

        # centos and redhat
        if os.path.isfile("/etc/centos-release") or os.path.isfile("/etc/redhat-release"):
            return "/usr/lib64/squid/negotiate_kerberos_auth"

        # windows (for debug only)
        if System.name() == System.WS_WINDOWS:
            return r"c:\Squid\bin\squidclient.exe"

        if System.name() == System.WS_FREEBSD:
            return "/usr/local/libexec/squid/negotiate_kerberos_auth"

        # by default - debian and ubuntu
        return "/usr/lib/squid/negotiate_kerberos_auth"

#
#
#
class BinaryNegotiateWrapperAuth:

    @staticmethod
    def full_path():

        # centos and redhat
        if os.path.isfile("/etc/centos-release") or os.path.isfile("/etc/redhat-release"):
            return "/usr/lib64/squid/negotiate_wrapper_auth"

        # windows (for debug only)
        if System.name() == System.WS_WINDOWS:
            return r"c:\Squid\bin\squidclient.exe"

        if System.name() == System.WS_FREEBSD:
            return "/usr/local/libexec/squid/negotiate_wrapper_auth"

        # by default - debian and ubuntu
        return "/usr/lib/squid/negotiate_wrapper_auth"