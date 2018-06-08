from nettypes import ActualNetDevice, CONFIG_TYPE_DHCP, CONFIG_TYPE_NONE, CONFIG_TYPE_STATIC


#
#
#
class CentOsIpParser:

    def fill(self, device):
        raise Exception("CentOsIpParser::fill - not implemented!")

#
#
#
class DebianIpParser:

    def fill(self, device):

        # load the parser
        from netaddr_debian import Parser

        # parse existing file in /etc/network/interfaces
        path = "/etc/network/interfaces"

        # parse the file
        file = Parser().parse(path)

        # and set its properties
        self.configure(file, device)
        
    def configure(self, file, device):

        for iface in file.ifaces:
            if iface.logical_name == device.name:
                if iface.get_addr_family() == "inet":
                    self.configure_ipv4(iface, device.ip4)
                if iface.get_addr_family() == "inet6":
                    self.configure_ipv6(iface, device.ip6)

    def configure_ipv4(self, iface, ipv4):
        
        # assume none
        ipv4.config_type = CONFIG_TYPE_NONE

        # set method
        method = iface.get_config_method()
        if method == "static":
            ipv4.config_type = CONFIG_TYPE_STATIC
        elif method == "dhcp":
            ipv4.config_type = CONFIG_TYPE_DHCP
        elif method == "loopback":
            pass            
        else:
            pass

        ipv4.address     = iface.get_address()
        ipv4.netmask     = iface.get_netmask()
        ipv4.gateway     = iface.get_gateway()
        ipv4.dns_search  = iface.get_dns_search()

        dnses = iface.get_dns_nameservers()
        if len(dnses) > 0:
            ipv4.dns_srv1 = dnses[0]
        if len(dnses) > 1:
            ipv4.dns_srv2 = dnses[1]

    def configure_ipv6(self, iface, ipv6):
        
        # assume none
        ipv6.config_type = CONFIG_TYPE_NONE

        # set method
        method = iface.get_config_method()
        if method == "static":
            ipv6.config_type = CONFIG_TYPE_STATIC
        elif method == "dhcp":
            ipv6.config_type = CONFIG_TYPE_DHCP
        elif method == "loopback":
            pass            
        else:
            pass

        ipv6.address     = iface.get_address()
        ipv6.subnet      = iface.get_netmask()
        ipv6.gateway     = iface.get_gateway()
        ipv6.dns_search  = iface.get_dns_search()

        dnses = iface.get_dns_nameservers()
        if len(dnses) > 0:
            ipv6.dns_srv1 = dnses[0]
        if len(dnses) > 1:
            ipv6.dns_srv2 = dnses[1]


if __name__ == "__main__":

    d = ActualNetDevice()
    d.name = "ens160"
    p = DebianIpParser().fill(d)    

    
    print "Device: %s" % d.name
    print "\tMAC: %s" % d.mac
    print "\tState: %s" % d.state

    print "\tIP4:"
    print "\t\t%s" % d.ip4.config_type
    print "\t\t%s" % d.ip4.address
    print "\t\t%s" % d.ip4.netmask
    print "\t\t%s" % d.ip4.gateway
    print "\t\t%s" % d.ip4.dns_srv1
    print "\t\t%s" % d.ip4.dns_srv2
    print "\t\t%s" % d.ip4.dns_search

    print "\tIP6:"
    print "\t\t%s" % d.ip6.config_type
    print "\t\t%s" % d.ip6.address
    print "\t\t%s" % d.ip6.subnet
    print "\t\t%s" % d.ip6.gateway
    print "\t\t%s" % d.ip6.dns_srv1
    print "\t\t%s" % d.ip6.dns_srv2
    print "\t\t%s" % d.ip6.dns_search