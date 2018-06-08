import os
import platform

#
#
#
class System(object):

    WS_WINDOWS = "windows"
    WS_LINUX   = "linux"
    WS_FREEBSD = "freebsd"

    @staticmethod
    def name():
        
        # set name
        system_str = platform.system()

        if system_str == "Windows":
            return System.WS_WINDOWS
        elif system_str == "Linux":
            return System.WS_LINUX
        elif system_str == "FreeBSD":
            return System.WS_FREEBSD
        
        raise Exception("Unknown system: %s" % system_str)


#
#
#
class Distrib:

    WS_WINDOWSX = "windowsx"    # generic windows
    WS_UBUNTU16 = "ubuntu16"
    WS_DEBIAN9  = "debian9"
    WS_CENTOS7  = "centos7"
    WS_FREEBS11 = "freebsd11"
    WS_PFSENSE  = "pfsense"

    @staticmethod
    def name():

        # return distrib based on system
        if System.WS_WINDOWS == System.name():
            return Distrib.WS_WINDOWSX

        if System.WS_FREEBSD == System.name():

            if os.path.isfile("/etc/version"):
                return Distrib.WS_PFSENSE
                
            return Distrib.WS_FREEBS11

        if System.WS_LINUX == System.name():

            if os.path.isfile("/etc/centos-release") or os.path.isfile("/etc/redhat-release"):
                return Distrib.WS_CENTOS7

            if os.path.isfile("/etc/os-release"):

                with open("/etc/os-release", "r") as fin:
                    data = fin.read() 
                    if data.find("ubuntu") == -1:
                        return Distrib.WS_DEBIAN9

            return Distrib.WS_UBUNTU16

        raise Exception("Cannot determine distrib for: %s" % system_str)

    @staticmethod
    def arch():

        # assume default
        value = "amd64"

        # for debugging
        if System.WS_WINDOWS == System.name():
            return value

        # see if this is i386
        if platform.architecture()[0] != '64bit':
            value = "i386"

        # it may also be arm
        try:
            with open("/proc/cpuinfo", "r") as fin:
                data = fin.read()

            if data.find("ARMv7") != -1:
                value = "armhf"
        except Exception as e:
            pass

        # and return
        return value

#
#
#
class WsUser:

    @staticmethod
    def name():
        return "websafety"

#
#
#
class WsGroup:

    @staticmethod
    def name():
        return "websafety"

