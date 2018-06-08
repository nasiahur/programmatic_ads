import os

#
#
#
from _domain.core import System, Distrib

#
#
#
from .nettypes import *
from .netaddr import *

#
#
#
class NetDeviceEnumerator:

    def enumerate(self):

        if System.WS_LINUX == System.name():
            return self.enumerate_linux()

        elif System.WS_FREEBSD == System.name():
            return self.enumerate_freebsd()

        return self.debug_enumerate()

    def enumerate_freebsd(self):
        raise Exception("NetDeviceEnumerator::enumerate_freebsd - not implemented on system '%s'" % System.name())

    def debug_enumerate(self):

        d1 = ActualNetDevice()
        d1.name   = "ens160"
        d1.mac    = "11:0C:29:2A:77:E3"
        d1.state  = "UP"
        d1.ip4.config_type     = CONFIG_TYPE_STATIC
        d1.ip4.address         = "192.168.1.14"
        d1.ip4.netmask         = "255.255.255.0"
        d1.ip4.gateway         = "192.168.1.1"
        d1.ip4.dns_srv1        = "192.168.1.4"
        d1.ip4.dns_srv2        = "192.168.1.5"
        d1.ip4.dns_search      = "diladele.lan"
        d1.ip6.config_type     = CONFIG_TYPE_NONE

        d2 = ActualNetDevice()
        d2.name   = "ens260"
        d2.mac    = "22:0C:29:2A:77:E3"
        d2.state  = "UP"
        d2.ip4.config_type     = CONFIG_TYPE_DHCP
        d2.ip6.config_type     = CONFIG_TYPE_NONE

        return {
            "ens160" : d1,
            "ens260" : d2
        }

    def enumerate_linux(self):

        # get the names of the cards installed
        names = []  
        for (dirpath, dirnames, filenames) in os.walk("/sys/class/net"):
            names.extend(dirnames)
            break

        nics = {}
        for name in names:

            # skip loopback
            if name == "lo":
                continue

            # skip the virtual device
            if self.is_virtual(name):
                continue           

            # save the device
            nics[name] = self.enumerate_linux_device(name)

        return nics

    def is_virtual(self, device):

        path = os.readlink(os.path.join("/sys/class/net", device))
        if path.find("devices/virtual/") != -1:
            return True

        return False


    def enumerate_linux_device(self, name):

        device = ActualNetDevice()
        device.name   = name
        device.mac    = self.enumerate_device_attribute_linux(name, "address")
        device.state  = self.enumerate_device_attribute_linux(name, "operstate")
        
        # not used
        # self.enumerate_device_attribute_linux(name, "mtu")
        # self.enumerate_device_attribute_linux(name, "carrier")
        # self.enumerate_device_attribute_linux(name, "duplex")
        # self.enumerate_device_attribute_linux(name, "speed")

        # debug check
        assert(System.WS_LINUX == System.name())

        # assume
        device.ip4.config_type = CONFIG_TYPE_DHCP
        device.ip6.config_type = CONFIG_TYPE_NONE

        # now try reading currently configured settings from the system
        if Distrib.name() in [Distrib.WS_DEBIAN9, Distrib.WS_UBUNTU16]:
            DebianIpParser().fill(device)
        else:
            raise Exception("NetDeviceEnumerator::enumerate_linux_device - not implemented on distrib '%s'" % Distrib.name())

        # ok return nicely
        return device

    def enumerate_device_attribute_linux(self, name, attr):

        path = os.path.join("/sys/class/net", name, attr)
        if os.path.exists(path):
            with open(path, "r") as fin:
                return fin.readline().strip().strip('\n').upper()

        return ""


